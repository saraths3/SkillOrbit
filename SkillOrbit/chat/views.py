from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from .models import Conversation, Message


@login_required(login_url='signin')
def chat(request, user_id):
    User = get_user_model()
    user_two = get_object_or_404(User, id=user_id)
    if user_two == request.user:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("explore")
    conversation = Conversation.objects.filter(Q(user_one=request.user, user_two=user_two) | Q(user_one=user_two, user_two=request.user)).first()
    if conversation is None:
        conversation = Conversation.objects.create(user_one=request.user,user_two=user_two)
    chat_messages = Message.objects.filter(conversation=conversation).order_by("created_at")
    context = {
        "user_two": user_two,
        "conversation": conversation,
        "chat_messages": chat_messages,
    }

    return render(request, "chat/chat.html", context)