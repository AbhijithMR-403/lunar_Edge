"""
URL configuration for lunar_Edge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('adn/', admin.site.urls),
    path('', include('authenticator.urls')),
    path('', include('user_panel.urls')),
    path('', include('order.urls')),
    path('', include('user_cart.urls')),
    path('profile/', include('user_profile.urls')),
    path('admin/', include('order_details_admin.urls')),
    path('admin/', include('admin_panel.urls')),
    path('admin/', include('category_management.urls')),
    path('admin/', include('product_management.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
