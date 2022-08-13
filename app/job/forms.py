from dal import autocomplete
from master.models import PartMF, Furnance
from django import forms

from .models import Job, JobFurnance, JobPhoto, JobPhotoInspectQ, JobInspection, JobSetting
from crispy_forms.helper import FormHelper

class SearchPartForm(forms.Form):
     part = forms.ModelChoiceField(
        queryset=PartMF.objects.all(),
        widget=autocomplete.ModelSelect2(url='part-autocomplete')
    )
class FurnanceForm(forms.Form):
    furnance = forms.ModelChoiceField(queryset=Furnance.objects.all())

class JobPhotoForm(forms.ModelForm):
    photo = forms.ImageField(widget = forms.FileInput)
    class Meta:
        model = JobPhoto
        exclude = ()

class JobPhotoInspectQForm(forms.ModelForm):
    photo = forms.ImageField(widget = forms.FileInput)
    class Meta:
        model = JobPhotoInspectQ
        exclude = ()


class TRQForm(forms.Form):
    furnance = forms.ModelChoiceField(queryset=Furnance.objects.all())
    ptn = forms.IntegerField()
    zone1_temp = forms.FloatField(required=False)
    zone2_temp = forms.FloatField(required=False)
    zone3_temp = forms.FloatField(required=False)
    zone4_temp = forms.FloatField(required=False)
    zone5_temp = forms.FloatField(required=False)
    zone6_temp = forms.FloatField(required=False)
    zone1_cp = forms.FloatField(required=False)
    zone2_cp = forms.FloatField(required=False)
    zone3_cp = forms.FloatField(required=False)
    zone4_cp = forms.FloatField(required=False)
    zone5_cp = forms.FloatField(required=False)
    zone6_cp = forms.FloatField(required=False)
    zone1_nh = forms.FloatField(required=False)
    zone2_nh = forms.FloatField(required=False)
    zone3_nh = forms.FloatField(required=False)
    zone4_nh = forms.FloatField(required=False)
    zone5_nh = forms.FloatField(required=False)
    zone6_nh = forms.FloatField(required=False)
    rxgas = forms.FloatField(required=False)
    speedtime = forms.FloatField(required=False)

    zone1_ot = forms.FloatField(required=False)
    zone2_ot = forms.FloatField(required=False)
    zone3_ot = forms.FloatField(required=False)
    zone4_ot = forms.FloatField(required=False)
    zone5_ot = forms.FloatField(required=False)
    zone6_ot = forms.FloatField(required=False)

    agigator_hz = forms.FloatField(required=False)
    feed_pattern = forms.CharField(required=False)
    cooling_fan_no1 = forms.FloatField(required=False)
    cooling_fan_no2 = forms.FloatField(required=False)

    jet_pump_no1 = forms.CharField(required=False)
    jet_pump_no2 = forms.CharField(required=False)


    def __init__(self, *args, **kwargs):
        super(TRQForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class JobForm(forms.ModelForm):
    part = forms.ModelChoiceField(
        queryset=PartMF.objects.all(),
        widget=autocomplete.ModelSelect2(url='part-autocomplete'),
        required=False
    )
    class Meta:
        model = Job
        #fields = "__all__"
        exclude = ('part', 'meta_data', 'created_by', 'updated_at', 'created_at', 'updated_by', 'main_furnance' )

JobPhotoFormSet = forms.inlineformset_factory(Job, JobPhoto, form=JobPhotoForm)
JobPhotoInpsectQFormSet = forms.inlineformset_factory(Job, JobPhotoInspectQ, form=JobPhotoInspectQForm)

class JobFurnanceForm(forms.ModelForm):

    class Meta:
        model = JobFurnance
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(JobFurnanceForm, self).__init__(*args, **kwargs)
        self.fields['furnance'].widget.attrs\
                .update({
                    'class': 'furnance-select'
                    })

class JobInspectionForm(forms.ModelForm):
    class Meta:
        model = JobInspection
        exclude =  ()

    def __init__(self, *args, **kwargs):
        super(JobInspectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_show_labels = False

JobInspectionFormSet = forms.inlineformset_factory(Job, JobInspection, form=JobInspectionForm)

class JobSettingForm(forms.ModelForm):
    class Meta:
        model = JobSetting
        exclude =  ()

    def __init__(self, *args, **kwargs):
        super(JobSettingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #self.helper.form_show_labels = False

JobSettingFormSet = forms.inlineformset_factory(Job, JobSetting, form=JobSettingForm)


class TRQFurnaneModelForm(forms.ModelForm):
    class Meta:
        model = JobFurnance
        fields = ('furnance', 'qcol1', 'qcol2')

    def __init__(self, *args, **kwargs):
        super(TRQFurnaneModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

JobJobFurnanceFormSet = forms.inlineformset_factory(Job, JobFurnance, form=JobFurnanceForm)

