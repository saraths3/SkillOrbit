from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.db.models import Q

# Create your views here.
@login_required(login_url='signin')
def chat(request, user_id):
    User = get_user_model()
    user_two = User.objects.get(id = user_id)
    # print(user_two.username)
    conversation = Conversation.objects.filter(Q(user_one = request.user, user_two = user_two) | Q(user_one= user_two, user_two= request.user)).first()
    
    return render(request, 'chat/chat.html')