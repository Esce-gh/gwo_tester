from django import forms

from app.models import Page, Rating, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaImageDetection, CriteriaOCR, PageSet, Service, CriteriaObjectGroups


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
        fields = ['visible_text_objects', 'detected_text_objects',
                  'visible_image_objects', 'detected_image_objects',
                  'visible_table_objects', 'detected_table_objects',
                  'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 2,
            }),
        }


class CriteriaImageDetectionForm(forms.ModelForm):
    class Meta:
        model = CriteriaImageDetection
        fields = ['detected_images', 'visible_images', 'comment']


class CriteriaOCRForm(forms.ModelForm):
    class Meta:
        model = CriteriaOCR
        fields = ['word_recognition_errors', 'comment']


class CriteriaObjectGroupsForm(forms.ModelForm):
    class Meta:
        model = CriteriaObjectGroups
        fields = ['visible_groups', 'detected_groups', 'comment']
