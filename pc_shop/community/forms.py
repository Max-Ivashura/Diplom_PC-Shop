from django import forms
from .models import CommunityBuild, Comment

class CommunityBuildForm(forms.ModelForm):
    class Meta:
        model = CommunityBuild
        fields = ['title', 'description', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']