from django.contrib import admin

from courses.models import Courses, Comments


class CoursesAdmin(admin.ModelAdmin):
    model = Courses

    list_display = ['title', 'published', 'get_author_username']
    prepopulated_fields = {'slug': ('title',)}

    def get_author_username(self, instance):
        return instance.author.username

    get_author_username.short_description = 'Author'


admin.site.register(Courses, CoursesAdmin)


class CommentsAdmin(admin.ModelAdmin):
    model = Comments


admin.site.register(Comments, CommentsAdmin)
