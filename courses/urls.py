from django.urls import path
from courses.views import CoursesCreateView, CoursesListView, CoursesUpdateView, CoursesDeleteView, \
    SearchView, course_detail

app_name = 'course'
urlpatterns = [
    path('', CoursesListView.as_view(), name="home"),
    path('courses/', CoursesListView.as_view(), name="courses"),
    path('courses/<slug:slug>/', course_detail, name="course_detail"),
    # path('courses/<slug:slug>/', CoursesDetailView.as_view(), name="course_detail"),
    path('create/', CoursesCreateView.as_view(), name="course_create"),
    path('courses/update/<slug:slug>/', CoursesUpdateView.as_view(), name="course_update"),
    path('courses/delete/<slug:slug>/', CoursesDeleteView.as_view(), name="course_delete"),
    path('search/', SearchView.as_view(), name="search"),
]
