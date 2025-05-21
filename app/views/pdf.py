# Standard Python libraries
from datetime import timedelta, datetime

# Django utilities
from django.http import HttpResponse
from django.template.loader import render_to_string

# Third-party libraries
from weasyprint import HTML

# Application-specific imports
from app.models import *


def generatePdfInvoice(request, client, shippingInstance, packagesInstance):

    id_invoice = f"{shippingInstance.id:08d}"
    packagesInstance = Packages.objects.filter(shipping = shippingInstance)

    total = []
    amount = 0

    for item in packagesInstance:
        value = item.load * item.price
        total.append(value)
        amount = amount + value

    combined = zip(packagesInstance, total)

    context = {
        'client':client, 
        'id_invoice': id_invoice,
        'shippingInstance': shippingInstance,
        'combined' : combined,
        'amount' : amount
    }

    # Renderiza la plantilla HTML a un string
    html_content = render_to_string('templatesPdf/invoice.html', context)

    # Genera el PDF
    pdf_file = HTML(string=html_content).write_pdf()

    # Guarda el PDF en el modelo usando un ContentFile
    pdf_name = f'Client {client.first_name} {client.last_name} #Invoice{id_invoice} {datetime.now().strftime("%m-%d-%Y-%H:%M")}.pdf'  # Nombre del archivo

    # Crea una respuesta HTTP con el PDF para descarga
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'

    return response

