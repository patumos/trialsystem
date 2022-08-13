from django.db import models
from django.urls import reverse
# Create your models here.
from multiselectfield import MultiSelectField
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from model_clone import CloneMixin
from django_cloneable import CloneableMixin
from .prevalues import INSP_ITEMS

SAFETY_CHOICES = (
        ('helmet', 'หมวกพนักงาน'),
        ('safety_shoes', 'รองเท้า Safety'),
        ('glass', 'แว่นตา'),
        ('ear_cover', 'ที่ครอบหู'),
        ('ear_fill', 'ที่อุดหู'),
        ('belt', 'เข็มขัดนิรภัย'),
        ('nose', 'ผ้าปิดจมูก'),
        ('glove', 'ถุงมือยาง'),
        ('eam', 'เอี้ยม'),
        ('glove_c', 'ถุงมือผ้า'),
        ('arm', 'ปลอกแขนทางความร้อน'),
        ('back', 'แผ่นรองหลัง'),
        ('other', 'อื่นๆ'),
        )

class JobValues(models.Model):
    jobfurnance = models.ForeignKey('JobFurnance', on_delete=models.SET_NULL, null=True)
    topicName = models.CharField(max_length=40, blank=False, null=False, default="")
    colName = models.CharField(max_length=40, blank=False, null=True, default="")
    fvalue = models.FloatField(blank=True, null=True)
    tvalue = models.CharField(max_length=200, blank=True, null=True)

class JobFurnance(models.Model):
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True)
    enable = models.BooleanField(blank=True, default=False)
    body = JSONField(blank=True, null=True)
    furnance = models.ForeignKey('master.Furnance', on_delete=models.SET_NULL, null=True)
    qcol1 = models.CharField(max_length=100,  blank=True, null=True)
    qcol2 = models.CharField(max_length=100,  blank=True, null=True)
    qcol3 = models.CharField(max_length=100,  blank=True, null=True)
    qcol4 = models.CharField(max_length=100,  blank=True, null=True)
    qcol5 = models.CharField(max_length=100,  blank=True, null=True)
    qcol6 = models.CharField(max_length=100,  blank=True, null=True)
    qcol7 = models.CharField(max_length=100,  blank=True, null=True)
    qcol8 = models.CharField(max_length=100,  blank=True, null=True)
    tcol1 = models.CharField(max_length=100,  blank=True, null=True)
    tcol2 = models.CharField(max_length=100,  blank=True, null=True)
    tcol3 = models.CharField(max_length=100,  blank=True, null=True)
    tcol4 = models.CharField(max_length=100,  blank=True, null=True)
    tcol5 = models.CharField(max_length=100,  blank=True, null=True)
    tcol6 = models.CharField(max_length=100,  blank=True, null=True)
    checkq_1 = models.CharField(max_length=100, blank=True, null=True)
    checkt_2 = models.CharField(max_length=100,  blank=True, null=True)
    coveyor_length =  models.FloatField(blank=True, null=True)
    max_weight_value = models.FloatField(blank = True, null = True)
    max_weight_unit = models.CharField(max_length=20, blank=True, null=True)
    furtype  = models.CharField(max_length=40, blank=True, null=True)
    furno = models.CharField(max_length=4, blank=True, null=True)
    keys = JSONField(blank=True, null=True)
    values = JSONField(blank=True, null=True)
    is_batch = models.BooleanField(default=False, blank=True)
    batch_values = JSONField(blank=True, null=True)
    template_name = models.CharField(max_length=100, blank=False, null=True)

    def get_absolute_url(self):
        return reverse('jobfurnance-edit', kwargs={'pk': self.pk})



class JobPhoto(models.Model):
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to="jobphotos/")
    caption = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self,  *args, **kwargs):
        print("Save ...Photo")

        super(JobPhoto, self).save()
        image = Image.open(self.photo)

        (width, height) = image.size
        MAX_SIZE = 100
        "Max width and height 800"
        if (MAX_SIZE / width)  < ( MAX_SIZE / height):
            factor = MAX_SIZE / height
        else:
            factor = MAX_SIZE / width

        size = (int(width * factor), int(height * factor))
        print("job photo")
        print(size)
        #size = (600,400)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.photo.path)


class JobPhotoInspectQ(models.Model):
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to="jobphotos/")
    caption = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print("Save ...Photo")

        super(JobPhotoInspectQ, self).save()


        image = Image.open(self.photo)
        (width, height) = image.size
        MAX_SIZE = 100
        "Max width and height 800"
        if (MAX_SIZE / width)  < ( MAX_SIZE / height):
            factor = MAX_SIZE / height
        else:
            factor = MAX_SIZE / width

        size = ( int(width * factor), int(height * factor))
        print("job photo inspect")
        print(size)
        #size = (600,400)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.photo.path)


TESTER_CHOICES = (
    ('MHv10g.', 'MHv10g.'),
    ('MHv25g.', 'MHv25g.'),
    ('MHv50g.', 'MHv50g.'),
    ('MHv100g.', 'MHv100g.'),
    ('MHv200g.', 'MHv200g.'),
    ('MHv300g.', 'MHv300g.'),
    ('MHv500g.', 'MHv500g.'),
    ('MHv1Kg.', 'MHv1Kg.'),
    ('Hv5Kg.', 'Hv5Kg.'),
    ('Hv10Kg.', 'Hv10Kg.'),
    ('Hv20Kg.', 'Hv20Kg.'),
    ('Hv30Kg.', 'Hv30Kg.'),
    ('Hv50Kg.', 'Hv50Kg.'),
    ('HR15N', 'HR15N'),
    ('HR30N', 'HR30N'),
    ('HRA', 'HRA'),
    ('HRB', 'HRB'),
    ('HRC', 'HRC'),
    ('HS', 'HS'),
    ('HB', 'HB'),
    ('Micro scope (x50)', 'Micro scope (x50)'),
    ('Micro scope (x100)', 'Micro scope (x100)'),
    ('Micro scope (x400)', 'Micro scope (x400)'),
    ('Micro scope (x100,x400)', 'Micro scope (x100,x400)'),
    ('Micro scope (x500)', 'Micro scope (x500)')
)
class JobSetting(CloneMixin,models.Model):
    setting_type = models.CharField(max_length=100, blank=True, null=True)
    job = models.ForeignKey('Job', null=True, blank=True, on_delete=models.SET_NULL)
    values = JSONField(blank=True, null=True)

class ShotBlast(models.Model):
    sb_type = models.CharField(max_length=100, blank=True, null=True)
    job = models.ForeignKey('Job', null=True, blank=True, on_delete=models.SET_NULL)
    furnance = models.ForeignKey('master.Furnance', on_delete=models.SET_NULL, null=True, blank=True)
    ptn_no = models.IntegerField(blank=False, null=True)
    time_op = models.FloatField(blank=False, null=True)
    kg_time = models.FloatField(blank=False, null=True)
    values = JSONField(blank=True, null=True)

class SbPhoto(models.Model):
    group = models.CharField(max_length=100, blank=False,  null=False)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(blank=True, null=False, default=0)
    sb = models.ForeignKey('ShotBlast', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        super(SbPhoto, self).save()

        print(f"file = {self.file}")
        if self.file:
            image = Image.open(self.file)
            (width, height) = image.size
            MAX_SIZE = 200
            "Max width and height 800"
            if (MAX_SIZE / width)  < ( MAX_SIZE / height):
                factor = MAX_SIZE / height
            else:
                factor = MAX_SIZE / width

            size = ( int(width * factor), int(height * factor))
            print("job photo inspect")
            print(size)
            #size = (600,400)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.file.path)

class JobFurnanceFile(models.Model):
    group = models.CharField(max_length=100, blank=False,  null=False)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(blank=True, null=False, default=0)
    jobFurnance = models.ForeignKey('JobFurnance', null=True, blank=True, on_delete=models.SET_NULL)

    def save_2(self, *args, **kwargs):

        super(JobFurnanceFile, self).save()


        image = Image.open(self.file)
        (width, height) = image.size
        MAX_SIZE = 100
        "Max width and height 800"
        if (MAX_SIZE / width)  < ( MAX_SIZE / height):
            factor = MAX_SIZE / height
        else:
            factor = MAX_SIZE / width

        size = ( int(width * factor), int(height * factor))
        print("job photo inspect")
        print(size)
        #size = (600,400)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.file.path)

class SettingPhoto(models.Model):
    group = models.CharField(max_length=100, blank=False,  null=False)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(blank=True, null=False, default=0)
    setting = models.ForeignKey('JobSetting', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        super(SettingPhoto, self).save()

        print(f"file = {self.file}")
        if self.file:
            image = Image.open(self.file)
            (width, height) = image.size
            MAX_SIZE = 100
            "Max width and height 800"
            if (MAX_SIZE / width)  < ( MAX_SIZE / height):
                factor = MAX_SIZE / height
            else:
                factor = MAX_SIZE / width

            size = ( int(width * factor), int(height * factor))
            print("job photo inspect")
            print(size)
            #size = (600,400)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.file.path)

class InspectionPhoto(models.Model):
    group = models.CharField(max_length=100, blank=False,  null=False)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(blank=True, null=False, default=0)
    job = models.ForeignKey('Job', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        super(InspectionPhoto, self).save()


        image = Image.open(self.file)
        (width, height) = image.size
        MAX_SIZE = 100
        "Max width and height 800"
        if (MAX_SIZE / width)  < ( MAX_SIZE / height):
            factor = MAX_SIZE / height
        else:
            factor = MAX_SIZE / width

        size = ( int(width * factor), int(height * factor))
        print("job photo inspect")
        print(size)
        #size = (600,400)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.file.path)

class JobInspection(models.Model):
    job = models.ForeignKey('Job', null=True, blank=True, on_delete=models.SET_NULL)
    inspection_item  = models.CharField(max_length=100, choices = INSP_ITEMS, null=False, blank=False)
    tester  = models.CharField(max_length=100, choices = TESTER_CHOICES, null=False, blank=False)
    sample_size = models.IntegerField(blank=False, null=False)
    sample_points = models.CharField(max_length=200, blank=False, null=False)
    sample_note = models.TextField(blank=True, null=True)
    standard_note = models.TextField(blank=True, null=True)

    photo  = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)

    safety = MultiSelectField(choices=SAFETY_CHOICES, null = True, blank = True, verbose_name = "Safety Protective", max_length=300)

class JobExportData(models.Model):
    job  = models.ForeignKey('Job', null=True, blank=False, on_delete=models.SET_NULL)
    path = models.CharField(max_length=255, blank=False, null=False)
    template = models.CharField(max_length=100, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name = _("created by"),)
    revision_code = models.CharField(max_length=100, blank=False, null=False, default="")

class Job(CloneMixin, models.Model):
    part  = models.ForeignKey('master.PartMF', on_delete=models.SET_NULL, to_field='partcode', null=True)
    safety = MultiSelectField(choices=SAFETY_CHOICES, null = True, blank = True, verbose_name = "Safety Protective", max_length=300)

    #heat treatment
    prev_wash_notneed = models.BooleanField(default=False)
    prev_wash_trw = models.BooleanField(default=False)
    prev_wash_tow = models.BooleanField(default=False)
    prev_wash_tbo = models.BooleanField(default=False)
    prev_wash_tbt = models.BooleanField(default=False)

    boutan = models.BooleanField(default=False)
    hand_setting = models.BooleanField(default=False)
    rust_prevention = models.BooleanField(default=False)
    rust_prevention_comment = models.CharField(max_length=100, null=True, blank=True)
    #hopper setting
    hopper_auto = models.BooleanField(default=False)
    chagerate_kg = models.FloatField(blank=True, null=True)
    charttime = models.FloatField(blank=True, null=True)
    totalweight = models.FloatField(blank=True, null=True)
    vibration_level = models.FloatField(blank=True, null=True)
    dumming_shutter_high = models.FloatField(blank=True, null=True)
    main_furnance = models.ForeignKey('master.Furnance', on_delete=models.SET_NULL, null=True, blank=True)

    q_s_pd  = models.IntegerField(blank=True, null=True)
    q_s_std = models.CharField(max_length=100, blank=True, null = True)
    q_s_std_low = models.FloatField(blank=True, null=True)
    q_s_std_hi = models.FloatField(blank=True, null=True)
    q_s_sent_qa = models.CharField(max_length=100, blank=True, null=True)

    q_c_pd  = models.IntegerField(blank=True, null=True)
    q_c_std = models.CharField(max_length=100, blank=True, null = True)
    q_c_std_low = models.FloatField(blank=True, null=True)
    q_c_std_hi = models.FloatField(blank=True, null=True)
    q_c_sent_qa = models.CharField(max_length=100, blank=True, null=True)

    t_s_pd  = models.IntegerField(blank=True, null=True)
    t_s_std = models.CharField(max_length=100, blank=True, null = True)
    t_s_std_low = models.FloatField(blank=True, null=True)
    t_s_std_hi = models.FloatField(blank=True, null=True)
    t_s_sent_qa = models.CharField(max_length=100, blank=True, null=True)

    t_c_pd  = models.IntegerField(blank=True, null=True)
    t_c_std = models.CharField(max_length=100, blank=True, null = True)
    t_c_std_low = models.FloatField(blank=True, null=True)
    t_c_std_hi = models.FloatField(blank=True, null=True)
    t_c_sent_qa = models.CharField(max_length=100, blank=True, null=True)



    JOBSTATUS_CHOICES = (
            ('draft', 'Draft'),
            ('trial', 'Trial'),
            ('trial_approve', 'Trial Approved'),
            ('standard', 'Standard')
            )
    status = models.CharField(max_length=40, choices = JOBSTATUS_CHOICES, blank=False, null=False, default = 'draft')

    approve =  models.BooleanField(blank = False, null=False, default=False)

    #version_code = models.CharField(max_length=100, blank=False, null=False, default="XXX")
    version_code = models.IntegerField(null=False, blank=False, default=1)

    parent_job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True )
    meta_data = JSONField(blank=True, null=True)

    updated_at = models.DateTimeField(_("updated at"),auto_now=True)
    created_by = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name = _("created by"),)
    updated_by = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    rev_note  = models.TextField("Revision note", blank=True, null=True)
    c_no  = models.CharField(max_length=100, blank=True, null=True)

    safety_inspection = MultiSelectField(choices=SAFETY_CHOICES, null = True, blank = True, verbose_name = "Safety Inspection", max_length=500, default="helmet,safety_shoes,nose,glove,glove_c")
    part_rank = models.CharField("Part Rank", max_length=40, blank=True, null=True)

    def __str__(self):
        return "%s" % self.part
    def get_absolute_url(self):
        return reverse('job-edit', kwargs={'pk': self.pk})
    '''
    part_rank
    esc
    page_no
    establish
    revision
    qrcode
    doc_code
    bar_code
    customer
    design_no
    mat_unit
    '''



