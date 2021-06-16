from django.contrib import admin
from view_animals.models import Shelter, User, Animal


class ShelterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city']
    search_fields = ['city']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    search_fields = ['shelter']


class AnimalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'shelter', 'special_signs']
    search_fields = ['arrival_date', 'shelter', 'is_arrived']


admin.site.register(Shelter, ShelterAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Animal, AnimalAdmin)
