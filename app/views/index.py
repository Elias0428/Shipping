# Standard Python libraries
import calendar
from datetime import datetime
import json

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render

# Application-specific imports
from app.models import *
from django.shortcuts import render, redirect

@login_required(login_url='/login') 
def index(request):

    statusShipping = Shipping.objects.values('status').annotate(count=Count('status'))

    for i in statusShipping:
        print(i['status'], 'soy el status - soy el count', i['count'])


    context = {
        'statusShipping' : statusShipping
    }      

    return render(request, 'dashboard/index.html', context)
