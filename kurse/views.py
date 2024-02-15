from django.shortcuts import render, redirect
from .models import Trainer
from .forms import KursForm


def is_orga_group(user):
    return user.groups.filter(name='orga').exists()


# Create your views here.

def create_kurs(request):
    if request.method == 'POST':
        form = KursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = KursForm()

    return render(request, 'trainer/create_trainer.html', {'form': form})
