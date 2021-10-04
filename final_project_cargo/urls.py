
from django.urls import path

from .views import Send_cagro_View, ChangePasswordView, UserDetail, UserProfileUpdateView, UserProfileUpdateimage, UserProfileUpdatephone

app_name = 'final_project_cargo'

urlpatterns = [
    path('',  Send_cagro_View.as_view(
        {'get': 'list'}), name='send_cargo_list'),
    path('<uuid:Send_cargo_id>/',
         Send_cagro_View.as_view({'get': 'retrieve'}), name='Send_cargo_detail'),
    path('change-password/', ChangePasswordView.as_view(),
         name='change-password'),
    path('change/<int:pk>', UserDetail.as_view(),
         name='change'),
    path('change-email/<int:pk>', UserProfileUpdateView.as_view(),
         name='changes'),
    path('change-phone/<int:pk>', UserProfileUpdatephone.as_view(),
         name='changesphone'),
    path('change-image/<int:pk>', UserProfileUpdateimage.as_view(),
         name='changesimage'),

]
