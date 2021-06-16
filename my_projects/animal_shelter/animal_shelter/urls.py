"""animal_shelter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from view_animals.views import AnimalFormView, AnimalEditFormView, SheltersView, ShowAnimals, AnimalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('view_animals.urls')),
    path('main_page/', SheltersView.as_view()),
    path('animal/register/', AnimalFormView.as_view()),
    path('animal/<int:animal_id>/edit/', AnimalEditFormView.as_view()),
    path('<int:shelter_id>/animals/', ShowAnimals.as_view(), name='животные'),
    path('animals/<int:animal_id>/', AnimalView.as_view(), name='информация о животном')
]
