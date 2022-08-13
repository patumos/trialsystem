from django import forms
from django.forms.widgets import DateInput
from .models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django.forms.utils import ErrorList
CHOICES = (('Not Spec', ''),)
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '''
<div id="card-alert" class="card red lighten-5">
                    <div class="card-content red-text">
			%s
                    </div>
                    <button type="button" class="close red-text" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">×</span>
                    </button>
                  </div>
    ''' % ''.join(['<p>%s</p>' % e for e in self])
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        '''
        labels = {
            "first_name": _("First Name")
        }
        '''

class ProfileForm(forms.ModelForm):
    '''
    birth_date = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d', attrs={'class': 'datepicker'}),
            input_formats=('%Y-%m-%d',),localize=False)
    '''

    def __init__(self, *args, **kwargs):
        kwargs_new = {'error_class': DivErrorList}
        kwargs_new.update(kwargs)
        super(ProfileForm, self).__init__(*args, **kwargs_new)

    class Meta:
        model = Profile
        fields = ('staff_roles',)
