from django.forms import ModelForm, inlineformset_factory
from .models import PartPhoto, PartMF

class PartPhotoForm(ModelForm):
    class Meta:
        model = PartPhoto
        exclude = ()

PartPhotoFormSet = inlineformset_factory(PartMF, PartPhoto, form=PartPhotoForm)
