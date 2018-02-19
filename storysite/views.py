from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

def homepage(request):
	return render(request, 'homepage.html', {})

def admin(request):
    context = {}

    if request.user.is_authenticated:
        context['authenticated'] = True
        return render(request, 'admin.html', context)

    elif request.POST:
        adminname = request.POST['admin-name']
        adminpass = request.POST['admin-pass']
        user = authenticate(username=adminname, password=adminpass)
        context['adminname'] = adminname
        context['adminpass'] = adminpass
        if user is not None:
            context['authenticated'] = True
        else:
            context['authenticated'] = False

        return render(request, 'admin.html', context)
    
    else:
        return render(request, 'admin.html', {})
