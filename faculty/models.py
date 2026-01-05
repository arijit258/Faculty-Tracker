from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Program(models.Model):
    """Program model for Easy2Learning - Jelet, Wbjee, Diploma, Btech, etc."""

    PROGRAM_TYPE_CHOICES = [
        ('jelet', 'JELET'),
        ('wbjee', 'WBJEE'),
        ('diploma', 'Diploma'),
        ('btech', 'B.Tech'),
        ('mtech', 'M.Tech'),
        ('others', 'Others'),
    ]

    DURATION_CHOICES = [
        (1, '1 Year'),
        (2, '2 Years'),
        (3, '3 Years'),
        (4, '4 Years'),
        (5, '5 Years'),
    ]

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES)
    duration_years = models.IntegerField(choices=DURATION_CHOICES, default=4)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_program_type_display()})"

    @property
    def total_subjects(self):
        """Return total number of subjects in this program"""
        return self.subject_set.count()


class Department(models.Model):
    """Department model for organizing faculty members"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    teachers = models.ManyToManyField('Teacher', related_name='departments', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Teacher/Faculty model with comprehensive details"""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefer_not_to_say')
    photo = models.ImageField(upload_to='teachers/', null=True, blank=True)

    # Professional Information
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    # Timestamps
    hire_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        """Return full name of the teacher"""
        return f"{self.first_name} {self.last_name}"

    @property
    def total_hours_taught(self):
        """Calculate total hours taught by this teacher"""
        sessions = self.session_set.all()
        total_hours = sum(session.duration for session in sessions)
        return round(total_hours, 2)

    @property
    def total_sessions_conducted(self):
        """Return total number of sessions conducted"""
        return self.session_set.count()

    @property
    def assigned_subjects(self):
        """Return all subjects assigned to this teacher"""
        return Subject.objects.filter(teachers=self)


class Subject(models.Model):
    """Subject/Course model belonging to a Program"""

    SUBJECT_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('both', 'Both'),
    ]

    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
        (9, '9th Semester'),
        (10, '10th Semester'),
    ]

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES, default='theory')
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    credits = models.PositiveIntegerField(default=1)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    teachers = models.ManyToManyField('Teacher', related_name='subjects', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        unique_together = ['code', 'program']
        ordering = ['program', 'semester', 'code']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.program.name})"

    @property
    def assigned_teachers(self):
        """Return all teachers assigned to this subject"""
        return self.teachers.all()

    @property
    def total_sessions(self):
        """Return total number of sessions for this subject"""
        return self.session_set.count()


class Session(models.Model):
    """Class session/schedule model"""

    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    day_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DecimalField(max_digits=5, decimal_places=2, help_text="Duration in hours")
    room = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['-date', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.teacher.full_name} - {self.subject.name} ({self.date})"

    @property
    def formatted_time(self):
        """Return formatted time string"""
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

    @property
    def is_conflicting(self):
        """Check if this session conflicts with other sessions"""
        conflicts = Session.objects.filter(
            teacher=self.teacher,
            date=self.date,
            status='scheduled'
        ).exclude(pk=self.pk)

        for session in conflicts:
            if (self.start_time < session.end_time and
                self.end_time > session.start_time):
                return True
        return False


class Attendance(models.Model):
    """Track session attendance"""

    SESSION_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    actual_duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['session', 'teacher', 'date']

    def __str__(self):
        return f"{self.teacher.full_name} - {self.session.subject.name} - {self.date}"


class ClassRoom(models.Model):
    """Classroom/Location model"""

    ROOM_TYPE_CHOICES = [
        ('classroom', 'Classroom'),
        ('lab', 'Laboratory'),
        ('auditorium', 'Auditorium'),
        ('meeting_room', 'Meeting Room'),
    ]

    name = models.CharField(max_length=50, unique=True)
    building = models.CharField(max_length=50, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    capacity = models.PositiveIntegerField(default=30)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='classroom')
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=True)
    has_computer = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.building})"
