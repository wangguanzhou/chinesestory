from django.shortcuts import render 
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect 
from django.conf import settings 
from datetime import datetime 
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
    active_notices = {}

    active_notices['Brossard'] = get_active_notice('Brossard')
    if len(active_notices['Brossard']) > 0:
        active_notices['Active_Brossard'] = True

    active_notices['Longueuil'] = get_active_notice('Longueuil')
    if len(active_notices['Longueuil']) > 0:
        active_notices['Active_Longueuil'] = True

    active_notices['CDN'] = get_active_notice('CDN')
    if len(active_notices['CDN']) > 0:
        active_notices['Active_CDN'] = True

    active_notices['Montreal'] = get_active_notice('Montreal')
    if len(active_notices['Montreal']) > 0:
        active_notices['Active_Montreal'] = True

    return render(request, 'homepage.html', {'active_notices': active_notices})

def adminlogin(request):
    context = {}

    if request.user.is_authenticated:
        admin_name = request.user.username
        district_name = DistrictNames[admin_name]
        context['district_name'] = district_name
        active_notice = get_active_notice(district_name)
        if len(active_notice) > 0:
            context['active_notice_exist'] = True
            context['active_notice_num'] = len(active_notice)
            context['active_notice'] = active_notice
        else:
            context['active_notice_exist'] = False

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


def shownotice(request):

    return render(request, 'notice.html', {})

@login_required(login_url='/chinesestory/admin/')
def createnotice(request):
    context = {}
    admin_name = request.user.username
    district_name = DistrictNames[admin_name]
    context['district_name'] = district_name

    if request.POST:
        notice_form = NoticeForm(request.POST)
        if notice_form.is_valid():
            notice_data = notice_form.cleaned_data
            save_notice_file(district_name, notice_data)
            active_notice = get_active_notice(district_name)
            if len(active_notice) > 0:
                context['active_notice_exist'] = True
                context['active_notice'] = active_notice
            return render(request, 'admin.html', context)
        else:
            return render(request, 'admin.html', {})

    else:
        notice_form = NoticeForm()
        # setting default notice data
        notice_form.fields['story_size'].initial = 20
        notice_form.fields['story_venue'].initial = StoryVenues[district_name]
        notice_form.fields['story_address'].initial = StoryAddresses[district_name]
        notice_form.fields['story_activity_1'].initial = 'ni hao ge'
        context['notice_form'] = notice_form
        return render(request, 'createnotice.html', context)

@login_required(login_url='/chinesestory/admin/')
def modifynotice(request):
    context = {}
    if request.GET:
        district_name = request.GET['district']
        story_date = request.GET['date']
        notice_file = district_name + '-' + story_date + '.json'
        notice_data = read_notice_file(notice_file)

        notice_form = NoticeForm()
        notice_form.fields['story_theme'].initial = notice_data['story_theme']
        notice_form.fields['story_date'].initial = datetime.strptime(notice_data['story_date'], '%Y-%m-%d')
        notice_form.fields['story_time'].initial = datetime.strptime(notice_data['story_time'], '%I:%M %p')
        notice_form.fields['story_host'].initial = notice_data['story_host']
        notice_form.fields['story_size'].initial = notice_data['story_size']
        notice_form.fields['story_venue'].initial = notice_data['story_venue']
        notice_form.fields['story_address'].initial = notice_data['story_address']
        notice_form.fields['reg_date'].initial = datetime.strptime(notice_data['reg_date'], '%Y-%m-%d')
        notice_form.fields['reg_time'].initial = datetime.strptime(notice_data['reg_time'], '%I:%M %p')
 
        context['notice_form'] = notice_form
        return render(request, 'createnotice.html', context)
    else:
        admin_name = request.user.username
        district_name = DistrictNames[admin_name]
        context['district_name'] = district_name
        active_notice = get_active_notice(district_name)
        if len(active_notice) > 0:
            context['active_notice_exist'] = True
            context['active_notice'] = active_notice
        return render(request, 'admin.html', context)
 

@login_required(login_url='/chinesestory/admin/')
def deletenotice(request):
    context = {}
    if request.GET:
        district_name = request.GET['district']
        story_date = request.GET['date']

        notice_file = district_name + '-' + story_date + '.json'
        delete_notice_file(notice_file)
        
    admin_name = request.user.username
    district_name = DistrictNames[admin_name]
    context['district_name'] = district_name
    active_notice = get_active_notice(district_name)
    if len(active_notice) > 0:
        context['active_notice_exist'] = True
        context['active_notice'] = active_notice
    return render(request, 'admin.html', context)
 


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
    notice_file_path = os.path.join(settings.BASE_DIR, 'static/noticefiles/')
    try:
        with open(notice_file_path + filename, 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
        return json_data
    except:
        print('Error reading notice file.')

def delete_notice_file(filename):
    notice_file_path = os.path.join(settings.BASE_DIR, 'static/noticefiles/')
    try:
        os.remove(notice_file_path + filename)
    except:
        print('Error deleting notice file.')
 
def get_active_notice(district):
    notice_file_path = os.path.join(settings.BASE_DIR, 'static/noticefiles/')
    active_notice = []
    for notice_file in os.listdir(notice_file_path):
        if notice_file.endswith('.json'):
            notice_data = read_notice_file(notice_file)
            story_datetime = notice_data['story_date'] + ' ' + notice_data['story_time']
            if district == notice_data['district_name'] and datetime.strptime(story_datetime, '%Y-%m-%d %I:%M %p') > datetime.now():
                active_notice.append({'story_date': notice_data['story_date'], 'story_theme': notice_data['story_theme'], 'story_host': notice_data['story_host']})

    return active_notice
