from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm


@login_required(login_url="signin")
def course_list_view(request):
    courses = Course.objects.exclude(video_url='').order_by('-created_at')
    return render(request, 'course/course_list.html', {'courses': courses})


@login_required(login_url="signin")
def create_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, f'Video Course "{course.title}" published!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/create_course.html', {'form': form})