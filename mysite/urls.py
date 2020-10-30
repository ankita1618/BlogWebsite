"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', views.post_list, name="post_list"),
	path('blog/', include(("blog.urls", 'app_name'),  namespace="blog", )),
    path('admin/', admin.site.urls),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('signup/',views.signup, name='signup'),
    path('like/', views.like_post, name="like_post"),
    
#     path('index/',views.index,name="index"),
#     path('datetime/',views.current_datetime, name="datetime"),

#password reset urls

    url('', include('django.contrib.auth.urls')),
    # path('password-reset/', auth_views.password_reset,name="password_reset"),
    # path('password-reset/done', auth_views.password_reset_done,name="password_reset_done"),
    # path('password-reset/confirm/(?P<uidb64>[\w-]+)/(?/P<token>[\w-]+)/$', auth_views.password_reset_confirm,name="password_reset_confirm"),
    # path('password-reset_complete', auth_views.password_reset_complete,name="password_reset_complete"),
]
# (?P<slug>[\w-]+)/$
 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)