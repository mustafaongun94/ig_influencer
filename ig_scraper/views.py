from django.shortcuts import render, redirect, get_object_or_404
from .models import Influencer, Post, Story
from .forms import InfluencerForm
from .scraper import fetch_influencer_data


def influencer_list(request):
    influencers = Influencer.objects.all()
    return render(request, 'influencer/influencer_list.html', {'influencers': influencers})


def influencer_detail(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    posts = Post.objects.filter(influencer=influencer)
    stories = Story.objects.filter(influencer=influencer)
    return render(request, 'influencer/influencer_detail.html', {'influencer': influencer, 'posts': posts, 'stories': stories})


def influencer_add(request):
    if Influencer.objects.count() >= 20:
        return redirect('influencer_list')

    if request.method == 'POST':
        form = InfluencerForm(request.POST)
        if form.is_valid():
            saved_influencer = form.save()
            fetch_influencer_data(saved_influencer.username)
            return redirect('influencer_list')
    else:
        form = InfluencerForm()

    return render(request, 'influencer/influencer_form.html', {'form': form})


def influencer_delete(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    if request.method == 'POST':
        influencer.delete()
        return redirect('influencer_list')
    return render(request, 'influencer/influencer_confirm_delete.html', {'influencer': influencer})
