import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._AlbumSelectedValue = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        self._model.buildGraph()
        grafo = self._model.getGraph()
        if len(grafo.nodes()) < 1:
            self._view._txt_result.controls.append(
                ft.Text(f"Grafo vuoto o creato in modo errato", color="red")
            )
            self._view.update_page()
            return
        self._view._txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges = self._model.detailGraph()
        self._view._txt_result.controls.append(
            ft.Text(f"Numero nodi: {numNodes}")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero archi: {numEdges}")
        )
        allAlbum = self._model.getAlbumDD()
        for o in allAlbum:
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(data=o,
                                   text=o.Title,
                                   key=o.AlbumId,
                                   on_click=self.choiceAlbum)
            )
        self._view.update_page()

    def choiceAlbum(self, e):
        self._AlbumSelectedValue = e.control.data
        return self._AlbumSelectedValue


    def handleStampaInfo(self,e):
            self._view._txt_result.controls.clear()
            numConnComp = self._model.numConnComponent()
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di componenti connesse del grafo: {numConnComp}")
            )
            maxComp= self._model.maxConnComponent()
            self._view._txt_result.controls.append(
                ft.Text(f"Dimensione della componente connessa più grande: {len(maxComp)} album")
            )
            self._view._txt_result.controls.append(
                ft.Text("Dettagli degli album appartenenti alla componente connessa più grande:", color="green")
            )
            maxCompOrd= list(maxComp)
            maxCompOrd.sort(key=lambda a:a.Title)
            for a in maxCompOrd:
                self._view._txt_result.controls.append(
                    ft.Text(f"- {a} brani")
                )
            self._view.update_page()

    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()
        nodoInizio = self._AlbumSelectedValue
        if self._view._ddAlbum.value is None:
            self._view.create_alert("Scegliere nodo di partenza!!")
            return
        dim = self._view._txtInN.value
        if dim == "":
            self._view.create_alert("Inserire valore nel text field!!")
            return
        try:
            dimInt = int(dim)
        except ValueError:
            self._view.create_alert("Inserire un valore intero!!")
            return
        if dimInt < 0:
            self._view.create_alert("Inserire un valore positivo!!")
            return
        bestPath, numBrani= self._model.getPath(nodoInizio, dimInt)
        if len(bestPath) == 0:
            self._view.txt_result.controls.append(
                ft.Text("nessun cammino esistente con questi input", color="red")
            )
            self._view.update_page()
            return
        self._view._txt_result.controls.append(
            ft.Text(f"Cammino trovato: ", color="green")
        )
        numAlbum= len(bestPath)
        bestPath.sort(key=lambda a: a.Title)
        for n in bestPath:
            self._view._txt_result.controls.append(
                ft.Text(f"{n} - ({n.AlbumId})")
            )
        self._view._txt_result.controls.append(
            ft.Text(f"Il numero di album nell'insieme ottenuto: {numAlbum} ")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Il numero complessivo di brani dell'insieme: {numBrani} ")
        )
        self._view.update_page()