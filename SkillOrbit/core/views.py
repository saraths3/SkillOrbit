from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
from .forms import TopicForm
from django.contrib import messages
from skill.models import UserSkill
from django.contrib.auth import get_user_model
from django.db.models import Q
from skill.models import Connection, SkillRequest

# Create your views here.
@login_required(login_url="signin")
def home_view(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    
    context = {
        "user_skills": user_skills,
    }
    return render(request, 'core/home.html', context)

def explore_view(request):
    User = get_user_model()
    all_users = User.objects.select_related('userprofile').prefetch_related('userskill_set__skill').exclude(id=request.user.id)
    query = request.GET.get('q')
    if query:
        query = query.strip()
        if query[0] == '@':
            query = query[1:]
            print(query)
            matching_skill_user_ids = UserSkill.objects.filter(skill__name__icontains=query).values_list('user_id', flat = True)
            all_users = all_users.filter(Q(username__icontains=query)).distinct()
            context = {
                'all_users': all_users
            }
            return render(request, 'core/explore.html', context)
        matching_skill_user_ids = UserSkill.objects.filter(skill__name__icontains=query).values_list('user_id', flat=True)
        all_users = all_users.filter(
            Q(full_name__icontains=query) |
            Q(id__in=matching_skill_user_ids)
        ).distinct()
    context = {
        'all_users': all_users
    }
    return render(request, 'core/explore.html', context)

@login_required(login_url='signin')
def public_profile_view(request, pp_id):
    User = get_user_model()
    user_profile = get_object_or_404(
        User.objects.select_related('userprofile').prefetch_related('userskill_set__skill'),id=pp_id 
    )
    context = {
        'user': user_profile
    }
    return render(request, 'core/public_profile.html', context)

@login_required(login_url="signin")
def sessions_view(request):
    return render(request, 'core/sessions.html')

@login_required(login_url="signin")
def community_list_view(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.user = request.user
            new_topic.save()
            messages.success(request, f'Topic "{new_topic.title}" created successfully!')
            return redirect('community')
    else:
        form = TopicForm()
    context = {
        'topics' : topics,
        'form':  form
    }
    return render(request, 'core/community.html', context)


@login_required(login_url="signin")
def topic_delete_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.user == request.user:
        topic.delete()
        messages.success(request, "Topic board and all associated chats have been removed.")
    else:
        messages.error(request, "Permission denied. You cannot delete an unowned topic room.")
    return redirect('community')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment

@login_required(login_url="signin")
def community_room_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('message_body', '').strip()
        if comment_text:
            Comment.objects.create(topic=topic, user=request.user, comment=comment_text)
            return redirect('community_room', topic_id=topic.id)

    context = {
        'topic': topic,
        'comments': topic.My_Comments.order_by('created_at'),
    }
    return render(request, 'core/community_room.html', context)

