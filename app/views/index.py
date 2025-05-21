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



    context = {

    }      

    return render(request, 'dashboard/index.html', context)
