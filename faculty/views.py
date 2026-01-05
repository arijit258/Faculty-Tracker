from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum, Avg
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import io
from xhtml2pdf import pisa
from .models import Teacher, Subject, Session, Department, Attendance, ClassRoom, Program
from .forms import TeacherForm, SubjectForm, SessionForm, DepartmentForm, AttendanceForm, ClassRoomForm, ProgramForm
from django.db.models.functions import TruncWeek, TruncDay


class DashboardView(View):
    """Dashboard view with overview statistics and charts"""
    
    def get(self, request):
        # Get current date and time
        now = timezone.now()
        today = now.date()
        current_time = now.time()
        
        # Basic statistics
        total_teachers = Teacher.objects.count()
        active_teachers = Teacher.objects.filter(status='active').count()
        total_subjects = Subject.objects.count()
        active_subjects = Subject.objects.filter(is_active=True).count()
        total_programs = Program.objects.count()
        total_sessions = Session.objects.count()
        scheduled_sessions = Session.objects.filter(status='scheduled').count()
        
        # Today's classes
        today_name = today.strftime('%A').lower()
        todays_sessions = Session.objects.filter(
            day_of_week=today_name,
            status='scheduled'
        ).select_related('teacher', 'subject').order_by('start_time')
        
        # Upcoming sessions (next 7 days)
        upcoming_sessions = Session.objects.filter(
            status='scheduled'
        ).select_related('teacher', 'subject')[:10]
        
        # Teachers by department
        teachers_by_department = Teacher.objects.values(
            'department__name'
        ).annotate(count=Count('id')).filter(department__isnull=False)
        
        # Sessions per day of week
        sessions_per_day = Session.objects.values(
            'day_of_week'
        ).annotate(count=Count('id'))
        
        # Hours taught per teacher (top 10)
        teacher_hours = Teacher.objects.annotate(
            total_hours=Sum('session__duration')
        ).order_by('-total_hours')[:10]
        
        # Recent activities (mock data for demo)
        recent_activities = [
            {
                'icon': 'fa-user-plus',
                'color': 'success',
                'title': 'New Teacher Added',
                'description': 'John Smith was added to the system',
                'time': '2 hours ago'
            },
            {
                'icon': 'fa-calendar-plus',
                'color': 'primary',
                'title': 'Class Scheduled',
                'description': 'Mathematics class scheduled for Monday',
                'time': '4 hours ago'
            },
            {
                'icon': 'fa-book',
                'color': 'info',
                'title': 'New Course Added',
                'description': 'Data Science course has been created',
                'time': '1 day ago'
            },
            {
                'icon': 'fa-exclamation-triangle',
                'color': 'warning',
                'title': 'Schedule Conflict',
                'description': 'Conflict detected for Room 101',
                'time': '2 days ago'
            },
        ]
        
        context = {
            'total_teachers': total_teachers,
            'active_teachers': active_teachers,
            'total_subjects': total_subjects,
            'active_subjects': active_subjects,
            'total_programs': total_programs,
            'total_sessions': total_sessions,
            'scheduled_sessions': scheduled_sessions,
            'todays_sessions': todays_sessions,
            'upcoming_sessions': upcoming_sessions,
            'teachers_by_department': list(teachers_by_department),
            'sessions_per_day': list(sessions_per_day),
            'teacher_hours': teacher_hours,
            'recent_activities': recent_activities,
            'today': today,
        }
        
        return render(request, 'faculty/dashboard.html', context)


class TeacherListView(ListView):
    """List all teachers with search and filtering"""
    
    model = Teacher
    template_name = 'faculty/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Teacher.objects.select_related('department').all()
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(employee_id__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by department
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department_id=department)
        
        return queryset.order_by('last_name', 'first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context


class TeacherDetailView(DetailView):
    """View detailed teacher profile"""
    
    model = Teacher
    template_name = 'faculty/teacher_detail.html'
    context_object_name = 'teacher'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        
        # Get date range from request parameters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Build session filter
        session_filter = {'teacher': teacher}
        if start_date:
            session_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            session_filter['created_at__date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get teacher's sessions with optional date filtering
        sessions = Session.objects.filter(**session_filter).select_related(
            'subject', 'subject__program'
        ).order_by('day_of_week', 'start_time')
        
        # Calculate statistics
        total_hours = sum(session.duration for session in sessions)
        total_sessions_count = sessions.count()
        
        # Get attendance records
        attendance_filter = {'teacher': teacher}
        if start_date:
            attendance_filter['date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            attendance_filter['date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        attendance_records = Attendance.objects.filter(**attendance_filter).select_related(
            'session', 'session__subject'
        ).order_by('-date')[:20]
        
        context['sessions'] = sessions
        context['total_hours'] = total_hours
        context['total_sessions_count'] = total_sessions_count
        context['attendance_records'] = attendance_records
        context['start_date'] = start_date
        context['end_date'] = end_date
        return context


class TeacherCreateView(CreateView):
    """Create new teacher"""

    model = Teacher
    form_class = TeacherForm
    template_name = 'faculty/teacher_form.html'
    success_url = reverse_lazy('faculty:teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher added successfully!')
        return super().form_valid(form)


class TeacherUpdateView(UpdateView):
    """Update existing teacher"""

    model = Teacher
    form_class = TeacherForm
    template_name = 'faculty/teacher_form.html'
    success_url = reverse_lazy('faculty:teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher updated successfully!')
        return super().form_valid(form)


class TeacherDeleteView(DeleteView):
    """Delete teacher"""

    model = Teacher
    template_name = 'faculty/teacher_confirm_delete.html'
    success_url = reverse_lazy('faculty:teacher_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Teacher deleted successfully!')
        return super().delete(request, *args, **kwargs)


class SubjectListView(ListView):
    """List all subjects"""
    
    model = Subject
    template_name = 'faculty/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Subject.objects.select_related('program', 'program').all()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(code__icontains=search)
            )
        
        # Filter by program
        program = self.request.GET.get('program')
        if program:
            queryset = queryset.filter(program_id=program)
        
        subject_type = self.request.GET.get('type')
        if subject_type:
            queryset = queryset.filter(subject_type=subject_type)
        
        is_active = self.request.GET.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=(is_active == 'true'))
        
        return queryset.order_by('program', 'semester', 'code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        return context


class SubjectCreateView(CreateView):
    """Create new subject"""

    model = Subject
    form_class = SubjectForm
    template_name = 'faculty/subject_form.html'
    success_url = reverse_lazy('faculty:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject added successfully!')
        return super().form_valid(form)


class SubjectUpdateView(UpdateView):
    """Update existing subject"""

    model = Subject
    form_class = SubjectForm
    template_name = 'faculty/subject_form.html'
    success_url = reverse_lazy('faculty:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject updated successfully!')
        return super().form_valid(form)


class SubjectDeleteView(DeleteView):
    """Delete subject"""

    model = Subject
    template_name = 'faculty/subject_confirm_delete.html'
    success_url = reverse_lazy('faculty:subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Subject deleted successfully!')
        return super().delete(request, *args, **kwargs)


class SessionListView(ListView):
    """List all sessions with filtering"""
    
    model = Session
    template_name = 'faculty/schedule.html'
    context_object_name = 'sessions'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Session.objects.select_related(
            'teacher', 'teacher__department', 'subject'
        ).all()
        
        # Filters
        teacher = self.request.GET.get('teacher')
        if teacher:
            queryset = queryset.filter(teacher_id=teacher)
        
        day = self.request.GET.get('day_of_week')
        if day:
            queryset = queryset.filter(day_of_week=day)
        
        subject = self.request.GET.get('subject')
        if subject:
            queryset = queryset.filter(subject_id=subject)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('day_of_week', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(status='active')
        context['subjects'] = Subject.objects.filter(is_active=True)
        return context


class SessionCreateView(CreateView):
    """Create new session"""

    model = Session
    form_class = SessionForm
    template_name = 'faculty/session_form.html'
    success_url = reverse_lazy('faculty:schedule')

    def form_valid(self, form):
        messages.success(self.request, 'Session scheduled successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Session'
        return context


class SessionUpdateView(UpdateView):
    """Update existing session"""

    model = Session
    form_class = SessionForm
    template_name = 'faculty/session_form.html'
    success_url = reverse_lazy('faculty:schedule')

    def form_valid(self, form):
        messages.success(self.request, 'Session updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Session'
        return context


class SessionDeleteView(DeleteView):
    """Delete session"""

    model = Session
    template_name = 'faculty/session_confirm_delete.html'
    success_url = reverse_lazy('faculty:schedule')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Session deleted successfully!')
        return super().delete(request, *args, **kwargs)


class DepartmentListView(ListView):
    """List all departments"""

    model = Department
    template_name = 'faculty/department_list.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add teacher count per department using ManyToManyField
        for dept in context['departments']:
            dept.teacher_count = dept.teachers.count()
        return context


class DepartmentCreateView(CreateView):
    """Create new department"""

    model = Department
    form_class = DepartmentForm
    template_name = 'faculty/department_form.html'
    success_url = reverse_lazy('faculty:department_list')

    def form_valid(self, form):
        messages.success(self.request, 'Department added successfully!')
        return super().form_valid(form)


class DepartmentUpdateView(UpdateView):
    """Update existing department"""

    model = Department
    form_class = DepartmentForm
    template_name = 'faculty/department_form.html'
    success_url = reverse_lazy('faculty:department_list')

    def form_valid(self, form):
        messages.success(self.request, 'Department updated successfully!')
        return super().form_valid(form)


class DepartmentDeleteView(DeleteView):
    """Delete department"""

    model = Department
    template_name = 'faculty/department_confirm_delete.html'
    success_url = reverse_lazy('faculty:department_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Department deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProgramListView(ListView):
    """List all programs"""
    
    model = Program
    template_name = 'faculty/program_list.html'
    context_object_name = 'programs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add subject count per program
        for prog in context['programs']:
            prog.subject_count = Subject.objects.filter(program=prog).count()
        return context


class ProgramCreateView(CreateView):
    """Create new program"""

    model = Program
    form_class = ProgramForm
    template_name = 'faculty/program_form.html'
    success_url = reverse_lazy('faculty:program_list')

    def form_valid(self, form):
        messages.success(self.request, 'Program added successfully!')
        return super().form_valid(form)


class ProgramUpdateView(UpdateView):
    """Update existing program"""

    model = Program
    form_class = ProgramForm
    template_name = 'faculty/program_form.html'
    success_url = reverse_lazy('faculty:program_list')

    def form_valid(self, form):
        messages.success(self.request, 'Program updated successfully!')
        return super().form_valid(form)


class ProgramDeleteView(DeleteView):
    """Delete program"""

    model = Program
    template_name = 'faculty/program_confirm_delete.html'
    success_url = reverse_lazy('faculty:program_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Program deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ReportsView(View):
    """Reports and analytics view"""
    
    def get(self, request):
        # Get date range from request parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Base queryset for sessions with optional date filtering
        session_filter = {}
        if start_date:
            session_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            session_filter['created_at__date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Teacher utilization report with optional date filtering
        teacher_utilization_base = Teacher.objects.annotate(
            total_hours=Sum('session__duration'),
            session_count=Count('session')
        ).order_by('-total_hours')
        
        # Apply date filtering if dates are provided
        if start_date or end_date:
            # Filter teachers who have sessions in the date range
            session_qs = Session.objects.filter(**session_filter) if session_filter else Session.objects.all()
            teacher_ids_with_sessions = session_qs.values_list('teacher_id', flat=True).distinct()
            teacher_utilization = teacher_utilization_base.filter(id__in=teacher_ids_with_sessions)
        else:
            teacher_utilization = teacher_utilization_base
        
        # Department-wise statistics
        department_stats = []
        departments = Department.objects.all()
        for dept in departments:
            teacher_count = Teacher.objects.filter(department=dept).count()
            
            # Count subjects through teachers in this department
            subject_count = Subject.objects.filter(teachers__department=dept).distinct().count()
            
            # Count sessions through teachers in this department
            session_qs = Session.objects.filter(teacher__department=dept)
            if start_date:
                session_qs = session_qs.filter(created_at__date__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
            if end_date:
                session_qs = session_qs.filter(created_at__date__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
            session_count = session_qs.count()
            
            department_stats.append({
                'id': dept.id,
                'name': dept.name,
                'teacher_count': teacher_count,
                'subject_count': subject_count,
                'session_count': session_count
            })
        
        # Weekly session trends (last 8 weeks from end date or now)
        weekly_trends = []
        end_reference = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else timezone.now().date()
        for i in range(8):
            week_start = end_reference - timedelta(weeks=i)
            week_end = week_start + timedelta(days=6)
            week_filter = {'created_at__date__range': [week_start, week_end]}
            if start_date:
                week_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
            count = Session.objects.filter(**week_filter).count()
            weekly_trends.insert(0, {
                'week': f'Week {8-i}',
                'count': count
            })
        
        # Calculate totals
        total_sessions = Session.objects.filter(**session_filter).count() if session_filter else 0
        total_hours = Session.objects.filter(**session_filter).aggregate(total=Sum('duration'))['total'] or 0
        
        # Serialize teacher utilization for JavaScript
        teacher_utilization_list = [
            {
                'first_name': t.first_name,
                'last_name': t.last_name,
                'total_hours': float(t.total_hours) if t.total_hours else 0,
                'session_count': t.session_count or 0,
            }
            for t in teacher_utilization
        ]
        
        context = {
            'teacher_utilization': teacher_utilization_list,
            'department_stats': department_stats,
            'weekly_trends': weekly_trends,
            'start_date': start_date,
            'end_date': end_date,
            'total_sessions': total_sessions,
            'total_hours': float(total_hours),
        }
        
        return render(request, 'faculty/reports.html', context)


def check_session_conflicts(request):
    """AJAX view to check for session conflicts"""
    if request.method == 'GET':
        teacher_id = request.GET.get('teacher_id')
        day_of_week = request.GET.get('day_of_week')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        exclude_id = request.GET.get('exclude_id')
        
        if not all([teacher_id, day_of_week, start_time, end_time]):
            return JsonResponse({'has_conflict': False, 'message': 'Incomplete data'})
        
        try:
            # Convert time strings to time objects
            start = datetime.strptime(start_time, '%H:%M').time()
            end = datetime.strptime(end_time, '%H:%M').time()
            
            # Query for conflicts
            conflicts = Session.objects.filter(
                teacher_id=teacher_id,
                day_of_week=day_of_week,
                status='scheduled'
            )
            
            if exclude_id:
                conflicts = conflicts.exclude(pk=exclude_id)
            
            for session in conflicts:
                if (start < session.end_time and end > session.start_time):
                    return JsonResponse({
                        'has_conflict': True,
                        'message': f'Conflict with {session.subject.name} ({session.start_time} - {session.end_time})'
                    })
            
            return JsonResponse({'has_conflict': False, 'message': 'No conflicts found'})
            
        except Exception as e:
            return JsonResponse({'has_conflict': False, 'message': str(e)})
    
    return JsonResponse({'has_conflict': False, 'message': 'Invalid request'})


def get_all_teachers(request):
    """AJAX view to get all active teachers for autocomplete search"""
    teachers = Teacher.objects.filter(status='active').values(
        'id', 'first_name', 'last_name', 'email', 'specialization'
    )

    teacher_list = []
    for t in teachers:
        teacher_list.append({
            'id': t['id'],
            'name': f"{t['first_name']} {t['last_name']}",
            'email': t['email'],
            'specialization': t['specialization'] or ''
        })

    return JsonResponse({'teachers': teacher_list})


def get_teacher_subjects(request):
    """AJAX view to get subjects assigned to a teacher"""
    teacher_id = request.GET.get('teacher_id')

    if not teacher_id:
        return JsonResponse({'subjects': []})

    try:
        # Get subjects assigned to the teacher
        subjects = Subject.objects.filter(
            teachers__id=teacher_id
        ).distinct().values('id', 'code', 'name', 'program__name')

        return JsonResponse({'subjects': list(subjects)})
    except Exception as e:
        return JsonResponse({'subjects': [], 'error': str(e)})


class ExportPDFView(View):
    """Export Faculty Report as PDF"""
    
    def get(self, request):
        # Get date range from request parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Build session filter
        session_filter = {}
        if start_date:
            session_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            session_filter['created_at__date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Gather all data
        teachers = Teacher.objects.all().order_by('last_name', 'first_name')
        departments = Department.objects.all()
        programs = Program.objects.all()
        subjects = Subject.objects.all()
        
        # Filter sessions based on date range
        sessions = Session.objects.filter(**session_filter).order_by('created_at') if session_filter else Session.objects.all().order_by('created_at')
        
        # Build teacher performance data with date filtering
        teacher_performance = []
        for teacher in teachers:
            teacher_sessions = sessions.filter(teacher=teacher)
            session_count = teacher_sessions.count()
            total_duration = teacher_sessions.aggregate(total=Sum('duration'))['total'] or 0
            
            teacher_performance.append({
                'teacher': teacher,
                'sessions_conducted': session_count,
                'total_duration': float(total_duration),
            })
        
        # Filter to only include teachers with activity in the date range
        active_teachers = [tp for tp in teacher_performance if tp['sessions_conducted'] > 0]
        
        # Calculate total duration for summary
        total_duration_all = sum(tp['total_duration'] for tp in active_teachers)
        
        context = {
            'teachers': teachers,
            'departments': departments,
            'programs': programs,
            'subjects': subjects,
            'sessions': sessions,
            'teacher_performance': active_teachers,
            'total_duration_all': total_duration_all,
            'generated_date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'start_date': start_date,
            'end_date': end_date,
        }
        
        # Render HTML template
        html = render_to_string('faculty/report_pdf.html', context)
        
        # Convert to PDF using xhtml2pdf
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode('UTF-8')), result)
        
        if pdf.err:
            # If PDF generation fails, return HTML instead
            response = HttpResponse(html, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename="faculty_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.html"'
            return response
        
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="faculty_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        return response
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="faculty_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        return response


class ExportExcelView(View):
    """Export Schedule Report as Excel (CSV format)"""
    
    def get(self, request):
        # Get filter parameters
        teacher_id = request.GET.get('teacher')
        day = request.GET.get('day')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        sessions = Session.objects.select_related('teacher', 'subject', 'subject__program').all()
        
        if teacher_id:
            sessions = sessions.filter(teacher_id=teacher_id)
        if day:
            sessions = sessions.filter(day_of_week=day)
        if start_date:
            sessions = sessions.filter(created_at__date__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            sessions = sessions.filter(created_at__date__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
        
        sessions = sessions.order_by('day_of_week', 'start_time')
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="schedule_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Day', 'Time', 'Teacher', 'Subject', 'Program', 'Room', 'Duration (hrs)', 'Status'])
        
        for session in sessions:
            writer.writerow([
                session.get_day_of_week_display(),
                f"{session.start_time} - {session.end_time}",
                str(session.teacher),
                session.subject.name,
                session.subject.program.name,
                session.room or 'N/A',
                session.duration,
                session.get_status_display()
            ])
        
        return response


class ExportCSVView(View):
    """Export Attendance Data as CSV"""
    
    def get(self, request):
        # Get filter parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Build filter
        filter_kwargs = {}
        if start_date:
            filter_kwargs['date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            filter_kwargs['date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get attendance records with related data
        attendance_query = Attendance.objects.select_related(
            'teacher', 'session', 'session__subject'
        ).all().order_by('-date')
        
        if filter_kwargs:
            attendance_records = attendance_query.filter(**filter_kwargs)[:500]
        else:
            attendance_records = attendance_query[:500]
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Teacher', 'Subject', 'Session Date', 'Status', 'Check In', 'Check Out', 'Notes'])
        
        for record in attendance_records:
            writer.writerow([
                record.date,
                str(record.teacher),
                record.session.subject.name if record.session and record.session.subject else 'N/A',
                record.session.date if record.session else 'N/A',
                record.get_status_display(),
                record.check_in_time or 'N/A',
                record.check_out_time or 'N/A',
                record.notes[:100] if record.notes else ''  # Limit notes to 100 chars
            ])
        
        return response


class ExportTeacherDetailsView(View):
    """Export Teacher Details with Classes and Timings as Excel"""
    
    def get(self, request):
        # Get filter parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Build session filter
        session_filter = {}
        if start_date:
            session_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            session_filter['created_at__date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get all teachers
        teachers = Teacher.objects.all().order_by('last_name', 'first_name')
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="teacher_details_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Teacher Name', 'Employee ID', 'Email', 'Department', 'Qualification',
            'Subject', 'Program', 'Day', 'Time', 'Room', 'Duration (hrs)', 'Status', 'Session Date'
        ])
        
        for teacher in teachers:
            # Get sessions for this teacher with optional date filtering
            sessions_qs = Session.objects.select_related('subject', 'subject__program').filter(teacher=teacher)
            if session_filter:
                sessions_qs = sessions_qs.filter(**session_filter)
            
            sessions = sessions_qs.order_by('day_of_week', 'start_time')
            
            if sessions:
                for session in sessions:
                    writer.writerow([
                        str(teacher),
                        teacher.employee_id,
                        teacher.email,
                        teacher.department.name if teacher.department else 'N/A',
                        teacher.qualification or 'N/A',
                        session.subject.name,
                        session.subject.program.name,
                        session.get_day_of_week_display(),
                        f"{session.start_time} - {session.end_time}",
                        session.room or 'N/A',
                        session.duration,
                        session.get_status_display(),
                        session.date
                    ])
            else:
                # Write teacher row with no sessions
                writer.writerow([
                    str(teacher),
                    teacher.employee_id,
                    teacher.email,
                    teacher.department.name if teacher.department else 'N/A',
                    teacher.qualification or 'N/A',
                    'No sessions', '', '', '', '', 0, '', ''
                ])
        
        return response


class ExportSingleTeacherView(View):
    """Export individual teacher profile details with classes to Excel"""
    
    def get(self, request, pk):
        # Get teacher
        teacher = get_object_or_404(Teacher, pk=pk)
        
        # Get filter parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Build session filter
        session_filter = {'teacher': teacher}
        if start_date:
            session_filter['created_at__date__gte'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            session_filter['created_at__date__lte'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get teacher's sessions
        sessions = Session.objects.select_related(
            'subject', 'subject__program'
        ).filter(**session_filter).order_by('day_of_week', 'start_time')
        
        # Calculate summary statistics
        total_sessions = sessions.count()
        total_hours = sessions.aggregate(total=Sum('duration'))['total'] or 0
        
        # Get assigned subjects
        assigned_subjects = teacher.subjects.all().select_related('program')
        
        # Get attendance records
        attendance_records = Attendance.objects.filter(
            teacher=teacher
        ).select_related('session', 'session__subject').order_by('-date')[:100]
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="teacher_profile_{teacher.employee_id}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['=' * 50])
        writer.writerow(['FACULTY TRACKER - TEACHER PROFILE REPORT'])
        writer.writerow(['=' * 50])
        writer.writerow([])
        
        # Teacher Personal Information Section
        writer.writerow(['PERSONAL INFORMATION'])
        writer.writerow(['Full Name', f"{teacher.first_name} {teacher.last_name}"])
        writer.writerow(['Employee ID', teacher.employee_id])
        writer.writerow(['Email', teacher.email])
        writer.writerow(['Phone', teacher.phone])
        writer.writerow(['Address', teacher.address or 'N/A'])
        writer.writerow(['Date of Birth', teacher.date_of_birth or 'N/A'])
        writer.writerow(['Gender', teacher.get_gender_display()])
        writer.writerow([])
        
        # Professional Information Section
        writer.writerow(['PROFESSIONAL INFORMATION'])
        writer.writerow(['Department', teacher.department.name if teacher.department else 'Not Assigned'])
        writer.writerow(['Qualification', teacher.qualification or 'N/A'])
        writer.writerow(['Specialization', teacher.specialization or 'N/A'])
        writer.writerow(['Experience (Years)', teacher.experience_years])
        writer.writerow(['Hourly Rate', teacher.hourly_rate])
        writer.writerow(['Status', teacher.get_status_display()])
        writer.writerow(['Hire Date', teacher.hire_date or 'N/A'])
        writer.writerow([])
        
        # Emergency Contact Section
        writer.writerow(['EMERGENCY CONTACT'])
        writer.writerow(['Contact Name', teacher.emergency_contact_name or 'N/A'])
        writer.writerow(['Contact Phone', teacher.emergency_contact_phone or 'N/A'])
        writer.writerow([])
        
        # Assigned Subjects Section
        writer.writerow(['ASSIGNED SUBJECTS'])
        writer.writerow(['Subject Code', 'Subject Name', 'Program', 'Type', 'Semester'])
        for subject in assigned_subjects:
            writer.writerow([
                subject.code,
                subject.name,
                subject.program.name,
                subject.get_subject_type_display(),
                subject.get_semester_display() if subject.semester else 'N/A'
            ])
        if not assigned_subjects:
            writer.writerow(['No subjects assigned'])
        writer.writerow([])
        
        # Summary Statistics Section
        writer.writerow(['CLASS SUMMARY'])
        writer.writerow(['Period', f"{start_date or 'All Time'} to {end_date or 'Present'}"])
        writer.writerow(['Total Classes Conducted', total_sessions])
        writer.writerow(['Total Teaching Hours', float(total_hours)])
        writer.writerow([])
        
        # Detailed Classes Section
        writer.writerow(['DETAILED CLASSES'])
        writer.writerow(['Day', 'Date', 'Time', 'Subject', 'Program', 'Room', 'Duration (hrs)', 'Status', 'Notes'])
        for session in sessions:
            writer.writerow([
                session.get_day_of_week_display(),
                session.date,
                f"{session.start_time} - {session.end_time}",
                session.subject.name,
                session.subject.program.name,
                session.room or 'N/A',
                session.duration,
                session.get_status_display(),
                session.notes[:100] if session.notes else ''
            ])
        if not sessions:
            writer.writerow(['No classes scheduled'])
        writer.writerow([])
        
        # Attendance Records Section
        writer.writerow(['ATTENDANCE RECORDS'])
        writer.writerow(['Date', 'Subject', 'Status', 'Check In', 'Check Out', 'Notes'])
        for record in attendance_records:
            writer.writerow([
                record.date,
                record.session.subject.name if record.session and record.session.subject else 'N/A',
                record.get_status_display(),
                record.check_in_time or 'N/A',
                record.check_out_time or 'N/A',
                record.notes[:100] if record.notes else ''
            ])
        if not attendance_records:
            writer.writerow(['No attendance records'])
        writer.writerow([])
        
        # Footer
        writer.writerow(['=' * 50])
        writer.writerow([f'Report Generated: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'])
        writer.writerow(['Faculty Tracker System'])
        writer.writerow(['=' * 50])
        
        return response


# Add missing import for Q objects
from django.db import models
