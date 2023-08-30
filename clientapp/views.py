from django.shortcuts import render, redirect


def index(request):
    return redirect('/startpage')


def startpage(request):
    return render(request, '1_startpage.html', {})


def background(request):
    return render(request, '3_background.html', {})


def guide(request):
    return render(request, '4_guide.html', {})


def cam(request):
    return render(request, '5_cam.html', {})


def picturechoose(request):
    return render(request, '2_picturechoose.html', {})


def framechoose(request):
    return render(request, '6_framechoose.html', {})
