from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Banner
from .serializers import BannerSerializer
from django.conf import settings


class BannerView(GenericViewSet, ListModelMixin):
    serializer_class = BannerSerializer
    # qs对象，可以切片  qs[:3]
    queryset = Banner.objects.all().filter(is_delete=False, is_show=True)[:settings.BANNER_COUNT]