from rdflib import Graph


class GraphLoader:
    graph = Graph().parse("youtube.ttl")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GraphLoader, cls).__new__(cls)
        return cls.instance
