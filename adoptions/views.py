from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from django import forms
from datetime import datetime

from .models import Pet

def home(request):
    pets = Pet.objects.all()
    return render(request, 'home.html', {
        'pets': pets,
    })

def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404('pet not found')
    return render(request, 'pet_detail.html', {
        'pet': pet,
    })


class PetForm(forms.Form):
    name = forms.CharField(max_length=100)
    submitter = forms.CharField(max_length=100)
    species = forms.CharField(max_length=30)
    breed = forms.CharField(max_length=30, required=False)
    description = forms.CharField(max_length=100, required=False)
    sex = forms.ChoiceField(choices = Pet.SEX_CHOICES)
    age = forms.IntegerField(required=False)


def add_pet(request):

    if request.method == 'POST':
        # In this case, the user has filled the form and
        # the "request" parameter contains the filled values.

        # Create a form with the data stored in the request
        form = PetForm(request.POST) 
        if form.is_valid():
            # Extract the data fields from the form
            name = form.cleaned_data['name']
            submitter = form.cleaned_data['submitter']
            species = form.cleaned_data['species']
            breed = form.cleaned_data['breed']
            description = form.cleaned_data['description']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']

            # Create a pet object with this information
            newpet = Pet(
                        name=name,
                        submitter=submitter,
                        species=species,
                        breed=breed,
                        description=description,
                        age=age,
                        sex=sex,
                        submission_date=datetime.now()
                        
            )

            # Save it to the database
            newpet.save()
        # Head back to the home page
        return HttpResponseRedirect(reverse('home'))

    else:
        # Return a blank form
        return render(
            request, 
            'add_pet.html',
            {'form': PetForm()}
        )
    

def delete_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.delete()
    # Head back to the home page
    return HttpResponseRedirect(reverse('home'))

