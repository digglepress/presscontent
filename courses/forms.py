from django import forms
from courses.models import Courses, Comments
from tinymce.widgets import TinyMCE


class CourseCreateForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(mce_attrs={'width': 750, 'class': 'form-group'}))

    class Meta:
        model = Courses
        fields = ['cover', 'title', 'summary', 'body']


class CommentsForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 5,
            'cols': 10
        }
    ))

    class Meta:
        fields = ['comment']
        model = Comments
