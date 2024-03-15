from django.contrib import admin

from .models import Task, Test, Answer, Results


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    display_fields = ('text', 'choises', 'test')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    display_fields = ('text', )


@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    display_fields = ('date', 'test', 'name', 'res')
