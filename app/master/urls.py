from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='master-index'),
    path('furnances/', views.FurnanceListView.as_view(), name = 'furnance-list'),
    path('furnances/new', views.FurnanceCreateView.as_view(), name = 'furnance-create'),
    path('furnances/edit/<int:pk>', views.FurnanceEditView.as_view(), name = 'furnance-edit'),
    path('furnances/clone/<int:pk>', views.clone_furnance, name = 'furnance-clone'),
    path('furnances/delete/<int:pk>', views.FurnanceDeleteView.as_view(), name = 'furnance-delete'),
    path('templates/', views.ParamTemplateListView.as_view(), name = 'paramtemplate-list'),
    path('templates/new', views.ParamTemplateCreateView.as_view(), name = 'paramtemplate-create'),
    path('templates/edit/<int:pk>', views.ParamTemplateEditView.as_view(), name = 'paramtemplate-edit'),
    path('templates/delete/<int:pk>', views.ParamTemplateDeleteView.as_view(), name = 'paramtemplate-delete'),
    path('customers/', views.CustomerListView.as_view(), name = 'customer-list'),
    path('customers/new', views.CustomerCreateView.as_view(), name = 'customer-create'),
    path('customers/edit/<int:pk>', views.CustomerEditView.as_view(), name = 'customer-edit'),
    path('customers/delete/<int:pk>', views.CustomerDeleteView.as_view(), name = 'customer-delete'),
    path('parts/', views.PartListView.as_view(), name = 'part-list'),
    path('parts/new', views.PartCreateView.as_view(), name = 'part-create'),
    path('parts/edit/<int:pk>', views.PartEditView.as_view(), name = 'part-edit'),
    path('parts/delete/<int:pk>', views.PartDeleteView.as_view(), name = 'part-delete'),
    path('import/', views.importFile, name = 'importFile'),
        ]
