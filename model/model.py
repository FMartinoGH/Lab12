import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._countries = DAO.getAllCountries()
        self._archiSort = sorted(self._graph.edges, key=lambda x: x[2]['weight'], reverse=True)




    def buildGraph(self, anno, nazione):
        self._nodes = DAO.getAllNodes(nazione)
        self._graph.add_nodes_from(self._nodes)
        for v in self._graph.nodes:
            self._idMap[v.Retailer_code] = v
        self.addEdges(anno, nazione)

    def addEdges(self, anno, nazione):
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u != v:
                    if not (self._graph.has_edge(u, v)):
                        valore = DAO.getAllEdges(anno, nazione, u, v)
                        if valore > 0:
                            self._graph.add_edge(u, v, weight=valore)

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())

    def getConnessa(self):
        return nx.connected_components(self._graph)

    def getVicini(self, cod):
        vicini = {}
        nodoscelto = self._idMap[cod]
        for u, v, data in self._graph.edges(data=True):
            if u == nodoscelto:
                vicini[v] = data["weight"]
            elif v == nodoscelto:
                vicini[u] = data["weight"]
        return vicini

    """
    il tuo metodo getVicini considera solo gli archi in cui u == nodoscelto, 
    ma non quelli in cui v == nodoscelto, 
    il che è un errore se il grafo è non orientato 
    (cioè, le connessioni valgono in entrambi i sensi).
    """

    def getTotale(self, cod):
        totale = 0
        nodoscelto = self._idMap[cod]
        for u, v, data in self._graph.edges(data=True):
            if u == nodoscelto:
                totale += data["weight"]
            elif v == nodoscelto:
                totale += data["weight"]
        return totale

    def getAllEdges(self):
        archi_ordinati = sorted(
            self._graph.edges(data=True),
            key=lambda e: e[2]["weight"], reverse=True
        )
        return archi_ordinati


    def getNodiConMaxPeso(self):
        result = {}
        for u in self._graph.nodes():
            valore = self.getTotale(u.Retailer_code)
            result[u] = valore

        ordinato = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        return ordinato

    def getAllWeights(self):
        str1 = ""
        for u, v, data in self._graph.edges(data=True):
            str1 += str(u.Retailer_code) + ", " + str(v.Retailer_code) + ", " + str(data["weight"]) + "\n"
        return str1

    def getIsolati(self):
        isolati = [n for n in self._graph.nodes() if self._graph.degree(n) == 0]
        print("Nodi isolati:", isolati)

    def getAllEdgesXCOD(self, cod):
        str1 = ""
        for u, v, data in self._graph.edges(data=True):
            if u.Retailer_code == cod or v.Retailer_code == cod:
                str1 += str(u.Retailer_code) + ", " + str(v.Retailer_code) + ", " + str(data["weight"]) + "\n"
        if str1 == "":
            return "Vuota"
        return str1

    def getCamminoChiusoMassimo(self, N):
        if N < 2:
            return None, 0  # N deve essere almeno 2

        self._bestCycle = []
        self._bestWeight = 0

        for start in self._graph.nodes: #devo fare la ricorsione su ogni nodo di partenza
            self._ricorsione([start], 0, N, start)

        return self._bestCycle#, self._bestWeight

    def _ricorsione(self, cammino, peso_parziale, N, start):
        current = cammino[-1]


        if len(cammino) == N + 1:
            if current == start and peso_parziale > self._bestWeight:
                self._bestCycle = copy.deepcopy(cammino)
                self._bestWeight = peso_parziale
            return

        for neighbor in self._graph.neighbors(current):
            if neighbor == start and len(cammino) == N:
                edge_weight = self._graph[current][neighbor]['weight']
                self._ricorsione(cammino + [neighbor], peso_parziale + edge_weight, N, start)
            elif neighbor not in cammino:
                edge_weight = self._graph[current][neighbor]['weight']
                cammino.append(neighbor)
                self._ricorsione(cammino, peso_parziale + edge_weight, N, start)
                cammino.pop()

    def stampaCammino(self, cammino):
        if not cammino:
            print("Nessun ciclo trovato.")
            return

        print("Cammino di peso massimo trovato:")
        for i in range(len(cammino) - 1):
            u = cammino[i]
            v = cammino[i + 1]
            peso = self._graph[u][v]['weight']
            print(f"{u} —> {v} : {peso}")




