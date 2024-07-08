from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionsDetail

urlpatterns = [
    # Employees URLs
    path('employees/', Employees.as_view()),
    path('employees/<int:employee_id>/', EmployeeDetail.as_view()),
    
    #Groups and Permissions URLs
    path('permissions', PermissionsDetail.as_view())
]