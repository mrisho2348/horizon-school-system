
from django.urls import include, path
from django.conf.urls.static import static
from result_system import settings

urlpatterns = [
   
    path('', include('result_module.urls')),
    path('ClassTeacher/', include('result_system.class_teacher_urls')),
    path('Headmaster/', include('result_system.headmaster_urls')),
    path('Academic/', include('result_system.academic_urls')),
    path('Accountant/', include('result_system.accountant_urls')),
    path('hod/', include('result_system.hod_urls')),   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
    
    
