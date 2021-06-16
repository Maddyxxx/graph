from django.contrib import admin
from .models import Graph, Vector


@admin.register(Graph)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'operation']
    search_fields = ['id']


@admin.register(Vector)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'vector']
