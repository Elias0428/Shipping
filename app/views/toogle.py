
# Django core libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

# Application-specific imports
from app.models import *

@login_required(login_url='/login')
def toggleUser(request, user_id):
    # Obtener el cliente por su ID
    user = get_object_or_404(Users, id=user_id)
    
    # Cambiar el estado de is_active (True a False o viceversa)
    user.is_active = not user.is_active
    user.save()  # Guardar los cambios en la base de datos
    
    # Redirigir de nuevo a la página actual con un parámetro de éxito
    return redirect('users')

