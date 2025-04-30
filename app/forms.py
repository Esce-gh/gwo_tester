from django import forms

from app.models import Page, Rating, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['service', 'image']


class RatingForm(forms.ModelForm):
    page_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rating
        fields = ['page_id']


class CriteriaPageNumberForm(forms.ModelForm):
    class Meta:
        model = CriteriaPageNumber
        fields = ['page_number_detected', 'page_number_visible']


class CriteriaHeaderFooterForm(forms.ModelForm):
    class Meta:
        model = CriteriaHeaderFooter
        fields = ['header_detected', 'header_visible', 'footer_detected', 'footer_visible']


class CriteriaObjectDetectionForm(forms.ModelForm):
    class Meta:
        model = CriteriaObjectDetection
        fields = ['detected_objects', 'visible_objects']
