from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from courses.forms import CommentsForm, CourseCreateForm
from courses.models import Comments, Courses
from django.contrib.auth import get_user_model

User = get_user_model()


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class CoursesListView(ListView):
    template_name = 'courses/course_list.html'
    model = Courses
    ordering = ['-published']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context['side_course'] = Courses.objects.filter().order_by('-published')[:5]
        context['users'] = User.objects.exclude(id=self.request.user.id)
        return context


# class CoursesDetailView(DetailView):
#     template_name = 'courses/course_detail.html'
#     context_object_name = 'course_detail'
#     model = Courses

def course_detail(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    comments = course.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comments.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.course = course
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        comment_form = CommentsForm()
    context = {'course_detail': course,
               'comments': comments,
               'comment_form': comment_form}
    return render(request, 'courses/course_detail.html', context)


class CoursesCreateView(LoginRequiredMixin, CreateView):
    template_name = 'courses/course_form.html'
    model = Courses
    form_class = CourseCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CoursesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'courses/course_form.html'
    model = Courses
    form_class = CourseCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


class CoursesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'courses/course_delete.html'
    model = Courses
    success_url = reverse_lazy('accounts:dashboard')

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.author:
            return True
        return False


class SearchView(ListView):
    model = Courses
    template_name = 'courses/course_search.html'
    context_object_name = 'search_list'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            result = Courses.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query)
            )
        else:
            result = Courses.objects.all()
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')

        return context


class BaseTemplateView(ListView):
    model = Courses
    template_name = 'base.html'
