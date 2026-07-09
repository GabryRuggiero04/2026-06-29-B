import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._compInizio = None
        self._bestNumBrani = None
        self._allConnComp = None
        self._dimPath = None
        self._allEdges = None
        self._allNodes = DAO.getAllNodes()
        self._bestPath = None
        self._idMap = {}
        for n in self._allNodes:
            self._idMap[n.AlbumId] = n
        self._graph = nx.Graph()

    def setTracksByAlbum(self):
        for n in self._allNodes:
            DAO.getTracksByAlbum(n)

    def buildGraph(self):
        self._graph.clear()
        self.setTracksByAlbum()
        self._graph.add_nodes_from(self._allNodes)
        self.addEdges()

    def addEdges(self):
        self._allEdges = DAO.getAllEdges()
        for e in self._allEdges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]])

    def getGraph(self):
        return self._graph

    def detailGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def numConnComponent(self):
        return nx.number_connected_components(self._graph)

    def maxConnComponent(self):
        comp= nx.connected_components(self._graph)
        maxcomp = max(comp, key=len)
        return maxcomp

    def getAlbumDD(self):
        return self._allNodes

    def getPath(self, nodoInizio, dim):
        self._bestPath = []
        self._dimPath = dim
        self._allConnComp= list(nx.connected_components(self._graph))
        self._bestNumBrani=0
        if dim > len(self._allConnComp):
            return [], 0
        for c in self._allConnComp:
            if nodoInizio in c:
                self._compInizio = c
                break
        compRimaste=[]
        for c in self._allConnComp:
            if c!=self._compInizio:
                compRimaste.append(c)
        self.ricorsione([nodoInizio], compRimaste, 0)
        return self._bestPath, self._bestNumBrani

    def ricorsione(self, parziale, compRimaste, indice):
        if len(parziale) == self._dimPath:
            numBraniParz = self.calcoloNumBrani(parziale)
            if numBraniParz > self._bestNumBrani:
                self._bestNumBrani = numBraniParz
                self._bestPath = copy.deepcopy(parziale)
        else:
            if len(parziale)+(len(compRimaste)-indice) < self._dimPath:
                return
            for album in compRimaste[indice]:
                if album not in parziale:
                    parziale.append(album)
                    self.ricorsione(parziale, compRimaste, indice+1)
                    parziale.pop()
            self.ricorsione(parziale, compRimaste, indice + 1)


    def calcoloNumBrani(self, parziale):
        cont=0
        for a in parziale:
            cont+= len(a.ListaBrani)
        return cont