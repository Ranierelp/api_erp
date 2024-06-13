from rest_framework import permissions
from accounts.models import UserGroups, GroupPermissions
from django.contrib.auth.models import Permission

def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False 
    
    if user.is_owner:
        return True
    
    required_permission = 'view_' + permission_to
    if method == 'POST':
        required_permission = 'add_' + permission_to
    elif method == 'PUT':
        required_permission = 'change_' + permission_to
    elif method == 'DELETE':
        required_permission = 'delete_' + permission_to
        
    groups = UserGroups.objects.values('group_id').filter(user_id=user.id).all() 
    
    for group in groups:
        permissions = GroupPermissions.objects.values('permission_id').filter(group_id=group['group_id']).all()
        
        for permission in permissions:
            if Permission.objects.filter(id=permission['permission_id'], codname=required_permission).exists():
                return True
            

class EmployeesPermission(permissions.BasePermission):
    message = 'O funcionario não tem permissão para acessar este recurso.'
    
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='employee')
    
class GroupPermission(permissions.BasePermission):
    message = 'O Funcionário não tem permissão para gerenciar os grupos.'
    
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='group')
    
class GroupsPermissionsPermission(permissions.BasePermission):
    message = 'O Funcionário não tem permissão para gerenciar as permissões.'
    
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='permission')
    
class TaskPermission(permissions.BasePermission):
    message = 'O Funcionário não tem permissão para gerenciar as tarefas.'
    
    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to='task')