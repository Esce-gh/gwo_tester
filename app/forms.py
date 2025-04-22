from django import forms

from app.models import Service, Page, Rating


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['service', 'image']


class RatingForm(forms.ModelForm):
    page_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rating
        fields = ['is_ok', 'comment', 'page_id']
