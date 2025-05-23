# Standard Python libraries
from django.http import JsonResponse, HttpResponse

# Django core libraries
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect, render

# Application-specific imports
from app.models import *

@login_required(login_url='/login') 
def formCreateUser(request):

    users = Users.objects.exclude(is_superuser = True)
    roles = Users.ROLES_CHOICES  # Obtén las opciones dinámicamente desde el modelo

    if request.method == 'POST':
        first_name = request.POST.get('first_name').upper()
        last_name = request.POST.get('last_name').upper()
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        try:
            # Validar si el username ya existe
            if Users.objects.filter(username=username).exists():
                return render(request, 'users/users.html', {'msg':f'El nombre de usuario "{username}" ya está en uso.','users':users, 'type':'error'})

            # Crear el usuario si no existe el username
            user = Users.objects.create(
                username=username,
                password=make_password(password),  # Encriptar la contraseña
                last_name=last_name,
                first_name=first_name,
                role=role
            )

            context = {
                'msg':f'Usuario {user.username} creado con éxito.',
                'users':users,
                'type':'good',
                'roles': roles,
            }

            return render(request, 'users/users.html', context)

        except Exception as e:
            return HttpResponse(str(e))
        
    context = {
            'users':users,
            'roles': roles,
        }
            
    return render(request, 'users/users.html', context)

@login_required(login_url='/login') 
def editUser(request, user_id):
    # Obtener el usuario a editar o devolver un 404 si no existe
    user = Users.objects.filter(id=user_id).first()


    if request.method == 'POST':
        # Recuperar los datos del formulario
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        username = request.POST.get('username', user.username)
        role = request.POST.get('role', user.role)
        is_active = request.POST.get('is_active', user.is_active)

        # Verificar si el nuevo username ya existe en otro usuario
        if username != user.username and Users.objects.filter(username=username).exists():
            return JsonResponse({'error': f'El nombre de usuario "{username}" ya está en uso.'}, status=400)

        # Actualizar los datos del usuario
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.role = role
        user.is_active = is_active

        # Guardar los cambios
        user.save()

        # Redirigir a otra vista o mostrar un mensaje de éxito
        return redirect('users')  

    # Renderizar el formulario con los datos actuales del usuario
    context = {'users': user}
    return render(request, 'users/editUser.html', context)

