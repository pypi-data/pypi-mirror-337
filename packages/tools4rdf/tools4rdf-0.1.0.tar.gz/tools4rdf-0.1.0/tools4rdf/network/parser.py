import os
import networkx as nx

from tools4rdf.network.term import OntoTerm, strip_name
from tools4rdf.network.patch import patch_terms
from rdflib import Graph, RDF, RDFS, OWL, BNode, URIRef


def parse_ontology(infile, format="xml"):
    if not os.path.exists(infile):
        raise FileNotFoundError(f"file {infile} not found!")
    graph = Graph()
    graph.parse(infile, format=format)
    return OntoParser(graph)


class OntoParser:
    def __init__(self, graph):
        self.graph = graph
        self._data_dict = None

    def _initialize(self):
        self._data_dict = {
            "classes": [],
            "attributes": {
                "class": {},
                "object_property": {},
                "data_property": {},
                "data_nodes": {},
            },
            "mappings": {},
            "namespaces": {},
            "extra_namespaces": {},
        }
        self.extract_classes()
        self.extract_relations(relation_type="union")
        self.extract_relations(relation_type="intersection")
        self.add_classes_to_attributes()
        self.parse_subclasses()
        self.add_subclasses_to_owlThing()
        self.parse_equivalents()
        self.parse_named_individuals()
        self.extract_object_properties()
        self.extract_data_properties()
        self.recheck_namespaces()

    @property
    def classes(self):
        return self.data_dict["classes"]

    @property
    def mappings(self):
        return self.data_dict["mappings"]

    @property
    def namespaces(self):
        return self.data_dict["namespaces"]

    @property
    def extra_namespaces(self):
        return self.data_dict["extra_namespaces"]

    @property
    def attributes(self):
        return self.data_dict["attributes"]

    @property
    def data_dict(self):
        if self._data_dict is None:
            self._initialize()
        return self._data_dict

    def __add__(self, ontoparser):
        """
        Add method; in principle it should add-
        - classes
        - attributes dict
        """
        graph = self.graph + ontoparser.graph
        return OntoParser(graph)

    def __radd__(self, ontoparser):
        return self.__add__(ontoparser)

    @property
    def base_iri(self):
        base_iri = None
        for s in self.graph.subjects(RDF.type, OWL.Ontology):
            base_iri = str(s)
        return base_iri

    def recheck_namespaces(self):
        for mainkey in ["class", "object_property", "data_property"]:
            for key, val in self.attributes[mainkey].items():
                namespace = self.attributes[mainkey][key].namespace
                if namespace not in self.namespaces.keys():
                    self.namespaces[namespace] = self.attributes[mainkey][
                        key
                    ].namespace_with_prefix

    def extract_classes(self):
        self._data_dict["classes"] = list(self.graph.subjects(RDF.type, OWL.Class))
        self._data_dict["classes"].append(URIRef("http://www.w3.org/2002/07/owl#Thing"))

    def extract_object_properties(self):
        object_properties = list(self.graph.subjects(RDF.type, OWL.ObjectProperty))
        for cls in object_properties:
            term = self.create_term(cls)
            term.domain = self.get_domain(cls)
            term.range = self.get_range(cls)
            term.node_type = "object_property"
            self.attributes["object_property"][term.name] = term

    def extract_data_properties(self):
        data_properties = list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))
        for cls in data_properties:
            term = self.create_term(cls)
            term.domain = self.get_domain(cls)
            rrange = self.get_range(cls)
            rrange = [x.split(":")[-1] for x in rrange]
            rrange = patch_terms(term.uri, rrange)

            term.range = rrange
            term.node_type = "data_property"
            self.attributes["data_property"][term.name] = term

            # now create data nodes
            data_term = OntoTerm()
            data_term.name = term.name + "value"
            data_term.node_type = "data_node"
            self.attributes["data_property"][
                term.name
            ].associated_data_node = data_term.name
            self.attributes["data_nodes"][data_term.name] = data_term

    def extract_values(self, subject, predicate):
        vallist = list([x[2] for x in self.graph.triples((subject, predicate, None))])
        if len(vallist) > 0:
            return vallist[0]
        else:
            return None

    def extract_relations(self, relation_type):
        if relation_type == "union":
            owl_term = OWL.unionOf
        elif relation_type == "intersection":
            owl_term = OWL.intersectionOf

        to_delete = []
        for term in self.classes:
            if isinstance(term, BNode):
                union_term = self.extract_values(term, owl_term)
                if union_term is not None:
                    unravel_list = []
                    self.unravel_relation(union_term, unravel_list)
                    self.mappings[term.toPython()] = {
                        "type": relation_type,
                        "items": [strip_name(item.toPython()) for item in unravel_list],
                    }
                    to_delete.append(term)
        for term in to_delete:
            self.classes.remove(term)

    def add_classes_to_attributes(self):
        for cls in self.classes:
            term = self.create_term(cls)
            term.node_type = "class"
            self.attributes["class"][term.name] = term

    def get_description(self, cls):
        comment = self.graph.value(
            cls, URIRef("http://purl.obolibrary.org/obo/IAO_0000115")
        )
        if comment is None:
            comment = self.graph.value(
                cls, URIRef("http://www.w3.org/2000/01/rdf-schema#comment")
            )
        if comment is None:
            comment = ""
        return comment

    def lookup_node(self, term):
        if isinstance(term, BNode):
            # lookup needed
            term_name = term.toPython()
            if term_name in self.mappings:
                terms = self.mappings[term_name]["items"]
            else:
                terms = [strip_name(term.toPython())]
        else:
            terms = [strip_name(term.toPython())]
        # so here we map the domain and range wrt to other heirarchies
        additional_terms = []
        # first get subclasses which will share the domain and range
        for term in terms:
            # check if such a thing exists in the class
            if term in self.attributes["class"]:
                # get the subclasses
                additional_terms += self.attributes["class"][term].subclasses
                # get the equivalent classes
                additional_terms += self.attributes["class"][term].equivalent_classes
                # get the named individuals
                additional_terms += self.attributes["class"][term].named_individuals
        # add additiona terms to terms
        terms += additional_terms
        return terms

    def lookup_class(self, term):
        if isinstance(term, BNode):
            term = term.toPython()
        else:
            term = strip_name(term.toPython())
        # print(term)
        if term in self.attributes["class"]:
            return [self.attributes["class"][term].name]
        elif term in self.mappings:
            return self.mappings[term]["items"]
        else:
            return []

    def get_domain(self, cls):
        domain = []
        for triple in self.graph.triples(
            (cls, URIRef("http://www.w3.org/2000/01/rdf-schema#domain"), None)
        ):
            domain_term = self.lookup_node(triple[2])
            for term in domain_term:
                domain.append(term)
        return domain

    def get_range(self, cls):
        rrange = []
        for triple in self.graph.triples(
            (cls, URIRef("http://www.w3.org/2000/01/rdf-schema#range"), None)
        ):
            range_term = self.lookup_node(triple[2])
            for term in range_term:
                rrange.append(term)
        return rrange

    def create_term(self, cls):
        iri = cls.toPython()
        term = OntoTerm(iri)
        term.description = self.get_description(cls)
        term._object = cls
        return term

    def unravel_relation(self, term, unravel_list):
        if term == RDF.nil:
            return
        first_term = self.graph.value(term, RDF.first)
        if first_term not in unravel_list:
            unravel_list.append(first_term)
        second_term = self.graph.value(term, RDF.rest)
        self.unravel_relation(second_term, unravel_list)

    def parse_subclasses(self):
        for key, cls in self.attributes["class"].items():
            for obj in self.graph.objects(cls._object, RDFS.subClassOf):
                superclasses = self.lookup_class(obj)
                for superclass in superclasses:
                    self.attributes["class"][superclass].subclasses.append(cls.name)

    def add_subclasses_to_owlThing(self):
        for key, cls in self.attributes["class"].items():
            objects = list(self.graph.objects(cls._object, RDFS.subClassOf))
            if len(objects)==0:
                self.attributes["class"]["owl:Thing"].subclasses.append(cls.name)

    def parse_equivalents(self):
        for key, cls in self.attributes["class"].items():
            for equivalent in self.graph.objects(cls._object, OWL.equivalentClass):
                if strip_name(equivalent) in self.attributes["class"]:
                    self.attributes["class"][
                        strip_name(equivalent)
                    ].equivalent_classes.append(cls.name)
                    cls.equivalent_classes.append(strip_name(equivalent))

    def parse_named_individuals(self):
        named_individuals = list(self.graph.subjects(RDF.type, OWL.NamedIndividual))
        for cls in named_individuals:
            # find parent
            term = self.create_term(cls)
            self.attributes["class"][term.name] = term
            parents = list(self.graph.objects(cls, RDF.type))
            for parent in parents:
                if parent != OWL.NamedIndividual:
                    self.attributes["class"][
                        strip_name(parent.toPython())
                    ].named_individuals.append(term.name)

    def get_attributes(self):
        # add first level - namespaces
        mapdict = {key: {} for key in self.namespaces.keys()}

        # now iterate over all attributes
        for k1 in ["class", "object_property", "data_property"]:
            for k2, val in self.attributes[k1].items():
                mapdict[val.namespace][val.name_without_prefix] = val
        return mapdict

    def get_networkx_graph(self):
        g = nx.DiGraph()
        for key, val in self.attributes["class"].items():
            g.add_node(val.name, node_type="class")

        for property_key in ["object_property", "data_property"]:
            for key, val in self.attributes[property_key].items():
                g.add_node(val.name, node_type=property_key)

                # add edges between them
                for d in val.domain:
                    g.add_edge(d, val.name)

                if property_key == "object_property":
                    for r in val.range:
                        g.add_edge(val.name, r)
                else:
                    g.add_edge(val.name, val.associated_data_node)
        return g

    def add_term(
        self,
        uri,
        node_type,
        namespace=None,
        dm=(),
        rn=(),
        data_type=None,
        node_id=None,
        delimiter="/",
    ):
        """
        Add a node.

        Parameters
        ----------
        uri : str
            The URI of the node.
        node_type : str
            The type of the node.
        namespace : str, optional
            The namespace of the node.
        dm : list, optional
            The domain metadata of the node.
        rn : list, optional
            The range metadata of the node.
        data_type : str, optional
            The data type of the node.
        node_id : str, optional
            The ID of the node.
        delimiter : str, optional
            The delimiter used for parsing the URI.

        Raises
        ------
        ValueError
            If the namespace is not found.

        """
        term = OntoTerm(
            uri,
            namespace=namespace,
            node_type=node_type,
            dm=dm,
            rn=rn,
            data_type=data_type,
            node_id=node_id,
            delimiter=delimiter,
        )
        if term.namespace not in self.namespaces.keys():
            raise ValueError("Namespace not found, first add namespace")
        self.attributes[node_type][term.name] = term

    def add_namespace(self, namespace_name, namespace_iri):
        """
        Add a new namespace.

        Parameters
        ----------
        namespace_name : str
            The name of the namespace to add.
        namespace_iri : str
            The IRI of the namespace.

        Raises
        ------
        KeyError
            If the namespace already exists.

        """
        if namespace_name not in self.namespaces.keys():
            self.namespaces[namespace_name] = namespace_iri
