import base64

from django.shortcuts import render, redirect

from clientapp import static, consumers
from main import settings
from main.settings import conf
from utils import send_print, make_video
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

    if not conf['chroma']:
        return redirect('/cam?bg=1')

    models.cut.status = models.Status.BG
    models.cut.save()
    print("Background; paper_count:", models.cut.paper_count)
    return render(request, '3_background.html', {})


# Disabled
def guide(request):
    return render(request, '4_guide.html', {})


def cam(request):
    models.cut.bg = int(request.GET.get('bg', 1))
    make_video.clear_frames()

    models.cut.status = models.Status.CAM
    models.cut.save()
    print("Cam; background:", models.cut.bg)
    return render(request, '5_cam.html', {})


# Disabled
def picturechoose(request):
    data = {}
    for i in range(6):
        data['img' + str(i + 1)] = static.pics[i]
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
    models.cut.frame = request.GET.get('frame', 'black')

    # consumers.start_loading_thread()
    models.cut.status = models.Status.LOAD
    models.cut.save()
    print("Loading; frame:", models.cut.frame)
    return render(request, '7_loading.html', {
        # "result": img_str
    })


def end(request):
    # combine_photo()

    # reopen photo to send to client
    result_path = str(models.cut.storage() / "result.png")  # should be synced by 'consumers.py / manage_loading() / combine photo'
    with open(result_path, 'rb') as f:
        img = f.read()
        img_str = base64.b64encode(img).decode('utf-8')

    models.cut.status = models.Status.LOAD
    models.cut.save()
    print("Loading; frame:", models.cut.frame)
    return render(request, '8_end.html', {'img_str': img_str})


def wstest(request):
    return render(request, 'ws.html', {})


def ws2(request, room_name):
    return render(request, 'ws2.html', {})


def test(request, name):
    return render(request, name, {})
