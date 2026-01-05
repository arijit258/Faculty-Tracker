from django.urls import path
from . import views
from .views import (
    DashboardView, TeacherListView, TeacherDetailView, TeacherCreateView,
    TeacherUpdateView, TeacherDeleteView, SubjectListView, SubjectCreateView,
    SubjectUpdateView, SubjectDeleteView, SessionListView, SessionCreateView,
    SessionUpdateView, SessionDeleteView, DepartmentListView, DepartmentCreateView,
    DepartmentUpdateView, DepartmentDeleteView, ProgramListView, ProgramCreateView,
    ProgramUpdateView, ProgramDeleteView, ReportsView, ExportPDFView,
    ExportExcelView, ExportCSVView, ExportTeacherDetailsView, ExportSingleTeacherView
)

app_name = 'faculty'

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Teacher URLs
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', TeacherCreateView.as_view(), name='teacher_add'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/<int:pk>/edit/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('teachers/<int:pk>/export/', ExportSingleTeacherView.as_view(), name='teacher_export'),
    
    # Program URLs
    path('programs/', ProgramListView.as_view(), name='program_list'),
    path('programs/add/', ProgramCreateView.as_view(), name='program_add'),
    path('programs/<int:pk>/edit/', ProgramUpdateView.as_view(), name='program_edit'),
    path('programs/<int:pk>/delete/', ProgramDeleteView.as_view(), name='program_delete'),
    
    # Subject URLs
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', SubjectCreateView.as_view(), name='subject_add'),
    path('subjects/<int:pk>/edit/', SubjectUpdateView.as_view(), name='subject_edit'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
    
    # Session/Schedule URLs
    path('schedule/', SessionListView.as_view(), name='schedule'),
    path('schedule/add/', SessionCreateView.as_view(), name='session_add'),
    path('schedule/<int:pk>/edit/', SessionUpdateView.as_view(), name='session_edit'),
    path('schedule/<int:pk>/delete/', SessionDeleteView.as_view(), name='session_delete'),
    
    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
    
    # Reports
    path('reports/', ReportsView.as_view(), name='reports'),
    path('reports/export/pdf/', ExportPDFView.as_view(), name='export_pdf'),
    path('reports/export/excel/', ExportExcelView.as_view(), name='export_excel'),
    path('reports/export/csv/', ExportCSVView.as_view(), name='export_csv'),
    path('reports/export/teacher-details/', ExportTeacherDetailsView.as_view(), name='export_teacher_details'),
    
    # AJAX URLs
    path('check-conflicts/', views.check_session_conflicts, name='check_conflicts'),
    path('get-teacher-subjects/', views.get_teacher_subjects, name='get_teacher_subjects'),
    path('get-all-teachers/', views.get_all_teachers, name='get_all_teachers'),
]
