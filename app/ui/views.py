from django.shortcuts import render, redirect,reverse
from .forms import ExampleForm, StdMakingForm, InfoForm, SettingMethodForm, ParamsFormSet, RustPreventForm, InspectForm, ShotBlastForm, SearchForm
from django.forms.models import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'ui/index_page.html')

def index2(request):
    searchForm = SearchForm()
    if request.method == "POST":
        form = StdMakingForm(request.POST)
        if form.is_valid():
            factory = form.cleaned_data['factory']
            messages.add_message(request, messages.INFO, 'Hello world. %s' % (factory), extra_tags="alert-box")
            return redirect(reverse('updateform') + "?factory=%s"%(factory))
    else:
        form = StdMakingForm()
    return render(request, 'ui/index.html', {'form': form, 'searchForm': searchForm})

def trialRevise(request):
    return render(request, 'ui/trial-revise.html')

def dashboard(request):
    return render(request, 'ui/dashboard.html')

def updateform(request):
    infof = InfoForm()
    settingMethodForm = SettingMethodForm()
    trqForm = ParamsFormSet(prefix="trq",initial=[{'param_name': 'temp'}, {'param_name': 'cp'}, {'param_name':'nh3'}, {'param_name': 'speed'}, {'param_name':'oil_temp'}, {'param_name': 'agitator'}])

    trtForm = ParamsFormSet(prefix="trt", initial=[{'param_name': 'temp'},  {'param_name': 'speed'}])
    quenchingForm = InspectForm(prefix='qnch')
    temperingForm = InspectForm(prefix='temper')
    rustForm = RustPreventForm()
    sbForm = ShotBlastForm(prefix='shotBlast')
    if request.method == "POST":
        infof = InfoForm(request.POST)
        print(request.POST)
        quenchingForm = InspectForm(request.POST, prefix='qnch')
        temperingForm = InspectForm(request.POST, prefix='temper')
        sbForm = ShotBlastForm(request.POST, prefix='shotBlast')
        trqForm = ParamsFormSet(request.POST, prefix='trq')
        trtForm = ParamsFormSet(request.POST, prefix='trt')


        settingMethodForm = SettingMethodForm(request.POST)
        if infof.is_valid():
            #print(infof.cleaned_data['doc_code'])
            #messages.add_message(request, messages.INFO, 'Info form valid')
            pass
        if settingMethodForm.is_valid():
            print("setting method valid")
        else:
            print("setting method invlid")

    return render(request, 'ui/updateform.html', {'infoForm': infof, 'settingMethodForm': settingMethodForm, 'trqForm': trqForm, 'trtForm': trtForm, 'rustForm': rustForm, 'quenchingForm': quenchingForm, 'temperingForm':temperingForm, 'sbForm': sbForm})

def test(request):
    ExampleFormset = formset_factory(ExampleForm, extra = 3)
    example_formset = ExampleFormset()
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ExampleForm()
    return render(request, 'ui/index.html', {'form': form, 'formset': example_formset})
