from companies.views.base import Base
from companies.utils.permissions import TaskPermission
from companies.serializers import TasksSerializer, TaskSerializer
from companies.models import Task

from rest_framework.views import Response
from rest_framework.exceptions import APIException

import datetime

class Tasks(Base):
    permission_classes = [TaskPermission]
    
    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        tasks = Task.objects.filter(enterprise_id=enterprise_id).all()
        
        serializer = TasksSerializer(tasks, many=True)
        
        return Response({"tasks": serializer.data})
    
    def post(self, request):
        employee_id = request.data.get('employee_id')
        title = request.data.get('title')
        description = request.data.get('description')
        status_id = request.data.get('status_id')
        due_date = request.data.get('due_date')
        
        employee = self.get_employee(employee_id, request.user.id)
        _status = self.get_status(status_id)
        
        #Validations
        
        if not title or len(title) > 125:
            raise APIException('O Titulo da Tarefa é obrigatório')

        if due_date:
            try:
                due_date = datetime.datetime.strptime(due_date, '%d/%m/%Y %H:%M')
            except ValueError:
                raise APIException('A data de vencimento deve ser enviada no formato dd/mm/yyyy HH:MM')
            
        task = Task.objects.create(
            employee_id=employee_id,
            title=title,
            description=description,
            status_id=status_id,
            due_date=due_date,
            enterprise_id=employee.enterprise.id
        )
        
        serializer = TaskSerializer(task)
        
        return Response({"task": serializer.data})
    
class TaskDetail(Base):
    permission_classes = [TaskPermission]
    
    def get(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        task = self.get_task(task_id, enterprise_id)
        
        serializer = TaskSerializer(task)
        
        return Response({"task": serializer.data})
    
    def put(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        task = self.get_task(task_id, enterprise_id)
        
        title = request.data.get('title', task.title)
        description = request.data.get('description', task.description)
        status_id = request.data.get('status_id', task.status.id)
        due_date = request.data.get('due_date', task.due_date)  
        employee_id = request.data.get('employee_id', task.employee.id)
        
        #Validations
        self.get_employee(employee_id, request.user.id)
        self.get_status(status_id)
        
        if due_date and due_date != task.due_date:
            try:
                due_date = datetime.datetime.strptime(due_date, '%d/%m/%Y %H:%M')
            except ValueError:
                raise APIException('A data de vencimento deve ser enviada no formato dd/mm/yyyy HH:MM')
        
        
        data = {
            'title': title,
            'description': description,
            'due_date': due_date,
        }  
        
        serializer = TaskSerializer(task, data=data, partial=True)
        
        if not serializer.is_valid():
            raise APIException('Erro ao atualizar a tarefa')
        
        serializer.update(task, serializer.validated_data)
        
        task.status_id = status_id
        task.employee_id = employee_id
        task.save()
        
        return Response({"task": serializer.data})
        
        
    def delete(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        task = self.get_task(task_id, enterprise_id).delete()
           
        return Response({"success": True})
    
