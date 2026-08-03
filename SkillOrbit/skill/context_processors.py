from  .models import SkillRequest,Connection
from django.db.models import Q

def pending_request(request):
    if request.user.is_authenticated:
        count = SkillRequest.objects.filter(to_user = request.user, status = 'pending').count()
        return {'pending_requests_count': count}
    return {'pending_requests_count':0}

def connection_context(request):
    if request.user.is_authenticated:
        connections = Connection.objects.filter(Q(user_one=request.user) | Q(user_two=request.user))
        return {'connections': connections}
    return {'connections': []}