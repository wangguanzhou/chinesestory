from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from datetime import datetime, date
import json
import os.path
from .forms import NoticeForm

DistrictNames = {
    'bsdadmin': 'Brossard',
    'logadmin': 'Longueuil',
    'mtladmin': 'Montreal',
    'cdnadmin': 'CDN',
}

StoryVenues = { 
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
        admin_name = request.user.username
        context['district_name'] = DistrictNames[admin_name]
        return render(request, 'admin.html', context)

    elif request.POST:
        admin_name = request.POST['admin-name']
        admin_pass = request.POST['admin-pass']
        user = authenticate(username=admin_name, password=admin_pass)
        if user is not None:
            context['authenticated'] = True
            context['district_name'] = DistrictNames[admin_name]
            login(request, user)
        else:
            context['authenticated'] = False
            context['login_error'] = True

        return render(request, 'admin.html', context)

    else:
        return render(request, 'admin.html', {})


def adminlogout(request):
    logout(request)
    return redirect('/chinesestory/admin/')


@login_required(login_url='/chinesestory/admin/')
def createnotice(request):
    context = {}
    district_name = 'Brossard'

    if request.POST:
        notice_form = NoticeForm(request.POST)
        if notice_form.is_valid():
            notice_data = notice_form.cleaned_data
            save_notice_file(district_name, notice_data)
            return render(request, 'base.html', {'notice_form': notice_form})
        else:
            return render(request, 'base.html', {'notice_form': notice_form})

    else:
        notice_form = NoticeForm()
        # setting default notice data
        notice_form.fields['story_size'].initial = 20
        notice_form.fields['story_venue'].initial = StoryVenues[district_name]
        notice_form.fields['story_address'].initial = StoryAddresses[district_name]
        notice_form.fields['story_activity_1'].initial = 'ni hao ge'
        context['notice_form'] = notice_form
        return render(request, 'createnotice.html', context)


def save_notice_file(district_name, notice_data):
    json_data = {}
    notice_file_path = os.path.join(settings.BASE_DIR, 'static/noticefiles/')
    story_date = notice_data['story_date'].strftime('%Y-%m-%d')
    filename = notice_file_path + district_name + '-' + story_date + '.json' 
    json_data['district_name'] = district_name
    json_data['story_theme'] = notice_data['story_theme']
    json_data['story_date'] = notice_data['story_date'].strftime('%Y-%m-%d')
    json_data['story_time'] = notice_data['story_time'].strftime('%I:%M %p')
    json_data['story_host'] = notice_data['story_host']
    json_data['story_size'] = notice_data['story_size']
    json_data['story_venue'] = notice_data['story_venue']
    json_data['story_address'] = notice_data['story_address']
    json_data['reg_date'] = notice_data['reg_date'].strftime('%Y-%m-%d')
    json_data['reg_time'] = notice_data['reg_time'].strftime('%I:%M %p')
    json_data['story_activity_1'] = notice_data['story_activity_1']
    json_data['story_activity_2'] = notice_data['story_activity_2']
    json_data['story_activity_3'] = notice_data['story_activity_3']
    json_data['story_activity_4'] = notice_data['story_activity_4']
    json_data['story_activity_5'] = notice_data['story_activity_5']

    try:
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file)
            json_file.close()
    except:
        print('Error writing JSON file.')

def read_notice_file(filename):
    notife_file_path = os.path.join(settings.BASE_DIR, 'static/notiefiles/')
    try:
        with open(notice_file_path + filename, 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
            return json_data
    except:
        print('Error reading JSON file.')
            
