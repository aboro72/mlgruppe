from django.shortcuts import render, redirect
from .models import Trainer
from .forms import TrainerForm


def create_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = TrainerForm()

    return render(request, 'trainer/create_trainer.html', {'form': form})
