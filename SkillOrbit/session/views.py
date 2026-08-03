from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScheduleSessionForm
from .models import ScheduleSession
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from datetime import datetime

User = get_user_model()

@login_required(login_url="signin")
def ScheduleSessionView(request, user_id=None):
    participant = None
    if user_id:
        participant = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ScheduleSessionForm(request.POST)
        if form.is_valid():
            session_obj = form.save(commit=False)
            session_obj.host = request.user
            if participant:
                session_obj.participant = participant

            if not session_obj.meeting_link:
                session_obj.meeting_link = f"https://meet.jit.si/SkillOrbit-Session-{request.user.username}"

            session_obj.save()
            messages.success(request, f"Learning session scheduled with @{session_obj.participant.username}!")
            return redirect('sessions')
    else:
        form = ScheduleSessionForm()

    context = {
        'form': form,
        'participant': participant,
    }
    return render(request, 'session/schedule.html', context)


@login_required(login_url="signin")
def accept_session_view(request, session_id):
    session_obj = get_object_or_404(ScheduleSession, id=session_id)
    if request.user == session_obj.participant or request.user == session_obj.host:
        session_obj.status = 'accepted'
        session_obj.save()
        messages.success(request, f'Session "{session_obj.name}" has been accepted!')
    return redirect('sessions')


@login_required(login_url="signin")
def complete_session_view(request, session_id):
    session_obj = get_object_or_404(ScheduleSession, id=session_id)
    if request.user == session_obj.host or request.user == session_obj.participant:
        session_obj.status = 'complete'
        session_obj.save()
        messages.success(request, f'Session "{session_obj.name}" marked as completed!')
    return redirect('sessions')


@login_required(login_url="signin")
def cancel_session_view(request, session_id):
    session_obj = get_object_or_404(ScheduleSession, id=session_id)
    if request.user == session_obj.host or request.user == session_obj.participant:
        session_obj.status = 'canceled'
        session_obj.save()
        messages.info(request, f'Session "{session_obj.name}" was canceled.')
    return redirect('sessions')