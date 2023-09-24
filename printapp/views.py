import json
import threading

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from utils import printer
from .models import PrintModel


@csrf_exempt
def send_print(request):
    try:
        img = request.FILES.get('img')
        cnt = request.POST.get('cnt')
        code = request.POST.get('code')  # jamsin.tk video code

        model = PrintModel()
        model.img = img
        model.cnt = cnt
        model.code = code
        model.save()

        add_print(model)

        return HttpResponse(json.dumps({
            'status': 'success'
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            'status': 'fail',
            'error': ex
        }))


print_list = []
run_thread = False
thread = None


def run_print():
    global run_thread, print_list, thread
    run_thread = True
    while len(print_list):
        model: PrintModel = print_list.pop(0)
        printer.print_file(model.img.path, model.cnt)
    run_thread = False
    thread = None


def add_print(model: PrintModel):
    global thread
    print_list.append(model)
    if not run_thread:
        if thread is not None:
            thread.join()
        thread = threading.Thread(target=run_print, daemon=True)
        thread.start()
