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
    from accounts.models import UserProfile
    from session.models import ScheduleSession
    user_skills = UserSkill.objects.filter(user=request.user)
    user_connections = Connection.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).select_related('user_one', 'user_two')
    connections_count = user_connections.count()
    pending_requests_count = SkillRequest.objects.filter(to_user=request.user, status='pending').count()
    recent_topics = Topic.objects.order_by('-created_at')[:4]
    user_sessions = ScheduleSession.objects.filter(
        Q(host=request.user) | Q(participant=request.user)
    ).select_related('host', 'participant', 'host__userprofile', 'participant__userprofile').order_by('-created_at')[:5]

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    recent_connections = []
    for conn in user_connections[:4]:
        partner = conn.user_two if conn.user_one == request.user else conn.user_one
        partner_prof, _ = UserProfile.objects.get_or_create(user=partner)
        recent_connections.append({
            'user': partner,
            'profile': partner_prof,
        })
    readiness_score = min(100, (user_skills.count() * 20) + (connections_count * 15) + (20 if profile.bio else 0) + (10 if profile.avatar else 0))
    if readiness_score == 0:
        readiness_score = 15

    context = {
        "user_skills": user_skills,
        "connections_count": connections_count,
        "pending_requests_count": pending_requests_count,
        "recent_topics": recent_topics,
        "recent_connections": recent_connections,
        "user_sessions": user_sessions,
        "readiness_score": readiness_score,
        "profile": profile,
    }
    return render(request, 'core/home.html', context)

@login_required(login_url='signin')
def explore_view(request):
    User = get_user_model()
    all_users = User.objects.exclude(id=request.user.id)
    query = request.GET.get('q')
    if query:
        query = query.strip()
        if query.startswith('@'):
            all_users = all_users.filter(username__icontains=query[1:])
        else:
            skill_users = UserSkill.objects.filter(skill__name__icontains=query).values_list('user_id', flat=True)
            all_users = all_users.filter(Q(full_name__icontains=query) | Q(id__in=skill_users))
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
    from session.models import ScheduleSession
    user_sessions = ScheduleSession.objects.filter(
        Q(host=request.user) | Q(participant=request.user)
    ).select_related('host', 'participant', 'host__userprofile', 'participant__userprofile').order_by('-created_at')[:5]

    context = {
        'user_sessions': user_sessions,
    }
    return render(request, 'core/sessions.html', context)

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
            messages.error(request, 'Failed to create topic board. Please check your form input.')
    else:
        form = TopicForm()
    context = {
        'topics': topics,
        'form': form
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


@login_required(login_url="signin")
def community_room_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('message_body', '').strip()
        if comment_text:
            Comment.objects.create(topic=topic, user=request.user, comment=comment_text)
            messages.success(request, "Comment posted!")
            return redirect('community_room', topic_id=topic.id)

    context = {
        'topic': topic,
        'comments': topic.My_Comments.order_by('created_at'),
    }
    return render(request, 'core/community_room.html', context)

