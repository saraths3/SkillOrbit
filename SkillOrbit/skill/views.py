from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserSkillForm,SkillRequestForm
from django.contrib.auth.decorators import login_required
from .models import UserSkill,SkillRequest,Connection
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.

# Skills

@login_required(login_url='signin')
def add_skills(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name', '').strip()
        proficiency = request.POST.get('proficiency', 'beginner')
        years = request.POST.get('years_of_experience')

        if not skill_name:
            messages.error(request, 'Please enter or select a skill name.')
            return render(request, 'skill/add_skill.html', {
                'skill_name': skill_name,
                'proficiency': proficiency,
                'years_of_experience': years,
            })

        from .models import Skill
        skill_obj = Skill.objects.filter(name__iexact=skill_name).first()
        if not skill_obj:
            skill_obj = Skill.objects.create(name=skill_name)

        if UserSkill.objects.filter(user=request.user, skill=skill_obj).exists():
            messages.error(request, f'"{skill_obj.name}" is already in your portfolio.')
            return render(request, 'skill/add_skill.html', {
                'skill_name': skill_name,
                'proficiency': proficiency,
                'years_of_experience': years,
            })

        years_val = None
        if years and str(years).isdigit():
            years_val = int(years)

        UserSkill.objects.create(
            user=request.user,
            skill=skill_obj,
            proficiency=proficiency,
            years_of_experience=years_val
        )
        messages.success(request, f'Added "{skill_obj.name}" to your portfolio!')
        return redirect('profile')

    return render(request, 'skill/add_skill.html')

@login_required(login_url="signin")
def delete_skills(request, sid):
    userskill = get_object_or_404(UserSkill, id=sid, user=request.user)
    userskill.delete()
    messages.success(request, 'Skill deleted successfully!')
    return redirect("profile")

@login_required(login_url='signin')
def edit_skills(request, sid):
    userskill = get_object_or_404(UserSkill, id=sid, user=request.user)
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name', '').strip()
        proficiency = request.POST.get('proficiency', 'beginner')
        years = request.POST.get('years_of_experience')

        if not skill_name:
            messages.error(request, 'Please enter or select a skill name.')
            return render(request, 'skill/edit_skill.html', {'userskill': userskill})

        from .models import Skill
        skill_obj = Skill.objects.filter(name__iexact=skill_name).first()
        if not skill_obj:
            skill_obj = Skill.objects.create(name=skill_name)

        if UserSkill.objects.filter(user=request.user, skill=skill_obj).exclude(id=userskill.id).exists():
            messages.error(request, f'"{skill_obj.name}" is already in your portfolio.')
            return render(request, 'skill/edit_skill.html', {'userskill': userskill})

        years_val = None
        if years and str(years).isdigit():
            years_val = int(years)

        userskill.skill = skill_obj
        userskill.proficiency = proficiency
        userskill.years_of_experience = years_val
        userskill.save()

        messages.success(request, f'Updated "{skill_obj.name}" successfully!')
        return redirect('profile')

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
    recipient_skills = Skill.objects.filter(userskill__user=reciever_user)
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
        'reciever_user': reciever_user
    }
    return render(request, 'skill/skill_request.html', context)

@login_required(login_url='signin')
def All_Skill_Requests(request):
    skill_requests = SkillRequest.objects.filter(to_user=request.user).order_by('-created_at')
    context = {
        'requests': skill_requests
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        req_obj = get_object_or_404(SkillRequest, id=request_id, to_user=request.user)
        if action == 'accept':
            req_obj.status = 'accepted'
            req_obj.save()
            if not (Connection.objects.filter(user_one=req_obj.from_user, user_two=req_obj.to_user).exists() or Connection.objects.filter(user_one=req_obj.to_user, user_two=req_obj.from_user).exists()):
                Connection.objects.create(user_one=req_obj.from_user, user_two=req_obj.to_user)
            messages.success(request, f'Accepted skill request from {req_obj.from_user.username}!')
        elif action == 'reject':
            req_obj.status = 'rejected'
            req_obj.save()
            messages.info(request, f'Rejected skill request from {req_obj.from_user.username}.')
        return redirect('all_skill_requests')
    return render(request, 'skill/requests.html', context)

@login_required(login_url='signin')
def My_Skill_Requests(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        if action == 'cancel' and request_id:
            req_obj = get_object_or_404(SkillRequest, id=request_id, from_user=request.user)
            req_obj.delete()
            messages.success(request, 'Skill request cancelled.')
            return redirect('my_requests')

    requests = SkillRequest.objects.filter(from_user=request.user).order_by('-created_at')
    context = {
        'requests': requests
    }
    return render(request, 'skill/myrequests.html', context)

@login_required(login_url='signin')
def My_Connection(request):
    return render(request, 'skill/connections.html')