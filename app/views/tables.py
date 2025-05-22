#libreria de paises
import json
import urllib.request
from django.http import JsonResponse
from django.shortcuts import render

# Django core libraries
from django.contrib.auth.decorators import login_required

# Application-specific imports
from app.forms import *
from app.models import *


@login_required(login_url='/login') 
def tableNewShipment(request):

    clients = Clients.objects.filter(is_active=1).order_by('id')

    return render(request, 'tables/tableNewShipment.html', { 'clients': clients})

@login_required(login_url='/login') 
def tableShipping(request):

    shipping = Shipping.objects.order_by('id')
    status = DropDownList.objects.filter(statusShipping__isnull=False)

    context = {
        'shipping': shipping,
        'status' : status
    }

    return render(request, 'tables/tableShipping.html', context)



