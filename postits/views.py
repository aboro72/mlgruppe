from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PostIt
from .forms import PostItForm


def postit_list(request):
    postits = PostIt.objects.all()
    return render(request, 'postits/postit_list.html', {'postits': postits})


def postit_detail(request, id):
    postit = PostIt.objects.get(id=id)
    return render(request, 'postits/postit_detail.html', {'postit': postit})


@login_required
def postit_create(request):
    if request.method == 'POST':
        form = PostItForm(request.POST)
        if form.is_valid():
            new_postit = form.save(commit=False)
            new_postit.user = request.user
            new_postit.save()
            return redirect('postits:postit_list')
    else:
        form = PostItForm()
    return render(request, 'postits/postit_form.html', {'form': form})


@login_required
def postit_update(request, postit_id):
    postit = get_object_or_404(PostIt, id=postit_id, user=request.user)

    if request.method == 'POST':
        form = PostItForm(request.POST, instance=postit)
        if form.is_valid():
            form.save()
            return redirect('postits:postit_list')
    else:
        form = PostItForm(instance=postit)

    return render(request, 'postits/postit_form.html', {'form': form})


@login_required
def postit_delete(request, postit_id):
    postit = get_object_or_404(PostIt, id=postit_id, user=request.user)
    postit.delete()
    return redirect('postits:postit_list')