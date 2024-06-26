def total_carrito(request):
    total=0
    if request.user in request.session:
        try:
            if "carrito" in request.session.keys():
                for key, value in request.session["carrito"].items():
                    total+=(int(value["precio"]))*(value["cantidad"])
        except:
            request.session['carrito']={}
            total=0
    return {'total_carrito':int(total)}