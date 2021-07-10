from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path('admin/', admin.site.urls),
    path('user_account/', include('user_account.urls')),
    path('nyumba/', include('nyumba.urls')),
    path('MpesaPayments/', include('MpesaPayments.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
