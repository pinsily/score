from django.contrib import admin

# Register your models here.
from system.models import Profile, Professor, Module, Score


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'year', 'semester')


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('index', 'code', 'name',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username',)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'professor', 'score')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Score, ScoreAdmin)
