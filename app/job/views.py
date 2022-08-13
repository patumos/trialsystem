from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Job, JobFurnance, JobSetting, SettingPhoto, ShotBlast, SbPhoto, JobExportData, JobFurnanceFile
from master.models import PartMF, Customer, ConstantMF, Furnance
from dal import autocomplete
from django.forms.models import modelform_factory
from django.views import View
from .forms import SearchPartForm, JobForm, JobJobFurnanceFormSet, TRQForm,\
        FurnanceForm, TRQFurnaneModelForm, JobPhotoFormSet, JobPhotoInpsectQFormSet, JobInspectionFormSet, JobSettingFormSet
from django.db import transaction
from django.contrib import messages
import re
from django.http import JsonResponse
import json
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.db.models import Q
from .utils import generateExportFile

import django_filters

TEMPLATE_LIST = (
            "conveyor","batch-tvq", "batch-tvt", "batch-tfq_tft", "batch-tgc_trgc", "batch-tbt",
            "batch-tih", "batch-tsz", "batch-tsp_tsap"
        )
# Create your views here.
@login_required
def jobpost(request):
    temp = None
    if request.method == "POST":
        form = TRQForm(request.POST)
        if form.is_valid():
            j = JobFurnance()
            j.furnance = form.cleaned_data['furnance']
            del form.cleaned_data['furnance']
            j.body = form.cleaned_data
            j.save()
            return render(request, "job/jobpost.html", {'form': form, 'object': j})
    else:
        form = TRQForm()
        return render(request, "job/jobpost.html", {'form': form, 'temp': temp})

@login_required
def index(request):
    return render(request, 'job/index.html')

class TrialJobNew(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        part = PartMF.objects.get(pk = request.POST.get('part'))
        j = Job()
        j.part = part
        print("current user")
        print(request.user)
        j.created_by = request.user
        j.meta_data = {'parent': [], 'info': {}}
        try:
            j.save()
            for temp in TEMPLATE_LIST:
                jf = JobFurnance()
                jf.template_name = temp
                jf.job = j
                jf.save()

            return redirect("job-edit", pk = j.pk)
        except:
            messages.error(request, j.errors)
            return redirect("job-prepare")
class TrialView(View):
    def get(self, request, *args, **kwargs):
        searchForm = SearchPartForm()
        return render(request, "job/prepare.html", {'searchForm': searchForm})

    def post(self, request, *args, **kwargs):
        searchForm = SearchPartForm(request.POST)
        if searchForm.is_valid():
            part = searchForm.cleaned_data['part']
            job = Job()
            job.part = part

            jobForm = JobForm(instance = job)
            customer = Customer.objects.get(code = part.custom_no)
            constant = None
            jobs = Job.objects.filter(part = part)
            if part.shtester3 is not None:
                print(part.shtester3)
                try:
                    constant = ConstantMF.objects.get(data_code = part.shtester3, class_code=7)
                except ConstantMF.DoesNotExist:
                    pass

            coolConst = None
            if part.chtester1 is not None:
                try:
                    coolConst = ConstantMF.objects.get(data_code = part.chtester1, class_code = 7)
                except ConstantMF.DoesNotExist:
                    pass

            coolConst2 = None
            if part.chtester2 is not None:
                try:
                    coolConst2 = ConstantMF.objects.get(data_code = part.chtester2, class_code = 7)
                except ConstantMF.DoesNotExist:
                    pass

            otherCon = None
            if part.othertester is not None:
                try:
                    otherCon = ConstantMF.objects.get(data_code = part.othertester, class_code = 7)
                except ConstantMF.DoesNotExist:
                    pass

            effpoint = None
            if part.effpoint1 is not None and part.effpoint1 != 0:
                try:
                    effpoint  = ConstantMF.objects.get(data_code = part.effpoint1, class_code = 8)
                except ConstantMF.DoesNotExist:
                    pass

            effpoint2 = None
            if part.effpoint2 is not None and part.effpoint2 != 0:
                try:
                    effpoint2  = ConstantMF.objects.get(data_code = part.effpoint2, class_code = 8)
                except ConstantMF.DoesNotExist:
                    pass

            return render(request, "job/prepare.html", {'searchForm': searchForm, 'part': part, 'customer': customer, 'const': constant, 'coolConst': coolConst, 'coolConst2': coolConst2, 'otherCon': otherCon, 'effpoint': effpoint, 'effpoint2': effpoint2, 'jobForm': jobForm, 'jobs': jobs})

class JobFilter(django_filters.FilterSet):
    part__partcode = django_filters.CharFilter(lookup_expr='icontains', label="Part code contains")
    part__doc_code = django_filters.CharFilter(lookup_expr='icontains', label="Doc code contains")
    version_code = django_filters.CharFilter(lookup_expr='icontains')
    rev_note = django_filters.CharFilter(lookup_expr='icontains')
    c_no = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Job
        fields = ['part__partcode', 'part__doc_code','version_code', 'rev_note', 'c_no']

class JobListView(ListView):
    model = Job
    paginate_by  = 50
    ordering = ['-id',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.model.objects.count()

        listFilter  = JobFilter(self.request.GET)
        context['filter'] = listFilter
        return context

    def get_queryset(self):
        object_list =  self.model.objects.all().order_by('-id')
        listFilter = JobFilter(self.request.GET, queryset=object_list)
        return listFilter.qs

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('page_size', self.paginate_by)

class JobCreateView(SuccessMessageMixin,CreateView):
    model = Job
    form_class = modelform_factory(Job,
            exclude = ('created_by', 'udpated_by'),
            widgets = {
                'part': autocomplete.ModelSelect2(url='part-autocomplete'),
            })

    success_message = "%(part)s was created successfully"


@never_cache
@csrf_exempt
def loadjobfurnance(request, pk):
    from django.core import serializers

    job = Job.objects.get(pk = pk)
    jf2 = job.jobfurnance_set.all().values('id', 'job', 'furnance','furnance__furnance', 'furnance__qcol1',  'furnance__qcol2', 'furnance__qcol3', "furnance__qcol4", "furnance__qcol5",
            "furnance__qcol6", "furnance__qcol7", "furnance__qcol8",  "furnance__tcol1", "furnance__tcol2",
            "furnance__tcol3", "furnance__tcol4", "furnance__tcol4", "furnance__tcol5", "furnance__tcol5",
            "furnance__tcol6", "furnance__template_name", "furnance__params", 'furnance__tparams',"furnance__enable_qcols", "furnance__enable_tcols",    'keys', 'values', 'is_batch', 'batch_values', 'template_name')
    #print(jf2)
    if request.method == "POST":
        #print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data  = body['data']
        if body['action'] == "save":

            jf = JobFurnance.objects.get(pk = data['id'])
            jf.values = data['values']

            if 'enable' in data:
                jf.enable = data['enable']

            if 'is_batch' in data:
                jf.is_batch = data['is_batch']

            if 'batch_values' in data:
                jf.batch_values = data['batch_values']

            jf.save()
        elif body['action'] == "getData":
            if 'id' in data:
                jf = JobFurnance.objects.filter(pk = data['id']).values('id', 'job', 'furnance','furnance__furnance', 'furnance__qcol1',  'furnance__qcol2', 'furnance__qcol3', "furnance__qcol4", "furnance__qcol5",
                "furnance__qcol6", "furnance__qcol7", "furnance__qcol8",  "furnance__tcol1", "furnance__checkq_1", "furnance__checkt_2", "furnance__tcol2",
                "furnance__tcol3", "furnance__tcol4", "furnance__tcol4", "furnance__tcol5", "furnance__tcol5",
                "furnance__tcol6", "furnance__template_name", "furnance__params", 'furnance__tparams',"furnance__enable_qcols", "furnance__enable_tcols",    'keys', 'values', 'is_batch', 'batch_values', 'template_name', 'enable')

                return JsonResponse(list(jf), safe=False)
            else:
                return JsonResponse({'id': 'error'},safe=False)

        elif body['action'] == 'updateFurnance':
            jf = JobFurnance.objects.get(pk = data['id'])
            furnance = Furnance.objects.get(pk = data['furnance_id'])
            jf.furnance = furnance
            jf.save()

            job.main_furnance = furnance
            job.save()

        elif body['action'] == "delete":
            JobFurnance.objects.get(pk = data['id']).delete()


        return JsonResponse({'success': True}, safe=False)
    #serialized_obj = serializers.serialize('json', [ jf ])
    return JsonResponse(list(jf2), safe=False)


@csrf_exempt
@login_required
def job_api(request, pk):
    from django.core import serializers
    jf = Job.objects.filter(pk = pk).values('id', 'main_furnance__furnance', 'main_furnance__coveyor_length', 'main_furnance__max_weight_value',  'main_furnance', 'part', 'part__kgperpc', 'part__designno')
    return JsonResponse(list(jf), safe=False)

@csrf_exempt
@login_required
def jobfurnance_api(request, pk):
    from django.core import serializers
    jf = JobFurnance.objects.filter(job_id = pk).values('enable', 'template_name')
    return JsonResponse(list(jf), safe=False)

@csrf_exempt
@login_required
def job_add_jf(request, pk):
    job = Job.objects.get(pk=pk)
    jf = JobFurnance()

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        template = body['template']
        jf.template_name = template
        jf.job = job
        jf.save()
        jfs = job.jobfurnance_set.all().values('id', 'job', 'furnance','furnance__furnance', 'furnance__qcol1',  'furnance__qcol2', 'furnance__qcol3', "furnance__qcol4", "furnance__qcol5",
            "furnance__qcol6", "furnance__qcol7", "furnance__qcol8",  "furnance__tcol1", "furnance__tcol2",
            "furnance__tcol3", "furnance__tcol4", "furnance__tcol4", "furnance__tcol5", "furnance__tcol5",
            "furnance__tcol6", "furnance__template_name", "furnance__params", 'furnance__tparams',"furnance__enable_qcols", "furnance__enable_tcols",    'keys', 'values', 'is_batch', 'batch_values', 'template_name')
        return JsonResponse(list(jfs), safe=False)

@csrf_exempt
@login_required
def export_api(request, pk):
    #list exported files
    job = Job.objects.get(pk=pk)
    if request.method == "GET":
        exports = job.jobexportdata_set.all().order_by('-created_at').values('path', 'created_at', 'created_by__username', 'revision_code','id', 'template', 'job__c_no', 'job__version_code')
        return JsonResponse(list(exports), safe=False)

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        #body = json.loads(body_unicode)
        #template = body['template']

        if  job.jobfurnance_set.all().count()  > 0:

            #template = job.jobfurnance_set.all()[0].template_name
            jed = JobExportData()
            jed.job = job
            #jed.template = template
            jed.path = generateExportFile(pk)
            jed.revision_code = job.version_code
            jed.created_by = request.user
            jed.save()
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok':False}, status=400)


@never_cache
@csrf_exempt
@login_required
def jobsetting_api(request, pk):
    jo = Job.objects.get(pk=pk)
    jobSettings = jo.jobsetting_set.all().values('id', 'setting_type', 'values')
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        jobSettingId = body['id']
        data = body['data']
        #print(body)
        try:
            o = JobSetting.objects.get(pk = jobSettingId)
            #print(o)
            #print(data)
            o.values = data
            o.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False}, status=400)

    return JsonResponse(list(jobSettings), safe=False)

@csrf_exempt
@login_required
def sb_api(request, pk):
    jo = Job.objects.get(pk=pk)
    sbs = jo.shotblast_set.all().values('id', 'sb_type', 'values')
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        sbid = body['id']
        data = body['data']
        #print(body)
        try:
            o = ShotBlast.objects.get(pk = sbid)
            #print(o)
            #print(data)
            o.values = data
            o.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False}, status=400)

    return JsonResponse(list(sbs), safe=False)

@csrf_exempt
@login_required
def list_sb(request, pk):
    jo = Job.objects.get(pk=pk)
    sb = jo.shotblast_set.all().values("id", "sb_type", "furnance","ptn_no", "time_op", "kg_time", "values")


    return JsonResponse(list(sb), safe=False)

@never_cache
@csrf_exempt
@login_required
def job_createsetting(request, pk):
    from django.core import serializers
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data  = body['data']
        jf = Job.objects.get(pk = pk)
        js = JobSetting()
        js.job = jf
        js.setting_type = data['settingType']
        try:
            js.save()
            return JsonResponse({'ok':1})
        except Exception as e:
            return JsonResponse(status=400)

@csrf_exempt
@login_required
def createSb(request, pk):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        data  = body['data']
        jf = Job.objects.get(pk = pk)
        js = ShotBlast()
        js.job = jf
        js.sb_type = data['type']
        try:
            js.save()
            return JsonResponse({'ok':1})
        except Exception as e:
            return JsonResponse(status=400)

@csrf_exempt
@login_required
def job_delete_setting(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        jobid  = body['id']
        jf = JobSetting.objects.filter(pk=jobid).delete()
        return JsonResponse({'ok': True})

@csrf_exempt
@login_required
def sb_delete(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        jobid  = body['id']
        jf = ShotBlast.objects.filter(pk=jobid).delete()
        return JsonResponse({'ok': True})

@never_cache
@login_required
def job_revision(request, pk):
    parentJob = Job.objects.get(pk = pk)
    newJob = Job.objects.get(pk=pk)
    newJob.pk = None
    newJob.parent_job = parentJob
    #newJob.version_code = parentJob.version_code + 1
    newJob.created_by = request.user
    newJob.updated_by = request.user
    print(f"new job {newJob.meta_data['parent']}")
    newJob.meta_data['parent'].append({'id': parentJob.id, 'version_code': parentJob.version_code})
    newJob.save()
    for j in parentJob.jobfurnance_set.all():
        j.job = newJob
        j.pk = None
        j.save()

    for j in parentJob.jobsetting_set.all():
        oldPK = j.pk
        setPhotos = j.settingphoto_set.all()
        j.job = newJob
        j.pk = None
        j.save()

        for sp in setPhotos:
            sp.pk = None
            sp.setting = j
            sp.save()

    for j in parentJob.shotblast_set.all():
        oldPK = j.pk
        setPhotos = j.sbphoto_set.all()
        j.job = newJob
        j.pk = None
        j.save()

        for sp in setPhotos:
            sp.pk = None
            sp.sb = j
            sp.save()

    '''
    for j in parentJob.shotblast_set.all():
        j.job = newJob
        j.pk = None
        j.save()
    '''

    for j in parentJob.jobinspection_set.all():
        j.job = newJob
        j.pk = None
        j.save()
    '''
    for j in parentJob.jobexportdata_set.all():
        j.job = newJob
        j.pk = None
        j.save()
    '''

    for j in parentJob.inspectionphoto_set.all():
        j.job = newJob
        j.pk = None
        j.save()

    for j in parentJob.jobphoto_set.all():
        j.job = newJob
        j.pk = None
        j.save()

    for j in parentJob.jobphotoinspectq_set.all():
        j.job = newJob
        j.pk = None
        j.save()

    return redirect("job-edit", pk = newJob.pk)

'''
    @login_required
    @csrf_exempt
    def get_setting_photos(request):
        if request.method == "POST":
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            settingId = body['id']
            jobSetting = JobSetting.objects.get(pk = settingId)
            photos = jobSetting.setting_photo_set.all()
            return JsonResponse(list(photos), safe=True)
'''

@login_required
@csrf_exempt
def create_setting_photo(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = JobSetting.objects.get(pk = body['id'])
        settingPhoto = SettingPhoto()
        settingPhoto.setting = js
        settingPhoto.group = body['group']
        try:
            settingPhoto.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            print(e)
            return JsonResponse({'ok': False}, status=400)

@login_required
@csrf_exempt
def delete_setting_photo(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = SettingPhoto.objects.get(pk = body['id']).delete()
        return JsonResponse({'ok': True})

@login_required
@csrf_exempt
def create_sb_photo(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = ShotBlast.objects.get(pk = body['id'])
        sbPhoto = SbPhoto()
        sbPhoto.sb = js
        sbPhoto.group = body['group']
        try:
            sbPhoto.save()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False}, status=400)

@login_required
@csrf_exempt
def delete_sb_photo(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = SbPhoto.objects.get(pk = body['id']).delete()
        return JsonResponse({'ok': True})

@csrf_exempt
@login_required
def photo_api(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        action = body['action']

        if action == "list":
            jf = JobFurnance.objects.get(pk = body['id'])
            files = jf.jobfurnancefile_set.all().values("group", "file", "caption", "order", "id")
            return JsonResponse(list(files), safe=False)

        elif action == "update":
            try:
                jf = JobFurnanceFile.objects.get(pk = body['id'])
                jf.caption = body['data']['caption']
                jf.save()
                return JsonResponse({'ok': True})
            except:
                return JsonResponse({"ok": False})

        elif action == "delete":
            jf = JobFurnanceFile.objects.get(pk = body['id']).delete()
            return JsonResponse({'ok': True})

        elif action == "create":
            jf = JobFurnance.objects.get(pk = body['id'])
            afile = JobFurnanceFile()
            afile.jobFurnance = jf
            afile.group = body['group']

            try:
                afile.save()
                return JsonResponse({'ok': True})
            except:
                return JsonResponse({'ok': False}, status=400)

@login_required
@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        js = JobFurnanceFile.objects.get(pk = request.POST.get('id', None))
        #js.group = request.POST.get('group', None)
        js.file  = request.FILES['file']
        print(js.id)
        try:
            js.save()
            return JsonResponse({'ok': True}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'ok': False})

@login_required
@csrf_exempt
def get_setting_photo(request):
    if request.method == "POST":
        #print(request.POST)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = JobSetting.objects.get(pk=body['id'])
        photos = js.settingphoto_set.all().values('group', 'file', 'caption', 'id')
        return JsonResponse(list(photos), safe=False)

@login_required
@csrf_exempt
def get_sb_photo(request):
    if request.method == "POST":
        print(request.POST)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = ShotBlast.objects.get(pk=body['id'])
        photos = js.sbphoto_set.all().values('group', 'file', 'caption', 'id')
        return JsonResponse(list(photos), safe=False)

@login_required
@csrf_exempt
def update_setting_photo_data(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = SettingPhoto.objects.get(pk=body['id'])
        js.caption = body['data']['caption']
        try:
            js.save()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False})

@login_required
@csrf_exempt
def update_sbphoto_data(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        js = SbPhoto.objects.get(pk=body['id'])
        js.caption = body['data']['caption']
        try:
            js.save()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False})

@login_required
@csrf_exempt
def update_setting_photo(request):
    if request.method == "POST":
        js = SettingPhoto.objects.get(pk = request.POST.get('id', None))
        js.file  = request.FILES['file']
        try:
            js.save()
            return JsonResponse({'ok': True}, safe=False)
        except:
            return JsonResponse({'ok': False})

@login_required
@csrf_exempt
def upload_sb_photo(request):
    if request.method == "POST":
        js = SbPhoto.objects.get(pk = request.POST.get('id', None))
        js.file  = request.FILES['file']
        try:
            js.save()
            return JsonResponse({'ok': True}, safe=False)
        except:
            return JsonResponse({'ok': False})

@never_cache
@login_required
def furnance_list(request):
    f = Furnance.objects.all().values("id", "furnance", "qcol1")
    return JsonResponse(list(f), safe=False)

@never_cache
@login_required
def jobedit(request, pk):
    obj = get_object_or_404(Job, pk = pk)
    raw_obj = get_object_or_404(Job, pk = pk)
    #print(obj.jobfurnance_set.all())
    f1 = FurnanceForm()
    jobf = JobForm(instance = obj)
    part = obj.part
    customer = Customer.objects.get(code = part.custom_no)
    furnance_forms = []
    jfs = list(obj.jobfurnance_set.all())
    jobPhotoForms = JobPhotoFormSet(instance = obj)
    jobPhotoQForms = JobPhotoInpsectQFormSet(instance = obj)
    jobInspectionForms = JobInspectionFormSet(instance = obj)
    #print("jobedit")
    #print(request.method)
    constant = None
    if part.shtester3 is not None:
        #print(part.shtester3)
        try:
            constant = ConstantMF.objects.get(data_code = part.shtester3, class_code=7)
        except ConstantMF.DoesNotExist:
            pass

    coolConst = None
    if part.chtester1 is not None:
        try:
            coolConst = ConstantMF.objects.get(data_code = part.chtester1, class_code = 7)
        except ConstantMF.DoesNotExist:
            pass

    coolConst2 = None
    if part.chtester2 is not None:
        try:
            coolConst2 = ConstantMF.objects.get(data_code = part.chtester2, class_code = 7)
        except ConstantMF.DoesNotExist:
            pass

    otherCon = None
    if part.othertester is not None:
        try:
            otherCon = ConstantMF.objects.get(data_code = part.othertester, class_code = 7)
        except ConstantMF.DoesNotExist:
            pass

    effpoint = None
    if part.effpoint1 is not None and part.effpoint1 != 0:
        try:
            effpoint  = ConstantMF.objects.get(data_code = part.effpoint1, class_code = 8)
        except ConstantMF.DoesNotExist:
            pass

    effpoint2 = None
    if part.effpoint2 is not None and part.effpoint2 != 0:
        try:
            effpoint2  = ConstantMF.objects.get(data_code = part.effpoint2, class_code = 8)
        except ConstantMF.DoesNotExist:
            pass
    for jf in obj.jobfurnance_set.all():
        if jf.furnance is not None and  jf.furnance.furnance.find("TRQ") != -1:
            furnance_forms.append(TRQFurnaneModelForm(instance = jf))
    if request.is_ajax():
        if request.method == "POST":
            #print("raw data %s " % request.body)
            jfid = request.POST.get('jfid')
            pd = request.POST
            jfo = JobFurnance.objects.get(pk = jfid)
            jfo.qcol1 = pd.get('qcol1')
            jfo.qcol2 = pd.get('qcol2')
            #print(pd.get('temp[Zone1]'))
            try:
                jfo.save()
            except:
                return JsonResponse({'error': jfo.errors}, status=400)
            return JsonResponse({'foo': 'bar'})
    if request.method == "POST":
        #print("furnance form")
        #print(request.POST)
        furnance_form = request.POST.get('formdata')
        #print(furnance_form)
        f1 = FurnanceForm(request.POST)


        if f1.is_valid():
            #print("valid f1")
            furnance = f1.cleaned_data['furnance']
            #print(furnance)
            jf = JobFurnance()
            jf.job = obj
            jf.furnance = furnance
            jf.keys = ["temp", "cp", "nh"]
            #print(obj)
            #print(jf.job)
            #print(jf.furnance)
            try:
                jf.save()
                messages.success(request, "Job furnance success")
            except Exception as e:
                messages.error(request, e.msg)
            return redirect("job-edit", pk=pk)

        print("Job form ")

        jobf = JobForm(request.POST, instance = obj )
        #:print(f"part = {part}")
        if jobf.is_valid():
            print("form valid")
            try:
                part = jobf.cleaned_data['part']
                #print(f"part = {part}")
                obj = jobf.save(commit=False)
                if part:
                    obj.part  = part
                obj.updated_by = request.user
                obj.save()
                messages.success(request, "Save Success")
            except Exception as e:
                print("form cannot save")
                messages.error(request, e.msg)
        else:
            print("form invalid")
            messages.error(request, jobf.errors)



        try:
            jobPhotoForms = JobPhotoFormSet(request.POST, request.FILES, instance = obj)
            if jobPhotoForms.is_valid():
                jobPhotoForms.save()
            else:
                messages.error(request, jobPhotoForms.errors)

            jobPhotoQForms = JobPhotoInpsectQFormSet(request.POST, request.FILES, instance = obj)
            if jobPhotoQForms.is_valid():
                jobPhotoQForms.save()
            else:
                messages.error(request, jobPhotoQForms.errors)
        except:
            pass

        jobInspections = JobInspectionFormSet(request.POST, request.FILES, instance = obj)
        if jobInspections.is_valid():
            jobInspections.save()
        else:
            messages.error(request, jobInspections.errors)

        if 'delete-furnance' in request.POST:
            furnance_id = request.POST.get('furnance-id', None)
            JobFurnance.objects.get(pk=int(furnance_id)).delete()

        return redirect("job-edit", pk=pk)

    return render(request, "job/job_edit.html", {'f1':f1, 'obj': obj, 'jobf': jobf, 'furnace_forms': furnance_forms, 'jfs': jfs, 'part': part, 'customer': customer, 'jobPhotoForms': jobPhotoForms, 'jobPhotoQForms': jobPhotoQForms, 'jobInspectionForms': jobInspectionForms,
        'const': constant, 'coolConst': coolConst, 'coolConst2': coolConst2, 'otherCon': otherCon, 'effpoint': effpoint, 'effpoint2': effpoint2})

class JobEditView(SuccessMessageMixin, UpdateView):
    model = Job
    fields = "__all__"
    success_message = "%(part)s was updated successfully"
    def form_valid(self, form):
        context = self.get_context_data()
        #formset = context['formset']
        #trqForm = context['trqForm']
        furnanceForm = context['furnance_form']
        print(furnanceForm)
        if furnanceForm.is_valid():
            print("furnance form")
            jf = JobFurnance()
            jf.job = self.object
            jf.furnance = jf.cleaned_data['furnance']
            try:
                jf.save()
            except:
                print("cannot save furnance form")
        return super(JobEditView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)

        part = self.object.part
        customer = Customer.objects.get(code = self.object.part.custom_no)
        constant = None
        if self.object.part.shtester3 is not None:
            print(part.shtester3)
            try:
                constant = ConstantMF.objects.get(data_code = part.shtester3, class_code=7)
            except ConstantMF.DoesNotExist:
                pass

        context['constant'] = constant
        coolConst = None
        if part.chtester1 is not None:
            try:
                coolConst = ConstantMF.objects.get(data_code = part.chtester1, class_code = 7)
            except ConstantMF.DoesNotExist:
                pass

        context['coolConst'] = coolConst
        coolConst2 = None
        if part.chtester2 is not None:
            try:
                coolConst2 = ConstantMF.objects.get(data_code = part.chtester2, class_code = 7)
            except ConstantMF.DoesNotExist:
                pass

        context['coolConst2'] = coolConst2
        otherCon = None
        if part.othertester is not None:
            try:
                otherCon = ConstantMF.objects.get(data_code = part.othertester, class_code = 7)
            except ConstantMF.DoesNotExist:
                pass

        context['otherCon'] = otherCon
        effpoint = None
        if part.effpoint1 is not None and part.effpoint1 != 0:
            try:
                effpoint  = ConstantMF.objects.get(data_code = part.effpoint1, class_code = 8)
            except ConstantMF.DoesNotExist:
                pass

        context['effpoint'] = effpoint
        effpoint2 = None
        if part.effpoint2 is not None and part.effpoint2 != 0:
            try:
                effpoint2  = ConstantMF.objects.get(data_code = part.effpoint2, class_code = 8)
            except ConstantMF.DoesNotExist:
                pass

        context['effpoint2'] = effpoint2
        context['part'] = part
        context['furnance_form'] = FurnanceForm()
        if self.request.POST:
            formset  = JobJobFurnanceFormSet(self.request.POST, instance = self.object)
            context['formset'] = formset
            context['furnance_form'] = FurnanceForm(self.request.POST)
        else:
            context['trqForm'] = TRQForm()
            print("In get")
            formset  = JobJobFurnanceFormSet(instance = self.object)
            #reg math add furnance-xx
                #find post hast that object ?
                # show only enable fields
            for i in range(len(formset)):
            #for f in formset:
                if formset[i].instance.furnance is not None:
                    fh  = formset[i].instance.furnance.get_hidden_fields()
                    for k, v in fh.items():
                        print("%d %s" % (i,k))
                        formset[i].fields[k].widget = forms.HiddenInput()
                        print(formset[i].fields[k])


        return context



class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("job-list")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)



class PartAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = PartMF.objects.all()

        if self.q:
            qs = qs.filter(Q(doc_code__icontains = self.q) | Q(partcode__icontains=self.q))

        return qs


class JobFurnanceCreateView(SuccessMessageMixin,CreateView):
    model = JobFurnance

    success_message = "%(job)s was created successfully"

    fields = ("job", "furnance",)
