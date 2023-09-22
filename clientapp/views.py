import base64

from django.shortcuts import render, redirect

from clientapp import static, consumers
from utils.combine_photo import combine_photo
from . import models


def index(request):
    return redirect('/startpage')


def startpage(request):
    consumers.end_thread()
    models.cut = models.Cut()

    models.cut.status = models.Status.START
    models.cut.save()
    print("StartPage;")
    return render(request, '1_startpage.html', {})


def background(request):
    consumers.start_thread()
    models.cut.paper_count = int(request.GET.get('people', 1))

    models.cut.status = models.Status.BG
    models.cut.save()
    print("Background; paper_count:", models.cut.paper_count)
    return render(request, '3_background.html', {})


# Disabled
def guide(request):
    return render(request, '4_guide.html', {})


def cam(request):
    models.cut.bg = int(request.GET.get('bg', 1))

    models.cut.status = models.Status.CAM
    models.cut.save()
    print("Cam; background:", models.cut.bg)
    return render(request, '5_cam.html', {})


# Disabled
def picturechoose(request):
    data = {}
    for i in range(6):
        data['img' + str(i+1)] = static.pics[i]
    # models.cut.status = models.Status.
    return render(request, 'picturechoose.html', data)


def framechoose(request):
    # static.sel = request.GET.get('select')
    consumers.end_thread()

    models.cut.status = models.Status.FRAME
    models.cut.save()
    print("FrameChoose;")
    return render(request, '6_framechoose.html', {})


def loading(request):
    models.cut.status = request.GET.get('frame', 'black')

    while len(models.cut.chromas) < 6:
        pass

    frame_path = "clientapp/static/images/2x3_" + models.cut.frame + ".png"
    result_path = "result.png"
    combine_photo(frame_path, models.cut.chromas, result_path)

    with open(result_path, 'rb') as f:
        img = f.read()
        img_str = base64.b64encode(img).decode('utf-8')

    models.cut.status = models.Status.LOAD
    models.cut.save()

    print("Loading; frame:", models.cut.status)
    return render(request, '7_loading.html', {
        "result": img_str
    })


def end(request):

    # combine_photo()

    return render(request, '8_end.html', {'code': static.code })


def wstest(request):
    return render(request, 'ws.html', {})


def ws2(request, room_name):
    return render(request, 'ws2.html', {})

