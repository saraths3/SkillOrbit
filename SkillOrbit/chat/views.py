from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.db.models import Q

# Create your views here.
@login_required(login_url='signin')
def chat(request, user_id):
    User = get_user_model()
    user_two = get_object_or_404(User, id = user_id)
    # print(user_two.username)
    conversation = Conversation.objects.filter(Q(user_one = request.user, user_two = user_two) | Q(user_one= user_two, user_two= request.user)).first()
    if not conversation:
        conversation = Conversation.objects.create(user_one = request.user, user_two = user_two)
    context = {
        'conversation': conversation,
        'user_two': user_two
    }
    return render(request, 'chat/chat.html', context)