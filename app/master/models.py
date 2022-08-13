from django.db import models
from django.urls import reverse
from jsonfield import JSONField
from PIL import Image

COL_CHOICES = (
        ('zone1', 'Zone 1'),
        )
CHECK_CHOICES = (
        ('quenching', 'Quenching'),
        )

# Create your models here.
class ParamTemplate(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)
    qparams = JSONField(blank=True, null=True)
    tparams = JSONField(blank=True, null=True)

class Furnance(models.Model):
    furnance = models.CharField(max_length=100, blank=False, null=True)
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
    checkq_1 = models.CharField(max_length=100,  blank=True, null=True)
    checkt_2 = models.CharField(max_length=100,  blank=True, null=True)
    coveyor_length =  models.FloatField(blank=True, null=True)
    max_weight_value = models.FloatField(blank = True, null = True)
    max_weight_unit = models.CharField(max_length=20, blank=True, null=True)
    furtype  = models.CharField(max_length=40,  blank=True, null=True)
    furno = models.CharField(max_length=4, blank=False, null=False)
    template_name = models.CharField(max_length=100, blank=True, null=True)

    params = JSONField(blank=True, null=True)
    tparams = JSONField(blank=True, null=True)
    enable_qcols = models.CharField(max_length=200, blank=True, null=True)
    enable_tcols = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('furnance-edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.enable_qcols = self.get_qactive_cols()
        self.enable_tcols = self.get_tactive_cols()
        super(Furnance, self).save(*args, **kwargs)

    def get_qactive_cols(self):
        cols = ["qcol1", "qcol2", "qcol3", "qcol4", "qcol5", "qcol6",
                "qcol7", "qcol8"]
        cs  = []
        for c in cols:
            v = getattr(self, c)
            if v is not None and v != "" and v != "-":
                cs.append(c)
        return ",".join(cs)

    def get_tactive_cols(self):
        cols = ["tcol1", "tcol2", "tcol3", "tcol4", "tcol5", "tcol6"]
        cs  = []
        for c in cols:
            v = getattr(self, c)
            if v is not None and v != "" and v != "-":
                cs.append(c)
        return ",".join(cs)


    def __str__(self):
        return "%s" % (self.furnance,)

    def get_active_fields(self):
        fs = {}
        for f in self._meta.fields:
            v = getattr(self, f.name)
            if v is not None and  v != "" and v!= "-":
                fs[f.name]  =  v
        return fs

    def get_hidden_fields(self):
        fs = {}
        for f in self._meta.fields:
            v = getattr(self, f.name)
            if v is  None or  v == "" or v == "-":
                fs[f.name]  =  v
        return fs

    def to_json(self):
        return '{"name": "%s"}' % self.furnance

class PartPhoto(models.Model):
    caption  = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to="images/%Y/%m/%d/")
    part = models.ForeignKey('PartMF', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        super(PartPhoto, self).save()

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

class PartMF(models.Model):
    custom_no = models.IntegerField(null=False, blank=False)
    partcode = models.CharField(max_length=255, blank=False, null=False, unique=True)
    doc_code = models.CharField(max_length=255, blank=True, null=True)
    treatcd = models.CharField(max_length=255, blank=True, null=True)
    designno = models.CharField(max_length=255, blank=True, null=True)
    partname = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    mat = models.CharField(max_length=255, blank=False, null=True)

    shtester1 = models.CharField(max_length=255, blank=True, null=True)
    low1 = models.FloatField(blank=True, null=True)
    up1 = models.FloatField(blank=True, null=True)

    shtester2 = models.CharField(max_length=255, blank=True, null=True)
    low2 = models.FloatField(blank=True, null=True)
    up2 = models.FloatField(blank=True, null=True)

    shtester3 = models.CharField(max_length=255, blank=True, null=True)
    low3  = models.FloatField(blank=True, null=True)
    up3 = models.FloatField(blank=True, null=True)

    chtester1 = models.CharField(max_length=255, blank=True, null=True)
    chlow1 = models.FloatField(blank=True, null=True)
    chup1 = models.FloatField(blank=True, null=True)

    chtester2 = models.CharField(max_length=255, blank=True, null=True)
    chlow2 = models.FloatField(blank=True, null=True)
    chup2 = models.FloatField(blank=True, null=True)

    othertester = models.CharField(max_length=255, blank=True, null=True)
    olow1 = models.FloatField(blank=True, null=True)
    oup1 = models.FloatField(blank=True, null=True)

    effpoint1 = models.CharField(max_length=255, blank=True, null=True)
    effcriterion1 = models.IntegerField(blank=True, null=True)
    eff_low1= models.FloatField(blank=True, null=True)
    eff_up1 = models.FloatField(blank=True, null=True)


    effpoint2 = models.CharField(max_length=255, blank=True, null=True)
    effcriterion2 = models.IntegerField(blank=True, null=True)
    eff_low2= models.FloatField(blank=True, null=True)
    eff_up2 = models.FloatField(blank=True, null=True)


    total_measures= models.CharField(max_length=30, blank=True, null=True)
    total_low= models.FloatField(blank=True, null=True)
    total_up= models.FloatField(blank=True, null=True)

    rev_date = models.DateField(null=True, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    del_flag = models.IntegerField(null=True, blank=True)
    qo_no = models.CharField(max_length=255)
    kgperpc = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.doc_code or '-'} / {self.partcode or '-'} / {self.partname or '-'}"

    def shtester2_con(self):
        if self.shtester2 is not None:
            return  ConstantMF.objects.get(data_code = self.shtester2, class_code=7).data1
        else:
            return "-"

class Customer(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return "%s %s" % (self.code, self.name)
class ConstantMF(models.Model):
    class_code = models.IntegerField(blank=False, null=True)
    data_code = models.CharField(max_length=20, blank=False, null=False)
    data1  = models.CharField(max_length=150, blank=True, null=True)
    data2  = models.CharField(max_length=150, blank=True, null=True)
    data3  = models.CharField(max_length=150, blank=True, null=True)
    total  = models.IntegerField(blank=True, default=0)



