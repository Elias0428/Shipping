"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import index, auth, forms, fecth, tables, edit, sms, download, users, toogle

urlpatterns = [
    path('admin/', admin.site.urls),

    #<---------------------------Auth--------------------------->
    path('login/', auth.login_, name='login'),
    path('logout/', auth.logout_, name='logout'),

    #<---------------------------DashBoard--------------------------->
    path('', index.index, name='index'), #Home

    #<---------------------------Forms--------------------------->
    path('formCreateClient/', forms.formCreateClient, name='formCreateClient'),
    path('formCreateShipping/<client_id>/', forms.formCreateShipping, name='formCreateShipping'),

    #<---------------------------Fecth--------------------------->
    path('validatePhone/', fecth.validatePhone, name='validatePhone'),
    path('api/zipcode/<str:zipcode>/', fecth.proxyZipcode, name='proxyZipcode'),

    #<---------------------------Table--------------------------->
    path('tableNewShipment/', tables.tableNewShipment, name='tableNewShipment'),
    path('tableShipping/', tables.tableShipping, name='tableShipping'),

    #<---------------------------Edit--------------------------->
    path('editShipping/<shipping_id>/', edit.editShipping, name='editShipping'),

    #<---------------------------SMS--------------------------->
    path('sendMessage/<toPhone>/<messageContent>/', sms.sendMessage, name='sendMessage'),

    #<---------------------------Download--------------------------->
    path('shipping/export-excel/', download.exportShippingExcel, name='exportShippingExcel'),
    path('descargarPdf/<int:shipping_id>/', download.descargarPdf, name='descargarPdf'),

    #<---------------------------Users--------------------------->
    path('users/', users.formCreateUser, name='users'),
    path('editUser/<user_id>', users.editUser, name='editUser'),

    #<---------------------------Toggle--------------------------->
    path('toggleUser/<user_id>/', toogle.toggleUser, name='toggleUser'),

]
