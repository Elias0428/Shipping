#libreria de paises
import json
from pydoc import cli
import urllib.request
from django.http import JsonResponse
from django.shortcuts import render

# Standard Python libraries
import datetime

# Django utilities
from django.utils.timezone import make_aware

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

# Application-specific imports
from app.forms import *
from app.models import *
from .pdf import generatePdfInvoice

# Vista para crear cliente
@login_required(login_url='/login') 
def formCreateClient(request):

    if request.method == 'POST':

        date_births = request.POST.get('date_birth')
        fecha_obj = datetime.datetime.strptime(date_births, '%m/%d/%Y').date()

        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.agent = request.user
            client.is_active = 1
            client.date_birth = fecha_obj
            client.save()
         
            # Responder con éxito y la URL de redirección
            return redirect('formCreateShipping' ,client.id)
        else:
            return render(request, 'forms/formCreateClient.html', {'error_message': form.errors})
    
    return render(request, 'forms/formCreateClient.html')

@login_required(login_url='/login') 
def formCreateShipping(request, client_id):
    status = DropDownList.objects.filter(statusShipping__isnull=False)
    country = DropDownList.objects.filter(country__isnull=False)

    context = {
        'country':country,
        'status': status
    }

    if request.method == "POST":
        client = get_object_or_404(Clients, id=client_id)

        load = request.POST.getlist('load[]')
        type = request.POST.getlist('type[]')
        price = request.POST.getlist('price[]')
        description = request.POST.getlist('description[]')
        observationShipping = request.POST.get('observationShipping')
        country = request.POST.get('country')

        try:
            # Crear y guardar la observación
            shippingInstance = Shipping.objects.create(
                client=client,
                status='REGISTERED',
                status_date=timezone.now().date(),
                description=observationShipping,
                country = country
            )

            for load_item, type_item, price_item, desc_item in zip(load, type, price, description):  
                Packages.objects.create(
                    client=client,
                    agent=request.user,
                    shipping=shippingInstance,
                    load=load_item,
                    type=type_item,
                    price=price_item,
                    description=desc_item,
                )
            
            # Guardar el ID del envío en la sesión
            request.session['shipping_id_for_pdf'] = shippingInstance.id
            
            # Devolver respuesta con JSON 
            return JsonResponse({
                'success': True,
                'shipping_id': shippingInstance.id,
                'message': 'Envío registrado con éxito'
            })
            
        except Exception as e:
            if 'shippingInstance' in locals():
                shippingInstance.delete()       
            messages.error(request, "Ocurrió un error al guardar los paquetes. Por favor, inténtelo de nuevo.")
            print("Error al guardar los paquetes:", e)
            return JsonResponse({
                'success': False,
                'message': 'Ocurrió un error al guardar los paquetes'
            })
    
    return render(request, 'forms/formCreateShipping.html', context)

# Nueva función para solo generar el PDF (sin cambios)
def descargarPdf(request, shipping_id):
    shippingInstance = get_object_or_404(Shipping, id=shipping_id)
    client = shippingInstance.client
    packagesInstance = Packages.objects.filter(shipping=shippingInstance)
    
    return generatePdfInvoice(request, client, shippingInstance, packagesInstance)

