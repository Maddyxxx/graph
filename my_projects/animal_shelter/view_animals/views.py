from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from view_animals.models import Animal, Shelter
from view_animals.forms import AnimalForm


class ShowAnimals(View):
    def get(self, request, shelter_id, *args, **kwargs):
        shelter = Shelter.objects.get(id=shelter_id)
        animals = Animal.objects.filter(shelter=shelter)
        all_count = animals.count()
        return render(request, 'user_pages/main_page.html', {
            'shelter': shelter, 'animals': animals, 'all_count': all_count})


class SheltersView(View):
    def get(self, request):
        shelters = Shelter.objects.all()
        return render(request, 'shelter_pages/main_page.html', context={'shelters': shelters})


class AnimalView(View):
    def get(self, request, animal_id):
        animal = Animal.objects.get(id=animal_id)
        return render(request, 'animal_pages/info.html', context={
            'animal': animal, 'animal_id': animal_id})


class AnimalFormView(View):

    def get(self, request):
        animal_form = AnimalForm()
        return render(request, 'animal_pages/register.html', context={'animal_form': animal_form})

    def post(self, request):
        animal_form = AnimalForm(request.POST)

        if animal_form.is_valid():
            Animal.objects.create(**animal_form.cleaned_data)
            return HttpResponseRedirect('/animal/register')
        return render(request, 'animal_pages/register.html', context={'animal_form': animal_form})


class AnimalEditFormView(View):
    def get(self, request, animal_id):
        animal = Animal.objects.get(id=animal_id)
        animal_form = AnimalForm(instance=animal)
        return render(request, 'animal_pages/edit.html', context={'animal_form': animal_form, 'animal_id': animal_id})

    def post(self, request, animal_id):
        animal = Animal.objects.get(id=animal_id)
        animal_form = AnimalForm(request.POST, instance=animal)

        if animal_form.is_valid():
            animal.save()
        return render(request, 'animal_pages/edit.html', context={'animal_form': animal_form, 'animal_id': animal_id})
