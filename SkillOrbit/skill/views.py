from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserSkillForm,SkillRequestForm
from django.contrib.auth.decorators import login_required
from .models import UserSkill,SkillRequest,Connection
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.

#Skills

@login_required(login_url='signin')
def add_skills(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            selected_skill = form.cleaned_data.get('skill')
            if UserSkill.objects.filter(user=request.user, skill=selected_skill).exists():
                messages.error(request, 'This skill is already in your portfolio.')
                return render(request, 'skill/add_skill.html', {'form': form})
            new_skill = form.save(commit=False)
            new_skill.user = request.user
            new_skill.save()
            return redirect('profile')
    else:
        form = UserSkillForm()

    return render(request, 'skill/add_skill.html', {'form': form})

@login_required(login_url="signin")
def delete_skills(request, sid):
    userskill = get_object_or_404(UserSkill,id=sid,user=request.user,)
    userskill.delete()
    return redirect("profile")

@login_required(login_url='signup')
def edit_skills(request, sid):
    userskill = get_object_or_404(UserSkill, id = sid , user = request.user)
    if request.method =='POST':
        form = UserSkillForm(request.POST, instance=userskill)
        if form.is_valid():
            selected_skill = form.cleaned_data.get('skill')
            if UserSkill.objects.filter(user=request.user, skill=selected_skill).exists():
                messages.error(request, 'This skill is already in your portfolio.')
                return render(request, 'skill/add_skill.html', {'form': form})
            form.save()
            return redirect('profile')
    else:
        form = UserSkillForm(instance=userskill)
    return render(request, 'skill/edit_skill.html', {'form':form})
    
@login_required(login_url='signin')
def skill_request(request):
    User = get_user_model()
    user_id = request.GET.get('user_id')
    reciever_user = get_object_or_404(User, id = user_id)
    form = SkillRequestForm()
    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            skill_request=form.save(commit=False)
            skill_request.from_user = request.user
            skill_request.to_user = reciever_user
            skill_request.save()
            return redirect('public_profile', pp_id= reciever_user.id)
    context = {
        'form': form,
        'user_id': user_id
    }
    return render(request, 'skill/skill_request.html', context)

@login_required(login_url='signin')
def All_Skill_Requests(request):
    skill_request = SkillRequest.objects.filter(to_user = request.user)
    context = {
        'requests': skill_request
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        skill_request = SkillRequest.objects.get(id = request_id)
        if action == 'accept':
            skill_request.status = 'accepted'
            skill_request.save()
            if not (Connection.objects.filter(user_one = skill_request.from_user, user_two = skill_request.to_user).exists() or Connection.objects.filter(user_one = skill_request.to_user, user_two = skill_request.from_user).exists()):
                Connection.objects.create(user_one = skill_request.from_user, user_two = skill_request.to_user)
        elif action == 'reject':
            skill_request.status = 'rejected'
            skill_request.save()
        return redirect('all_skill_requests')
    return render(request,'skill/requests.html', context)

@login_required(login_url='signin')
def My_Skill_Requests(request):
    requests = SkillRequest.objects.filter(from_user = request.user)
    context = {
        'requests': requests
    }
    return render(request, 'skill/myrequests.html', context)

@login_required(login_url='signin')
def My_Connection(request):
    connections = Connection.objects.filter(Q(user_one = request.user)| Q(user_two = request.user))
    context = {
        'connections' : connections,
    }
    return render (request,'skill/connections.html', context)