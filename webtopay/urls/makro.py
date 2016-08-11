from django.conf.urls import url
from webtopay.views import makro

urlpatterns = [
    url(r'^$', makro, name="webtopay-makro")
]
