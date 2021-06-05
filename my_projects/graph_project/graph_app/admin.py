from django.contrib import admin
from .models import Graph


@admin.register(Graph)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['vector', 'operation']
    list_filter = ['vector']
    search_fields = ['vector']

