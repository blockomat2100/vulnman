from rest_framework import mixins
from apps.assets import models
from api.v1.generics import ProjectSessionViewSet
from api.v1.serializers import assets as serializers


class HostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ProjectSessionViewSet):
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    object_permissions_required = ["projects.view_project"]


class ServiceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ProjectSessionViewSet):
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()
    object_permissions_required = ["projects.view_project"]


class WebApplicationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ProjectSessionViewSet):
    serializer_class = serializers.WebApplicationSerializer
    queryset = models.WebApplication.objects.all()
    object_permissions_required = ["projects.view_project"]


class WebRequestViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, ProjectSessionViewSet):
    serializer_class = serializers.WebRequestSerializer
    queryset = models.WebRequest.objects.all()
    object_permissions_required = ["projects.view_project"]
