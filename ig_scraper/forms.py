from django import forms
from .models import Influencer

class InfluencerForm(forms.ModelForm):
    class Meta:
        model = Influencer
        fields = ['username']