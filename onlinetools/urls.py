"""onlinetools URL Configuration"""

from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='frontpage.html'), name='frontpage')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
