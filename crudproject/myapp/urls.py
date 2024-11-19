# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.alumni_list, name='alumni_list'),
#     path('<int:pk>/', views.alumni_detail, name='alumni_detail'),
#     path('create/', views.alumni_create, name='alumni_create'),
#     path('<int:pk>/update/', views.alumni_update, name='alumni_update'),
#     path('<int:pk>/delete/', views.alumni_delete, name='alumni_delete'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard (list of alumni)
    path('alumni/<int:pk>/', views.alumni_detail, name='alumni_detail'),  # View alumni details
    path('alumni/<int:pk>/edit/', views.alumni_update, name='alumni_update'),  # Edit alumni
    path('alumni/<int:pk>/delete/', views.alumni_delete, name='alumni_delete'),  # Delete alumni
    path('list', views.alumni_list, name='alumni_list'),
    path('create/', views.alumni_create, name='alumni_create'),
    path('alumni/<int:pk>/edit/', views.alumni_update, name='alumni_update'),
    path('alumni/<int:pk>/delete/', views.alumni_delete, name='alumni_delete'),
    path('export/csv/', views.export_alumni_csv, name='export_alumni_csv'),
    path('sync', views.sync_data, name='sync_data'),
]