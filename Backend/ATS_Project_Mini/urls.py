from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('',views.landing,name='landing'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path("templates/", views.resume_templates, name="resume_templates"),
    path("beginResume/",views.beginResume, name='beginResume'),
    path("beginResume1/",views.beginResume1, name='beginResume1'),
    path("beginResume2/",views.beginResume2, name='beginResume2'),
    path("editTemplates/", views.editableTemplates, name="editableTemplates"),
    path('about/', views.about_us, name='about_us'),
    path('logout/', views.logout, name='logout'),
]