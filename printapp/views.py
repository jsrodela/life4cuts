import base64
import json
import threading

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import consumers


@csrf_exempt
def send_print(request):
    try:
        img = request.POST.get('img')
        cnt = request.POST.get('cnt')
        code = request.POST.get('code')  # jamsin.tk video code

        consumers.broadcast_photo(img, cnt, code)

        return HttpResponse(json.dumps({
            'status': 'success'
        }))

    except Exception as ex:
        return HttpResponse(json.dumps({
            'status': 'fail',
            'error': ex
        }))
        
# thread code moved to printapp/print_websocket.py

