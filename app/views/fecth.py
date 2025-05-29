# Standard Python libraries
import json
import requests

# Django utilities
from django.http import JsonResponse

# Django core libraries
from django.views.decorators.csrf import csrf_exempt

# Application-specific imports
from app.models import *

def countDigits(numero):
  """
  Esta función toma un valor (esperando que sea un número o una cadena numérica)
  y devuelve la cantidad de dígitos que tiene.
  Maneja el caso en que la entrada sea una cadena.
  """
  try:
    # Intenta convertir la cadena a un entero
    numero_entero = int(numero)
    # Ahora podemos calcular el valor absoluto y luego la longitud de su representación en string
    return len(str(abs(numero_entero)))
  except (TypeError, ValueError):
    # Si la conversión a entero falla (no es una cadena numérica válida),
    # intentamos contar la longitud de la cadena original (si es una cadena)
    if isinstance(numero, str):
      return len(numero)
    else:
      # Si no es ni un número convertible a entero ni una cadena, devolvemos 0 o raise un error
      return 0  # O podrías hacer raise TypeError("Se esperaba un número o una cadena numérica.")

@csrf_exempt
def validatePhone(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    phoneNumber = data.get('phone_number')

    amount = countDigits(phoneNumber)

    if amount == 10:
      newNumber = int(f'1{phoneNumber}')
    else:
      newNumber = phoneNumber

    exists = Clients.objects.filter(phone_number=newNumber).exists()

    return JsonResponse({'exists': exists})
  
  return JsonResponse({'error': 'Invalid request'}, status=400)

def proxyZipcode(request, zipcode):
  try:
    response = requests.get(f"https://ziptasticapi.com/{zipcode}")
    response.raise_for_status()
    return JsonResponse(response.json())
  except requests.RequestException as e:
    return JsonResponse({'error': 'No se pudo obtener info'}, status=500)

