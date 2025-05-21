# Standard Python libraries
import datetime

#libreria de paises
from django.shortcuts import render

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Application-specific imports
from app.models import *
from .sms import *

@login_required(login_url='/login') 
def editShipping(request, shipping_id):
    
    packages = Packages.objects.filter(shipping=shipping_id) 
    client = Shipping.objects.select_related('client').filter(id=shipping_id).first() 
    status = DropDownList.objects.filter(statusShipping__isnull=False)
    country = DropDownList.objects.filter(country__isnull=False)

    if request.method == 'POST':

        id = request.POST.getlist('id[]')
        load = request.POST.getlist('load[]')
        type = request.POST.getlist('type[]')
        price = request.POST.getlist('price[]')
        description = request.POST.getlist('description[]')
        observation = request.POST.get('observation')
        statusShipping = request.POST.get('statusShipping')
        country = request.POST.get('country')


        if client.status != statusShipping:

            # Crear y guardar la observación
            shippingInstance = Shipping.objects.filter(id = shipping_id).update(
                status=statusShipping,
                status_date=timezone.now().date(),
                description=observation,
                country = country
            )
            messageContent = f"Tu pedido se encuentra en el siguiente status '{statusShipping}', cualquier cambio se le estara notificando, 'NO REPLY SMS AUTOMATIC**'"
            sendMessage(request, client.client.phone_number, messageContent )
        else:
            # Crear y guardar la observación
            shippingInstance = Shipping.objects.filter(id = shipping_id).update(
                description=observation,
                country = country
            )

        for id_item, load_item, type_item, price_item, desc_item in zip(id, load, type, price, description):  
            Packages.objects.filter(id=id_item).update(
                load=load_item,
                type=type_item,
                price=price_item,
                description=desc_item,
            )          
       
        return redirect('tableShipping')         

    context = {
        'packages': packages,
        'client' : client,
        'status' : status,
        'country' : country
    }

    return render(request, 'edit/editShipping.html', context)
