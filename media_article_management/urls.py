from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import login_view 
from users.views import register # import your login view
# from users import views 
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    # path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),  # Routes for articles
    path('users/', include('users.urls')),        # Routes for user management
   
#    path('default_dashboard/', views.default_dashboard, name='default_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



