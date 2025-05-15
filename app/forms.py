from django import forms

from app.models import Page, Rating, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaImageDetection, CriteriaOCR, PageSet, Service


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['service', 'image', 'execution_time', 'type', 'text']


class PageSetForm(forms.ModelForm):
    class Meta:
        model = PageSet
        fields = ['image', 'execution_time']


class RatingForm(forms.ModelForm):
    page_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rating
        fields = ['page_id']


class AdminExportForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all().order_by('name'))


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
