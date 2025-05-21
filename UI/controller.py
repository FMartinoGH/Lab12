import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        anni = [2015,2016,2017,2018]
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view.ddyear.options = yearsDD
        #for a in anni:
            #self._view.ddyear.options.append(ft.dropdown.Option(key=a, text=str(a)))


        nazioni = self._model._countries
        countriesDD = list(map(lambda x: ft.dropdown.Option(str(x)), nazioni))
        self._view.ddcountry.options = countriesDD
        self._view.update_page()


    def handle_graph(self, e):
        self._model._graph.clear()
        print(self._view.ddcountry.value, self._view.ddyear.value)
        self._view.txt_result.controls.clear()
        if self._view.ddcountry.value == None or self._view.ddyear.value == None or (self._view.ddcountry.value and self._view.ddyear.value) == None:
            self._view.txt_result.controls.append(ft.Text("Scegliere i due campi."))
            self._view.update_page()
            return
        self._model.buildGraph(self._view.ddyear.value, self._view.ddcountry.value)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi"))
        self._view.update_page()



    def handle_volume(self, e):
        dict = self._model.getNodiConMaxPeso()
        for chiave, valore in dict.items():
            self._view.txt_result.controls.append(ft.Text(f"{chiave} --> {valore}"))
        self._view.update_page()



    def handle_path(self, e):
        pass
