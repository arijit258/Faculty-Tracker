from django import forms
from .models import Teacher, Subject, Session, Department, Attendance, ClassRoom, Program
from django.core.exceptions import ValidationError
from django.utils import timezone


class TeacherForm(forms.ModelForm):
    """Form for creating and updating teacher records"""
    
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address',
            'date_of_birth', 'gender', 'photo', 'employee_id',
            'department', 'qualification', 'specialization',
            'experience_years', 'hourly_rate', 'status',
            'emergency_contact_name', 'emergency_contact_phone', 'hire_date'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employee ID'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter qualification'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter specialization'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Years of experience'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Hourly rate'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact name'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact phone'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if Teacher.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A teacher with this email already exists.")
        return email
    
    def clean_employee_id(self):
        """Validate employee ID uniqueness"""
        employee_id = self.cleaned_data.get('employee_id')
        if Teacher.objects.filter(employee_id=employee_id).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A teacher with this employee ID already exists.")
        return employee_id
    
    def clean_hourly_rate(self):
        """Ensure hourly rate is non-negative"""
        rate = self.cleaned_data.get('hourly_rate')
        if rate and rate < 0:
            raise ValidationError("Hourly rate cannot be negative.")
        return rate


class SubjectForm(forms.ModelForm):
    """Form for creating and updating subjects"""

    class Meta:
        model = Subject
        fields = ['code', 'name', 'program', 'teachers', 'description']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject code (e.g., CS101)'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject name'
            }),
            'program': forms.Select(attrs={
                'class': 'form-select custom-select'
            }),
            'teachers': forms.SelectMultiple(attrs={
                'class': 'form-select select2',
                'multiple': 'multiple',
                'data-placeholder': 'Select teachers...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Subject description (optional)',
                'required': False
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teachers'].queryset = Teacher.objects.filter(status='active')
        self.fields['description'].required = False
        # Program dropdown will show the program name (updated in model __str__)

    def clean_code(self):
        """Validate subject code uniqueness per program"""
        code = self.cleaned_data.get('code', '').upper()
        program = self.cleaned_data.get('program')
        if program and code:
            if Subject.objects.filter(code=code, program=program).exclude(pk=self.instance.pk).exists():
                raise ValidationError(f"A subject with code '{code}' already exists in {program.name}.")
        return code


class SessionForm(forms.ModelForm):
    """Form for scheduling class sessions"""
    
    class Meta:
        model = Session
        fields = ['teacher', 'subject', 'date', 'day_of_week', 'start_time', 
                  'end_time', 'room', 'status', 'notes', 'is_recurring']
        widgets = {
            'teacher': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_teacher'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_subject'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room number/Location'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(status='active')
    
    def clean(self):
        """Validate session timing and check for conflicts"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        teacher = cleaned_data.get('teacher')
        date = cleaned_data.get('date')
        day_of_week = cleaned_data.get('day_of_week')
        
        # Check if end time is after start time
        if start_time and end_time and start_time >= end_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.'
            })
        
        # Check for scheduling conflicts using date
        if teacher and date and start_time and end_time:
            conflicts = Session.objects.filter(
                teacher=teacher,
                date=date,
                status='scheduled'
            ).exclude(pk=self.instance.pk)
            
            for session in conflicts:
                if (start_time < session.end_time and end_time > session.start_time):
                    raise ValidationError(
                        f"Teacher {teacher.full_name} already has a class scheduled "
                        f"from {session.start_time} to {session.end_time} on {session.date}."
                    )
        
        return cleaned_data


class ProgramForm(forms.ModelForm):
    """Form for creating and updating programs"""

    class Meta:
        model = Program
        fields = ['name', 'code', 'start_date', 'end_date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Program name (e.g., B.Tech)'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Program code (e.g., BTECH)'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Program description (required)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Description is now mandatory
        self.fields['description'].required = True

    def clean(self):
        """Validate that end date is after start date"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError({
                'end_date': 'End date must be after start date.'
            })

        return cleaned_data

    def clean_code(self):
        """Validate program code uniqueness"""
        code = self.cleaned_data.get('code', '').upper()
        if code:
            if Program.objects.filter(code__iexact=code).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A program with this code already exists.")
        return code

    def clean_name(self):
        """Validate program name uniqueness"""
        name = self.cleaned_data.get('name', '')
        if name:
            if Program.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A program with this name already exists.")
        return name


class DepartmentForm(forms.ModelForm):
    """Form for creating and updating departments"""
    
    class Meta:
        model = Department
        fields = ['name', 'description', 'teachers']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Department description (optional)',
                'required': False
            }),
            'teachers': forms.SelectMultiple(attrs={
                'class': 'form-select select2',
                'multiple': 'multiple',
                'data-placeholder': 'Select teachers...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teachers'].queryset = Teacher.objects.filter(status='active')
        self.fields['description'].required = False
    
    def clean_name(self):
        """Validate department name uniqueness"""
        name = self.cleaned_data.get('name', '')
        if name:
            if Department.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A department with this name already exists.")
        return name


class AttendanceForm(forms.ModelForm):
    """Form for tracking session attendance"""
    
    class Meta:
        model = Attendance
        fields = ['session', 'teacher', 'date', 'status', 
                  'check_in_time', 'check_out_time', 'actual_duration', 'notes']
        widgets = {
            'session': forms.Select(attrs={
                'class': 'form-select'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'check_in_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'check_out_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'actual_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.25',
                'placeholder': 'Actual duration in hours'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
        }
    
    def clean(self):
        """Validate attendance record"""
        cleaned_data = super().clean()
        session = cleaned_data.get('session')
        teacher = cleaned_data.get('teacher')
        date = cleaned_data.get('date')
        
        # Check for duplicate attendance records
        if session and teacher and date:
            existing = Attendance.objects.filter(
                session=session,
                teacher=teacher,
                date=date
            ).exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError(
                    f"Attendance record already exists for {teacher.full_name} "
                    f"on {date} for this session."
                )
        
        return cleaned_data


class ClassRoomForm(forms.ModelForm):
    """Form for managing classrooms"""
    
    class Meta:
        model = ClassRoom
        fields = ['name', 'building', 'floor', 'capacity', 'room_type',
                  'has_projector', 'has_whiteboard', 'has_computer', 
                  'is_available', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room name/number'
            }),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Building name'
            }),
            'floor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Floor number'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Room capacity'
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'has_projector': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_whiteboard': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_computer': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
        }
    
    def clean_name(self):
        """Validate room name uniqueness"""
        name = self.cleaned_data.get('name')
        if ClassRoom.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A room with this name already exists.")
        return name


class SessionFilterForm(forms.Form):
    """Form for filtering sessions"""
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'filter_teacher'
        }),
        empty_label="All Teachers"
    )
    day_of_week = forms.ChoiceField(
        choices=[('', 'All Days')] + Session.DAYS_OF_WEEK,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'filter_subject'
        }),
        empty_label="All Subjects"
    )
