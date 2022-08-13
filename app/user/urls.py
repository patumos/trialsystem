from django.urls import path

from . import views

urlpatterns = [
        path('profile/', views.update_profile, name='profile'),
        path('groups/', views.UserGroupAdminList.as_view(), name='usergroup_list'),
        path('groups/edit/<int:pk>', views.UserGroupAdminUpdate.as_view(), name='usergroup_edit'),
        path('groups/delete/<int:pk>', views.UserGroupAdminDelete.as_view(), name='usergroup_delete'),

        path('useradmin/', views.UserAdminList.as_view(), name='useradmin_list'),
        path('useradmin/view/<int:pk>', views.UserAdminView.as_view(), name='useradmin_view'),
        path('useradmin/new', views.UserAdminCreate.as_view(), name='useradmin_new'),
        path('useradmin/view/<int:pk>', views.UserAdminView.as_view(), name='useradmin_view'),
        path('useradmin/edit/<int:pk>', views.UserAdminUpdate.as_view(), name='useradmin_edit'),
        path('useradmin/delete/<int:pk>', views.UserAdminDelete.as_view(),
            name='useradmin_delete'),
        path('log/', views.user_log,name='user_log'),
]


