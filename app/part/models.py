from django.db import models

# Create your models herePartConfig.
class PartMF(models.Model):
    custno = models.IntegerField()
    partcode = models.CharField(max_length=40, blank=True, null=True)
    documentcode = models.CharField(max_length=40, blank=True, null=True)
    treatcode = models.CharField(max_length=100, blank=True, null=True)
    designno = models.CharField(max_length=100, blank=True, null=True)
    partname = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    shtester1 = models.CharField(max_length=100, blank=True, null=True)
    sh1low = models.FloatField(blank=True, null=True)
    sh1up = models.FloatField(blank=True, null=True)
    shtester2 = models.CharField(max_length=100, blank=True, null=True)
    sh2low = models.FloatField(blank=True, null=True)
    sh2up = models.FloatField(blank=True, null=True)
    shtester3 = models.CharField(max_length=100, blank=True, null=True)
    sh3low = models.FloatField(blank=True, null=True)
    sh3up = models.FloatField(blank=True, null=True)
    chtester1 = models.CharField(max_length=100, blank=True, null=True)
    ch1low = models.FloatField(blank=True, null=True)
    ch1up = models.FloatField(blank=True, null=True)
    chtester2 = models.CharField(max_length=100, blank=True, null=True)
    ch2low = models.FloatField(blank=True, null=True)
    ch2up = models.FloatField(blank=True, null=True)
    othertester = models.CharField(max_length=100, blank=True, null=True)
    olow = models.FloatField(blank=True, null=True)
    oup = models.FloatField(blank=True, null=True)


