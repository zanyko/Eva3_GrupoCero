class Carrito:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"]={}
            self.carrito=self.session["carrito"]
        else:
            self.carrito=carrito

    def guardar(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True

    def agregar(self, producto):
        id=str(producto.idObra)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "producto_id":id,
                "nombre":producto.nombre,
                "cantidad":1,
                "total":producto.precio,
            }
        else:
            for key,value in self.carrito.items():
                if key==id:
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]=producto.precio
                    value["total"]=value["total"]+producto.precio
                    break
        self.guardar()
    
    def eliminar(self,producto):
        id = producto.idObra
        if id in self.carrito:
            del self.carrito[id]
            self.guardar()

    def restar(self, producto):
        for key, value in self.carrito.items():
            if key==producto.idObra:
                value["cantidad"]=value["cantidad"]-1
                value["total"]=int(value["total"])-producto.precio
                if value["cantidad"]<1:
                    self.eliminar(producto)
                break
        self.guardar()

    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified=True