from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UserSkill, SkillRequest, Skill, Connection
from .forms import UserSkillForm, SkillRequestForm
from django.db import models
from django.db.models import Q

@login_required(login_url='signin')
def add_skills(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            skill_instance = form.save(commit=False)
            skill_type = request.POST.get('skill_type')
            
            if skill_type not in ['teach', 'learn']:
                messages.error(request, 'Invalid skill category selected.')
                return redirect('add_skills')

            skill_instance.user = request.user
            skill_instance.skill_type = skill_type

            if UserSkill.objects.filter(user=request.user, skill=skill_instance.skill, skill_type=skill_type).exists():
                messages.warning(request, f'You have already added "{skill_instance.skill.name}" to your {skill_type} list.')
                return redirect('profile')

            skill_instance.save()
            messages.success(request, f'Skill "{skill_instance.skill.name}" added successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserSkillForm()

    return render(request, 'skill/add_skill.html', {'form': form})


@login_required(login_url='signin')
def delete_skills(request, id):
    userskill = get_object_or_404(UserSkill, id=id, user=request.user)
    skill_name = userskill.skill.name
    userskill.delete()
    messages.success(request, f'Skill "{skill_name}" removed successfully.')
    return redirect('profile')


@login_required(login_url='signin')
def edit_skills(request, id):
    userskill = get_object_or_404(UserSkill, id=id, user=request.user)
    if request.method == 'POST':
        form = UserSkillForm(request.POST, instance=userskill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = UserSkillForm(instance=userskill)
    return render(request, 'skill/edit_skill.html', {'userskill': userskill})


@login_required(login_url='signin')
def skill_request(request):
    User = get_user_model()
    user_id = request.POST.get('user_id') or request.GET.get('user_id')
    if not user_id:
        messages.error(request, 'No recipient user specified for skill request.')
        return redirect('explore')
    reciever_user = get_object_or_404(User, id=user_id)
    if reciever_user == request.user:
        messages.error(request, 'You cannot send a skill request to yourself.')
        return redirect('public_profile', pp_id=reciever_user.id)
        
    existing_request = SkillRequest.objects.filter(from_user=request.user, to_user=reciever_user, status='pending').first()
    if existing_request:
        messages.error(request, f'You already have a pending skill request to {reciever_user.username}.')
        return redirect('public_profile', pp_id=reciever_user.id)
    user_skill_ids = UserSkill.objects.filter(user=reciever_user).values_list('skill_id', flat=True)
    recipient_skills = Skill.objects.filter(id__in=user_skill_ids)

    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        form.fields['skill'].queryset = recipient_skills
        if form.is_valid():
            skill_req = form.save(commit=False)
            skill_req.from_user = request.user
            skill_req.to_user = reciever_user
            skill_req.save()
            messages.success(request, f'Skill request sent to {reciever_user.username} successfully!')
            return redirect('public_profile', pp_id=reciever_user.id)
        else:
            messages.error(request, 'Failed to send skill request. Please check the form.')
    else:
        form = SkillRequestForm()
        form.fields['skill'].queryset = recipient_skills

    context = {
        'form': form,
        'user_id': user_id,
        'reciever_user': reciever_user,
        'has_skills': recipient_skills.exists()
    }
    return render(request, 'skill/skill_request.html', context)


@login_required(login_url='signin')
def All_Skill_Requests(request):
    skill_requests = SkillRequest.objects.filter(to_user=request.user).order_by('-created_at')
    return render(request, 'skill/requests.html', {'requests': skill_requests})


@login_required(login_url='signin')
def My_Skill_Requests(request):
    skill_requests = SkillRequest.objects.filter(from_user=request.user).order_by('-created_at')
    return render(request, 'skill/myrequests.html', {'requests': skill_requests})


@login_required(login_url='signin')
def My_Connection(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        
        req_obj = get_object_or_404(SkillRequest, id=request_id, to_user=request.user)
        
        if action == 'accept':
            req_obj.status = 'accepted'
            req_obj.save()
            if not (Connection.objects.filter(user_one=req_obj.from_user, user_two=req_obj.to_user).exists() or Connection.objects.filter(user_one=req_obj.to_user, user_two=req_obj.from_user).exists()):
                Connection.objects.create(user_one=req_obj.from_user, user_two=req_obj.to_user)
            messages.success(request, f'Connection accepted with {req_obj.from_user.username}!')
        elif action == 'reject':
            req_obj.status = 'rejected'
            req_obj.save()
            messages.info(request, f'Request from {req_obj.from_user.username} declined.')
            
        return redirect('all_skill_requests')

    user_connections = Connection.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).select_related('user_one', 'user_two')
    return render(request, 'skill/connections.html', {'connections': user_connections})