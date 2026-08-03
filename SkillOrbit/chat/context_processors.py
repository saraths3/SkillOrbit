from .models import Message
from django.db.models import Q

def unread_messages_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(Q(conversation__user_one = request.user, is_read = False)| Q(conversation__user_two = request.user, is_read = False)).exclude(sender = request.user).count()
        return {'unread_messages': count}
    return {'unread_messages': 0}