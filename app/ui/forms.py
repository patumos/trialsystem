from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import formset_factory

ACTION_CHOICES  = (
        ('Trial New', 'Trial (New)'),
        ('Trial Revise', 'Trial (Revise)'),
        ('Job Standard New', 'Job Standard(New)' ),
        ('Job Standard Revise', 'Job Standard(Revise)')
        )
class StdMakingForm(forms.Form):
    doc_code = forms.CharField(max_length=100, required=True)
    part_code = forms.CharField(max_length=100, required=True)
    factory = forms.ChoiceField(choices = (('A', 'A'), ('B', 'B')))
    furnance  = forms.ChoiceField(choices = (('F-1', 'F-1'), ('F-2', 'F-2')))
    actions = forms.ChoiceField(choices = ACTION_CHOICES)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Next', css_class='btn-info'))
        super(StdMakingForm, self).__init__(*args, **kwargs)

class InfoForm(forms.Form):
    doc_code = forms.CharField(max_length=100, required=True)
    part_code = forms.CharField(max_length=100, required=True)
    factory = forms.ChoiceField(choices = (('A', 'A'), ('B', 'B')))
    furnance  = forms.ChoiceField(choices = (('F-1', 'F-1'), ('F-2', 'F-2')))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    revision = forms.CharField(max_length=100, required=False)
    revision_comment = forms.CharField(widget=forms.Textarea, required=False)
    product_photos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(InfoForm, self).__init__(*args, **kwargs)

PARAM_NAMES = (
          ('temp', 'Temp(℃)'),
          ('cp', 'CP(%)'),
          ('nh3', 'NH3(m3/Hr)'),
          ('speed', 'Speed Time(Min)'),
          ('oil_temp', 'Oil Temp.(℃)'),
          ('agitator', 'Agitator(Hz)')
          )
class SearchForm(forms.Form):
    doc_code = forms.CharField(required=False)
    part_code = forms.CharField(required=False)
    bar_code = forms.CharField(required=False)
    part_name = forms.CharField(required=False)
    factory = forms.ChoiceField(choices = (('A', 'A'), ('B', 'B')))
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ParamsForm(forms.Form):
    param_name = forms.ChoiceField(choices = PARAM_NAMES)
    col1  = forms.FloatField(required=False)
    col2  = forms.FloatField(required=False)
    col3  = forms.FloatField(required=False)
    col4  = forms.FloatField(required=False)
    col5  = forms.FloatField(required=False)
    all_same = forms.BooleanField(required=False)
    '''
    col6  = forms.FloatField(required=False)
    col7  = forms.FloatField(required=False)
    col8  = forms.FloatField(required=False)
    col9  = forms.FloatField(required=False)
    col10  = forms.FloatField(required=False)
    '''
    def __init__(self, *args, **kwargs):
        super(ParamsForm, self).__init__(*args, **kwargs)
        self.fields['param_name'].widget.attrs['disabled'] = False



ParamsFormSet = formset_factory(ParamsForm, extra=0)

class RustPreventForm(forms.Form):
    need = forms.BooleanField(required=False)
    material = forms.ChoiceField(choices=(('Rustkote 943', 'Rustkote 943'), ('Mat B', 'Mat B')))

class SettingMethodForm(forms.Form):
    CHOICES=[('handSetting','Hand Setting'),
                     ('hopper','Hopper')]

    method = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pieces_per_row = forms.FloatField(required=False)
    row_width = forms.FloatField(required=False)

    charge_rate  = forms.FloatField(required=False)
    chart_time  = forms.FloatField(required=False)
    total_weight  = forms.FloatField(required=False)
    vibration_level  = forms.FloatField(required=False)
    dumming_shutter_high  = forms.FloatField(required=False)


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(SettingMethodForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        method = data.get('method', None)
        charge_rate = data.get('charge_rate', None)
        pieces_per_row = data.get('pieces_per_row', None)
        print("method")
        if method  == 'hopper':
            if charge_rate is None or charge_rate == "":
                print("charge rate = " + str(charge_rate))
                raise forms.ValidationError('charge rate required !!')
        if method == "handSetting":
            if pieces_per_row is None:
                raise forms.ValidationError("pieces per row required")

class InspectForm(forms.Form):
    surfacePd = forms.IntegerField(required=False)
    corePd = forms.IntegerField(required=False)
    surface_minValue = forms.FloatField(required=False)
    surface_maxValue = forms.FloatField(required=False)
    core_minValue = forms.FloatField(required=False)
    core_maxValue = forms.FloatField(required=False)
    sentQA = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(InspectForm, self).__init__(*args, **kwargs)

class ShotBlastForm(forms.Form):
    machine = forms.ChoiceField(choices=(('ma1', 'Machine1'), ('ma2', 'Machine2')))
    media_size = forms.CharField(required=False, max_length=100)
    load = forms.FloatField(required=False)
    time = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(ShotBlastForm, self).__init__(*args, **kwargs)

class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        #self.helper.form_tag = False

        self.helper.add_input(Submit('submit', 'Submit'))
        super(ExampleForm, self).__init__(*args, **kwargs)
