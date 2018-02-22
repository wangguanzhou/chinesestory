from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

DistrictNames = {
    'bsdadmin': 'Brossard',
    'logadmin': 'Longueuil',
    'mtladmin': 'Montreal',
    'cdnadmin': 'CDN',
}

StoryPlaces = { 
    'Brossard': 'Bibliothèque de Brossard (Brossard图书馆儿童活动区)',
    'Longueuil': 'Bibliothèque Georges-Dor',
    'CDN': 'CDN图书馆儿童活动室（地下一层）',
    'Montreal': 'Montreal library'
}

StoryAddresses = { 
    'Brossard': '7855 Ave San Francisco, Brossard J4X 2A4',
    'Longueuil': '2760 chemin de Chambly, Longueuil J4L 1M6',
    'CDN': '5290 Chemin de la Côté-des-Neiges, Montréal H3T 1Y3',
    'Montreal': '5290 Chemin de la Côté-des-Neiges, Montréal H3T 1Y3',
}

def homepage(request):
    return render(request, 'homepage.html', {})

def adminlogin(request):
    context = {}

    if request.user.is_authenticated:
        context['authenticated'] = True
        admin_name = request.user.usename
        context['district_name'] = DistrictNames[admin_name]
        return render(request, 'admin.html', context)

    elif request.POST:
        admin_name = request.POST['admin-name']
        admin_pass = request.POST['admin-pass']
        user = authenticate(username=admin_name, password=admin_pass)
        if user is not None:
            context['authenticated'] = True
            context['district_name'] = DistrictNames[admin_name]
        else:
            context['authenticated'] = False
            context['login_error'] = True

        return render(request, 'admin.html', context)

    else:
        return render(request, 'admin.html', {})


def adminlogout(request):
    logout(request)
    return redirect('/chinesestory/admin/')


# @login_required(login_url='/chinesestory/admin/')
def createnotice(request):
    context = {}
    district_name = 'Brossard'
    default_notice = set_default_notice(district_name)
    context['notice_data'] = default_notice
    return render(request, 'createnotice.html', context)


def set_default_notice(district_name):
    default_notice = {}

    if district_name not in ['Brossard', 'Longueuil', 'Montreal', 'CDN']:
        return default_notice

    default_notice['story_maxsize'] = 20
    default_notice['story_place'] = StoryPlaces[district_name]
    default_notice['story_address'] = StoryAddresses[district_name]
    default_notice['story_activity_1'] = 'ni hao ge'


    return default_notice


