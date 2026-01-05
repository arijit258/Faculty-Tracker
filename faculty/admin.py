from django.contrib import admin
from .models import Teacher, Subject, Session, Department, Attendance, ClassRoom, Program


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'status', 'hire_date']
    list_filter = ['status', 'department', 'gender']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['subjects']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 
                      'date_of_birth', 'gender', 'photo')
        }),
        ('Professional Information', {
            'fields': ('employee_id', 'department', 'subjects', 'qualification', 
                      'specialization', 'experience_years', 'hourly_rate', 'status', 'hire_date')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name', 'description']
    ordering = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'program', 'semester', 'subject_type', 'credits', 'total_hours', 'is_active']
    list_filter = ['program', 'semester', 'subject_type', 'is_active']
    search_fields = ['code', 'name', 'description']
    ordering = ['program', 'semester', 'code']
    filter_horizontal = ['teachers']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'date', 'day_of_week', 'start_time', 'end_time', 'room', 'status']
    list_filter = ['day_of_week', 'status', 'subject__program', 'teacher']
    search_fields = ['teacher__first_name', 'teacher__last_name', 'subject__name', 'room']
    ordering = ['-date', 'day_of_week', 'start_time']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['teachers']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'session', 'date', 'status', 'check_in_time']
    list_filter = ['status', 'date', 'teacher']
    search_fields = ['teacher__first_name', 'teacher__last_name', 'session__subject__name']
    ordering = ['-date', '-created_at']


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'capacity', 'room_type', 'is_available']
    list_filter = ['room_type', 'is_available', 'building']
    search_fields = ['name', 'building']
