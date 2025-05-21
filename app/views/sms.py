# Standard Python libraries
import logging

# Django utilities
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Third-party imports
import telnyx

# Application-specific imports
from app.modelsSMS import *
from ..alertWebsocket import websocketAlertGeneric

# Create your views here.
logger = logging.getLogger('django')

@csrf_exempt
def sendMessage(request, toPhone, messageContent):

    telnyx.api_key = settings.TELNYX_API_KEY
    telnyx.Message.create(
        from_=f"+{request.user.assigned_phone.phone_number}", # Your Telnyx number
        to=f'+{toPhone}',
        text= messageContent
    )

    message = Messages(
        message_content=messageContent,
    )
    message.save()
    
    return JsonResponse({'message':'ok'})


