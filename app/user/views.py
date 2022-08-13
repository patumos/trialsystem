from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from var_dump import var_dump
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Profile, LoginLogoutLog
from django.forms.models import inlineformset_factory
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
@transaction.atomic
def update_profile(request):
    '''if request.LANGUAGE_CODE == 'de-at':
        return HttpResponse("You prefer to read Austrian German.")
    else:
        return HttpResponse(request.LANGUAGE_CODE) '''
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            var_dump(request.POST['birth_date'])
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



class UserGroupAdminList(UserPassesTestMixin, ListView):
    model = Group
    template_name = "user/usergroup_list.html"
    def test_func(self):
        return self.request.user.is_superuser

class UserGroupAdminUpdate(UserPassesTestMixin, UpdateView):
    model = Group
    template_name = "user/usergroup_form.html"
    fields = "__all__"
    def test_func(self):
        return self.request.user.is_superuser

class UserGroupAdminDelete(DeleteView):
    model = Group
    success_url = reverse_lazy("usergroup_list")
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class UserAdminList(UserPassesTestMixin, ListView):
    paginate_by = 20
    model = User
    template_name = "user/useradmin_list.html"
    extra_context = {
            'headerText': _('User Admin'),
            'cols':['username','profile.province',  'first_name', 'last_name'],
            'colNames': ['User Name', 'Province', 'First Name', 'Last Name'],
            'modelName': 'useradmin'
            }

    def test_func(self):
        return self.request.user.is_superuser

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('page_size', self.paginate_by)


class UserAdminView(UserPassesTestMixin, DetailView):
    model = User
    template_name = "user/general_view.html"

    extra_context = {'headerText': _("View %s" % model.__name__),
            'view': {'label': 'View', 'url': 'useradmin_list' },
            'parent': 'user/useradmin_list.html'
            }

    def test_func(self):
        return self.request.user.is_superuser

CHOICES = (('Not Spec', ''),)

UserProfileFormSet = inlineformset_factory(User, Profile, fields=('staff_roles',))

class UserAdminCreate(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name  =  "user/gn_form.html"
    extra_context = {'headerText':_("UserAdmin Edit"),
            'editbs': {
            'label': 'UserAdmin Create', 'link': 'useradmin_new'},
            'parent': 'user/useradmin_list.html'
            }
    success_url = reverse_lazy("useradmin_list")

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("useradmin_edit", kwargs = {'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(UserAdminCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['user_profile'] = ProfileForm(self.request.POST, self.request.FILES)
        else:
            context['user_profile'] = ProfileForm()
        return context

    '''
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['user_profile_formset']

        if formset.is_valid():

            self.object = form.save()
            self.object.set_password(form.cleaned_data['password'])
            self.object.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    '''

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['user_profile']
        with transaction.atomic():
            if form.is_valid() and formset.is_valid():
                user = form.save()
                profile  = formset.save(commit=False)
                profile.user = user
                profile.save()

        return super(UserAdminCreate, self).form_valid(form)

class UserAdminUpdate(UserPassesTestMixin, UpdateView, SuccessMessageMixin):
    model = User
    template_name  =  "user/gn_form.html"
    #fields = ['firstName', 'lastName', 'prefix']

    extra_context = {'headerText': _("UserAdmin Edit"),
            'editbs': {
            'label': 'UserAdmin Edit', 'link': 'useradmin_ledit'},
            'parent': 'user/useradmin_list.html'
            }

    #form_class = UserChangeForm
    fields = ['username','first_name', 'last_name','email', 'is_staff','is_superuser', 'is_active']
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(UserAdminUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['user_profile'] = UserProfileFormSet(self.request.POST, self.request.FILES, instance = self.object)

        else:
            context['user_profile'] = UserProfileFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['user_profile']
        with transaction.atomic():
            self.object = form.save()
            password = self.request.POST.get('password', None)
            confirm_password = self.request.POST.get('confirm_password', None)
            if password is not None and password != "":
                if password == confirm_password:
                     self.object.set_password(password)
                     messages.success(self.request, "Password Updated")
                else:
                    messages.error(self.request, "Password not matched")

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                print(formset.errors)

        return super(UserAdminUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("useradmin_edit", kwargs = {'pk': self.object.pk})

class UserAdminDelete(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('useradmin_list')
    template_name = "forms/gn_confirm_delete.html"
    extra_context = {'header': _("Delete %s" % model.__name__), 'parent': 'users/useradmin_list.html',
            'deletebs': {
            'label': 'UserAdmin Delete', 'link': 'useradmin_delete'},
            }

    def test_func(self):
        return self.request.user.is_superuser


    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

def user_log(request):
    objects = LoginLogoutLog.objects.all().order_by("-id")
    return render(request, "user/history.html", {'objects': objects });
