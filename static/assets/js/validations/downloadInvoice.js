// shipping-form-handler.js

document.addEventListener('DOMContentLoaded', function() {
    // Iframe oculto para descargas
    var iframe = document.createElement('iframe');
    iframe.id = 'pdfDownloader';
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    
    // Interceptar el envío del formulario
    var formShipping = document.getElementById('formShipping');
    if (formShipping) {
        formShipping.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Obtener datos del formulario
            var formData = new FormData(formShipping);
            var formEntries = new URLSearchParams(formData).toString();
            
            // Obtener URL de redirección y guardarla (será usada por el AJAX)
            var redirectUrl = formShipping.getAttribute('data-redirect-url');
            
            // Realizar solicitud AJAX
            fetch(formShipping.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formEntries
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Construir URL para PDF
                    var pdfUrl = '/descargarPdf/' + data.shipping_id + '/';
                    
                    // Mostrar SweetAlert2 de éxito
                    Swal.fire({
                        title: '¡Éxito!',
                        text: 'El envío ha sido registrado correctamente. Se iniciará la descarga del PDF.',
                        icon: 'success',
                        timer: 3000,
                        timerProgressBar: true,
                        showConfirmButton: true,
                        confirmButtonText: 'Descargar PDF',
                        willClose: function() {
                            // Redireccionar cuando se cierra la alerta
                            window.location.href = redirectUrl;
                        }
                    }).then((result) => {
                        // Si se cierra con el botón de confirmación, no redirigir (ya se manejará)
                        if (result.isConfirmed) {
                            // La descarga se inicia con el clic del botón
                            window.location.href = pdfUrl;
                            
                            // Esperar un momento y luego redirigir
                            setTimeout(function() {
                                window.location.href = redirectUrl;
                            }, 1000);
                        }
                    });
                    
                    // Iniciar descarga usando iframe
                    document.getElementById('pdfDownloader').src = pdfUrl;
                } else {
                    // Mostrar SweetAlert2 de error
                    Swal.fire({
                        title: 'Error',
                        text: data.message,
                        icon: 'error',
                        confirmButtonText: 'Aceptar'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Ha ocurrido un error al procesar la solicitud',
                    icon: 'error',
                    confirmButtonText: 'Aceptar'
                });
            });
        });
    }
    
    // Función auxiliar para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});