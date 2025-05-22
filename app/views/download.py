# Nueva función para solo generar el PDF (sin cambios)
from django.shortcuts import get_object_or_404
from app.models import *
from app.views.pdf import generatePdfInvoice
from django.http import HttpResponse

# Import Excel
import openpyxl


def descargarPdf(request, shipping_id):
    shippingInstance = get_object_or_404(Shipping, id=shipping_id)
    client = shippingInstance.client
    packagesInstance = Packages.objects.filter(shipping=shippingInstance)
    
    return generatePdfInvoice(request, client, shippingInstance, packagesInstance)

def exportShippingExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Shipping Data'

    startDatePost = request.POST['start_date']
    endDatePost = request.POST['end_date']
    status = request.POST['status']

    # Encabezados
    ws.append(['Full Name Client', 'Teléfono', 'Country','Status','Contend'])

    shipping = Shipping.objects.select_related('client').filter(created_at__range=[startDatePost, endDatePost])

    # Aplica filtro por status solo si fue enviado
    if status:
        shipping = shipping.filter(status=status)

    for item in shipping:
        package_descriptions = ", ".join([
            p.description for p in Packages.objects.filter(shipping=item,created_at__range=[startDatePost, endDatePost])
        ])

        ws.append([
            f"{item.client.first_name} {item.client.last_name}",
            item.client.phone_number,
            item.country,
            item.status,
            item.description,
            package_descriptions  # Esto contiene todas las descripciones separadas por coma
        ])


    # Preparar respuesta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = "shipping_data.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)

    return response