from django.contrib import admin

from .models import Lesson, Module, Subject, Unit


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    show_change_link = True


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    show_change_link = True


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'order']
    list_filter = ['subject']
    inlines = [UnitInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order']
    list_filter = ['module__subject']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'type', 'order']
    list_filter = ['type', 'unit__module__subject']
