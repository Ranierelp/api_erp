from companies.views.base import Base
from companies.utils.permissions import GroupsPermission
from companies.serializers import PermissionsSerializer

from rest_framework.views import Response

from django.contrib.auth.models import Permission

class PermissionsDetail(Base):
    permission_classes = [GroupsPermission]
    
    def get(self, request):
        permissions = Permission.objects.filter(content_type_id__in=[2, 7, 11, 13]).all()
        
        serializer = PermissionsSerializer(permissions, many=True)
        
        return Response({"permissions": serializer.data})