from django.conf.urls import url
from webtopay.views import mikro

urlpatterns = [
    url(r'^$', mikro, name="webtopay-mikro")
]
