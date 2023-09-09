import base64

from django.shortcuts import render, redirect

from clientapp import static, consumers
from utils.combine_photo import combine_photo


def index(request):
    return redirect('/startpage')


def startpage(request):
    return render(request, '1_startpage.html', {})


def background(request):
    consumers.start_thread()
    return render(request, '3_background.html', {})


def guide(request):
    return render(request, '4_guide.html', {})


def cam(request):
    static.bg = int(request.GET.get('bg', 1))
    with open('img_' + static.code + 'bg' + str(static.bg), 'w' ) as f:
        f.write('1')
    static.pics = []
    return render(request, '5_cam.html', {})


def picturechoose(request):
    data = {}
    for i in range(6):
        data['img' + str(i+1)] = static.pics[i]
    return render(request, 'picturechoose.html', data)


def framechoose(request):
    static.sel = request.GET.get('select')
    return render(request, '6_framechoose.html', {})


def loading(request):
    static.frame = request.GET.get('frame', 'black')

    with open('img_' + static.code + static.frame, 'w') as f:
        f.write('1')

    frame_path = "clientapp/static/images/2x3_" + static.frame + ".png"
    result_path = "result.png"
    combine_photo(frame_path, static.pics, result_path)

    with open(result_path, 'rb') as f:
        img = f.read()
        img_str = base64.b64encode(img).decode('utf-8')

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

