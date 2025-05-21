from model.model import Model

myModel = Model()
myModel.buildGraph(2015, "France")
cammino =(myModel.getCamminoChiusoMassimo(5))
print(myModel.stampaCammino(cammino))