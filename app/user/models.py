from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
STAFF_ROLES = (
        ('admin', 'Admin'),
        ('engineer', 'Engineer')
        )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_roles  = MultiSelectField(choices=STAFF_ROLES, null=True, blank=True)


    def print_roles(self):
        return self.staff_roles

    def is_admin(self):
        return 'admin' in self.staff_roles

    def is_engineer(self):
        return 'engineer' in self.staff_roles



class LoginLogoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, blank=False, null=False)
    host = models.CharField(max_length=100, blank=False, null=False)
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'login_logout_logs'

#from .signals_handler import *
#
import logging
import datetime

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# for logging - define "error" named logging handler and logger in settings.py
error_log=logging.getLogger('error')


@receiver(user_logged_in)
def log_user_logged_in(sender, user, request, **kwargs):
    try:
        login_logout_logs = LoginLogoutLog.objects.filter(session_key=request.session.session_key, user=user.id)[:1]
        if not login_logout_logs:
            login_logout_log = LoginLogoutLog(login_time=datetime.datetime.now(),session_key=request.session.session_key, user=user, host=request.META['HTTP_HOST'])
            login_logout_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

@receiver(user_logged_out)
def log_user_logged_out(sender, user, request, **kwargs):
    try:
        login_logout_logs = LoginLogoutLog.objects.filter(session_key=request.session.session_key, user=user.id, host=request.META['HTTP_HOST'])
        login_logout_logs.filter(logout_time__isnull=True).update(logout_time=datetime.datetime.now())
        if not login_logout_logs:
            login_logout_log = LoginLogoutLog(logout_time=datetime.datetime.now(), session_key=request.session.session_key, user=user, host=request.META['HTTP_HOST'])
            login_logout_log.save()
    except Exception as e:
        #log the error
        error_log.error("log_user_logged_out request: %s, error: %s" % (request, e))



