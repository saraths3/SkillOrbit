from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm
from skill.models import Connection


@login_required(login_url="signin")
def course_list_view(request):
    conn1 = Connection.objects.filter(user_one=request.user).values_list('user_two_id', flat=True)
    conn2 = Connection.objects.filter(user_two=request.user).values_list('user_one_id', flat=True)
    allowed_user_ids = list(conn1) + list(conn2) + [request.user.id]
    courses = Course.objects.filter(user_id__in=allowed_user_ids).exclude(video_url='').order_by('-created_at')
    return render(request, 'course/course_list.html', {'courses': courses})


@login_required(login_url="signin")
def create_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, f'Video Course "{course.title}" published for your network!')
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'course/create_course.html', {'form': form})