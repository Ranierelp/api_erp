from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from accounts.models import UserGroup, GroupPermission
from companies.models import Enterprise, Employee

class Base(APIView):
    def get_enterprise_user(self,user_id):
        enterprise = {
            'is_owner': False,
            'permissions': []
        }
        
        enterprise['is_owner'] = Enterprise.objects.filter(user_id=user_id).exists()
        
        if enterprise['is_owner']: return enterprise
        
        # Permissions, Get Employee
        employee = Employee.objects.filter(user_id=user_id).first()
        
        if not employee: raise APIException('Este usuário não é um funcionário.')
        
        groups = UserGroup.objects.filter(user_id=user_id).all()
        
        for group in groups:
            group = group.group
            
            permissions = GroupPermission.objects.filter(group_id=group.id).all()
            
            for permission in permissions:
                enterprise['permissions'].append({
                    'id': permission.permission.id,
                    'label': permission.permission.name,
                    'codename': permission.permission.codename
                })
                
        return enterprise