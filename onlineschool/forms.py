from django.forms import ModelForm
from .models import Room
from django import forms
class RoomForm (forms.ModelForm):
    class Meta:
        
        model=Room
        fields = "__all__"
        exclude=['host','participants']
        # fields = ('id',)
        # fields = '_all_'