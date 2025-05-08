from django import forms

from app.models import Page, Rating, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaImageDetection, CriteriaOCR


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['service', 'image', 'execution_time']
        widgets = {'execution_time': forms.HiddenInput}


class RatingForm(forms.ModelForm):
    page_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rating
        fields = ['page_id']


class CriteriaPageNumberForm(forms.ModelForm):
    class Meta:
        model = CriteriaPageNumber
        fields = ['page_number_detected', 'page_number_visible', 'comment']


class CriteriaHeaderFooterForm(forms.ModelForm):
    class Meta:
        model = CriteriaHeaderFooter
        fields = ['header_detected', 'header_visible', 'footer_detected', 'footer_visible', 'comment']


class CriteriaObjectDetectionForm(forms.ModelForm):
    class Meta:
        model = CriteriaObjectDetection
        fields = ['detected_objects', 'visible_objects', 'comment']


class CriteriaImageDetectionForm(forms.ModelForm):
    class Meta:
        model = CriteriaImageDetection
        fields = ['detected_images', 'visible_images', 'comment']


class CriteriaOCRForm(forms.ModelForm):
    class Meta:
        model = CriteriaOCR
        fields = ['word_recognition_errors', 'comment']
