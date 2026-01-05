"""
Django management command to create 10 teachers with 10 sessions each.
Run with: python manage.py create_teacher_sessions --clear

Easy2Learning Institute Structure:
- Creates 10 teachers
- Creates 10 sessions per teacher (100 total sessions)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta, date
import random
from faculty.models import Department, Teacher, Program, Subject, Session, ClassRoom


class Command(BaseCommand):
    help = 'Create 10 teachers with 10 sessions each for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing teacher and session data before creating new data'
        )

    def handle(self, *args, **options):
        clear_data = options['clear']

        self.stdout.write(self.style.NOTICE('=' * 70))
        self.stdout.write(self.style.NOTICE('Creating 10 Teachers with 10 Sessions Each'))
        self.stdout.write(self.style.NOTICE('Easy2Learning Institute'))
        self.stdout.write(self.style.NOTICE('=' * 70))

        # Clear existing data if requested
        if clear_data:
            self.clear_data()
            self.stdout.write(self.style.WARNING('Cleared existing teacher and session data.'))

        # Create required data
        self.create_departments()
        self.create_classrooms()
        self.create_programs()
        self.create_subjects()

        # Create 10 teachers
        self.create_teachers(10)

        # Assign teachers to subjects
        self.assign_teachers_to_subjects()

        # Create 10 sessions per teacher (100 total)
        self.create_sessions_per_teacher(10)

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.HTTP_INFO(f'\nSummary:'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Department.objects.count()} Departments'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Program.objects.count()} Programs'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Subject.objects.count()} Subjects'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Teacher.objects.count()} Teachers'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Session.objects.count()} Sessions'))
        self.stdout.write(self.style.HTTP_INFO(f'\nEach teacher has approximately 10 sessions.'))
        self.stdout.write(self.style.HTTP_INFO('\nRun: python manage.py runserver'))

    def clear_data(self):
        """Clear existing teacher and session data"""
        Session.objects.all().delete()
        Subject.objects.all().delete()
        Teacher.objects.all().delete()
        Program.objects.all().delete()
        ClassRoom.objects.all().delete()
        Department.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared all existing data...'))

    def create_departments(self):
        """Create department records"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Departments...'))

        departments_data = [
            {'name': 'Computer Science & Engineering', 'description': 'Software development and computing'},
            {'name': 'Electrical Engineering', 'description': 'Electrical systems and circuit design'},
            {'name': 'Mechanical Engineering', 'description': 'Mechanical systems and design'},
            {'name': 'Electronics & Communication', 'description': 'Electronic systems and communication'},
            {'name': 'Basic Sciences', 'description': 'Physics, Chemistry, and Mathematics'},
        ]

        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {dept.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Already exists: {dept.name}'))

    def create_classrooms(self):
        """Create classroom records"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Classrooms...'))

        classrooms_data = [
            {'name': 'Room 101', 'building': 'Main Building', 'floor': '1st Floor', 'capacity': 50, 'room_type': 'classroom'},
            {'name': 'Room 102', 'building': 'Main Building', 'floor': '1st Floor', 'capacity': 45, 'room_type': 'classroom'},
            {'name': 'Room 201', 'building': 'Main Building', 'floor': '2nd Floor', 'capacity': 40, 'room_type': 'classroom'},
            {'name': 'Room 202', 'building': 'Main Building', 'floor': '2nd Floor', 'capacity': 35, 'room_type': 'classroom'},
            {'name': 'Lab CS-1', 'building': 'Tech Block', 'floor': '1st Floor', 'capacity': 30, 'room_type': 'lab'},
            {'name': 'Lab CS-2', 'building': 'Tech Block', 'floor': '1st Floor', 'capacity': 30, 'room_type': 'lab'},
            {'name': 'Auditorium', 'building': 'Main Building', 'floor': 'Ground Floor', 'capacity': 250, 'room_type': 'auditorium'},
        ]

        for room_data in classrooms_data:
            room, created = ClassRoom.objects.get_or_create(
                name=room_data['name'],
                defaults=room_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {room.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Already exists: {room.name}'))

    def create_programs(self):
        """Create program records with start_date and end_date"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Programs...'))

        # Calculate academic years
        current_year = date.today().year
        btech_start = date(current_year - 3, 8, 1)  # August 1st, 3 years ago
        btech_end = date(current_year + 1, 5, 31)   # May 31st, next year (4 years total)

        mtech_start = date(current_year - 1, 8, 1)  # August 1st, 1 year ago
        mtech_end = date(current_year + 1, 5, 31)   # May 31st, next year (2 years total)

        programs_data = [
            {
                'name': 'B.Tech',
                'code': 'BTECH',
                'program_type': 'btech',
                'start_date': btech_start,
                'end_date': btech_end,
                'description': 'Bachelor of Technology - 4 Year Program'
            },
            {
                'name': 'M.Tech',
                'code': 'MTECH',
                'program_type': 'mtech',
                'start_date': mtech_start,
                'end_date': mtech_end,
                'description': 'Master of Technology - 2 Year Program'
            },
        ]

        for prog_data in programs_data:
            prog, created = Program.objects.get_or_create(
                code=prog_data['code'],
                defaults=prog_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {prog.name} ({prog.start_date} to {prog.end_date})'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Already exists: {prog.name}'))

    def create_subjects(self):
        """Create subjects for each program"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Subjects...'))

        subject_templates = {
            'BTECH': {
                1: [
                    {'code': 'CS101', 'name': 'Introduction to Programming', 'subject_type': 'both', 'credits': 4, 'total_hours': 40},
                    {'code': 'CS102', 'name': 'Data Structures', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'MA101', 'name': 'Mathematics-I', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'PH101', 'name': 'Physics-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                ],
                2: [
                    {'code': 'CS201', 'name': 'Algorithms', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'CS202', 'name': 'Database Systems', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'MA201', 'name': 'Mathematics-II', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'PH201', 'name': 'Physics-II', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                ],
                3: [
                    {'code': 'CS301', 'name': 'Operating Systems', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS302', 'name': 'Computer Networks', 'subject_type': 'theory', 'credits': 4, 'total_hours': 45},
                    {'code': 'CS303', 'name': 'Web Development', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS304', 'name': 'Software Engineering', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                4: [
                    {'code': 'CS401', 'name': 'Machine Learning', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS402', 'name': 'Cloud Computing', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS403', 'name': 'Cyber Security', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS404', 'name': 'Artificial Intelligence', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
            },
            'MTECH': {
                1: [
                    {'code': 'MT101', 'name': 'Advanced Algorithms', 'subject_type': 'theory', 'credits': 4, 'total_hours': 45},
                    {'code': 'MT102', 'name': 'Research Methodology', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'MT103', 'name': 'Advanced ML', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'MT104', 'name': 'Deep Learning', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                2: [
                    {'code': 'MT201', 'name': 'Thesis/Dissertation', 'subject_type': 'practical', 'credits': 12, 'total_hours': 150},
                ],
            },
        }

        programs = list(Program.objects.all())
        created_count = 0

        for program in programs:
            templates = subject_templates.get(program.code, subject_templates['BTECH'])

            for semester, subjects in templates.items():
                for subj_data in subjects:
                    # Make semester optional - None for subjects without semester
                    semester_value = semester if semester else None
                    subject, created = Subject.objects.get_or_create(
                        code=subj_data['code'],
                        program=program,
                        defaults={
                            'name': subj_data['name'],
                            'subject_type': subj_data['subject_type'],
                            'semester': semester_value,
                            'credits': subj_data['credits'],
                            'total_hours': subj_data['total_hours'],
                            'is_active': True
                        }
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} subjects'))

    def create_teachers(self, count):
        """Create teacher records"""
        self.stdout.write(self.style.HTTP_INFO(f'\nCreating {count} Teachers...'))

        teachers_data = [
            {'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith', 'specialization': 'Data Structures', 'qualification': 'Ph.D. Computer Science'},
            {'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah.johnson', 'specialization': 'Algorithms', 'qualification': 'M.Tech Computer Science'},
            {'first_name': 'Michael', 'last_name': 'Williams', 'email': 'michael.williams', 'specialization': 'Machine Learning', 'qualification': 'Ph.D. AI'},
            {'first_name': 'Emily', 'last_name': 'Brown', 'email': 'emily.brown', 'specialization': 'Web Development', 'qualification': 'M.Sc Computer Science'},
            {'first_name': 'David', 'last_name': 'Jones', 'email': 'david.jones', 'specialization': 'Database Systems', 'qualification': 'B.Tech Computer Science'},
            {'first_name': 'Jessica', 'last_name': 'Davis', 'email': 'jessica.davis', 'specialization': 'Operating Systems', 'qualification': 'M.Tech Computer Science'},
            {'first_name': 'Robert', 'last_name': 'Miller', 'email': 'robert.miller', 'specialization': 'Computer Networks', 'qualification': 'Ph.D. Computer Science'},
            {'first_name': 'Amanda', 'last_name': 'Wilson', 'email': 'amanda.wilson', 'specialization': 'Software Engineering', 'qualification': 'M.Sc Software Engineering'},
            {'first_name': 'James', 'last_name': 'Moore', 'email': 'james.moore', 'specialization': 'Cyber Security', 'qualification': 'M.Tech Cyber Security'},
            {'first_name': 'Ashley', 'last_name': 'Taylor', 'email': 'ashley.taylor', 'specialization': 'Cloud Computing', 'qualification': 'Ph.D. Computer Science'},
        ]

        departments = list(Department.objects.all())
        today = timezone.now().date()

        created_count = 0
        for i, data in enumerate(teachers_data):
            if Teacher.objects.filter(employee_id=f'FAC{str(i + 1).zfill(4)}').exists():
                continue

            teacher = Teacher(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=f"{data['email']}{i}@easy2learning.com",
                phone=f'+91 98765{str(random.randint(10000, 99999))}',
                address=f'{random.randint(1, 100)} Academic Way, Kolkata',
                date_of_birth=datetime(1975, 1, 1) + timedelta(days=random.randint(1, 365 * 10)),
                gender=random.choice(['male', 'female']),
                employee_id=f'FAC{str(i + 1).zfill(4)}',
                department=random.choice(departments) if departments else None,
                qualification=data['qualification'],
                specialization=data['specialization'],
                experience_years=random.randint(3, 15),
                hourly_rate=random.randint(800, 2500) + random.randint(0, 99) / 100,
                status='active',
                emergency_contact_name=f'{data["first_name"]} Family',
                emergency_contact_phone=f'+91 98765{str(random.randint(10000, 99999))}',
                hire_date=today - timedelta(days=random.randint(365, 2000))
            )
            teacher.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {teacher.full_name} ({teacher.employee_id})'))

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} teachers'))

    def assign_teachers_to_subjects(self):
        """Assign teachers to subjects"""
        self.stdout.write(self.style.HTTP_INFO('\nAssigning Teachers to Subjects...'))

        teachers = list(Teacher.objects.filter(status='active'))
        subjects = list(Subject.objects.all())

        random.seed(42)
        total_assignments = 0

        for subject in subjects:
            # Assign 2-4 teachers to each subject
            num_teachers = random.randint(2, min(4, len(teachers)))
            selected_teachers = random.sample(teachers, num_teachers)

            for teacher in selected_teachers:
                if not subject.teachers.filter(pk=teacher.pk).exists():
                    subject.teachers.add(teacher)
                    total_assignments += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {total_assignments} teacher-subject assignments'))

    def create_sessions_per_teacher(self, sessions_per_teacher):
        """Create exactly 10 sessions for each teacher"""
        self.stdout.write(self.style.HTTP_INFO(f'\nCreating {sessions_per_teacher} sessions per teacher...'))

        teachers = list(Teacher.objects.filter(status='active'))
        rooms = list(ClassRoom.objects.all())

        if not teachers:
            self.stdout.write(self.style.ERROR('  ✗ No teachers found.'))
            return

        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        time_slots = [
            ('08:00', '09:00', 1.0),
            ('09:00', '10:00', 1.0),
            ('10:00', '11:00', 1.0),
            ('11:00', '12:00', 1.0),
            ('14:00', '15:00', 1.0),
            ('15:00', '16:00', 1.0),
            ('16:00', '17:00', 1.0),
            ('09:00', '11:00', 2.0),
            ('14:00', '16:00', 2.0),
        ]

        today = timezone.now().date()
        days_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5}

        random.seed(42)
        total_sessions = 0

        for teacher in teachers:
            # Get subjects this teacher is assigned to
            subjects = list(Subject.objects.filter(teachers=teacher, is_active=True))

            if not subjects:
                # If no subjects assigned, assign all subjects
                subjects = list(Subject.objects.filter(is_active=True))

            created_for_teacher = 0
            attempts = 0
            max_attempts = sessions_per_teacher * 3

            while created_for_teacher < sessions_per_teacher and attempts < max_attempts:
                attempts += 1

                subject = random.choice(subjects)
                day = random.choice(days_of_week)
                start_time_str, end_time_str, duration = random.choice(time_slots)

                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                # Find next occurrence of this day
                target_day = days_map[day]
                current_weekday = today.weekday()
                days_ahead = target_day - current_weekday
                if days_ahead <= 0:
                    days_ahead += 7

                session_date = today + timedelta(days=days_ahead + random.randint(0, 8))
                room = random.choice(rooms) if rooms else None

                # Check for conflicts
                existing_conflicts = Session.objects.filter(
                    teacher=teacher,
                    date=session_date,
                    status='scheduled'
                ).filter(
                    start_time__lt=end_time,
                    end_time__gt=start_time
                )

                if existing_conflicts.exists():
                    continue

                session = Session(
                    teacher=teacher,
                    subject=subject,
                    date=session_date,
                    day_of_week=day,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    room=room.name if room else f'Room {random.randint(1, 10)}',
                    status=random.choice(['scheduled', 'completed']),
                    notes=f'Class for {subject.name}',
                    is_recurring=random.choice([True, False])
                )
                session.save()
                created_for_teacher += 1
                total_sessions += 1

            self.stdout.write(self.style.SUCCESS(f'  ✓ {teacher.full_name}: {created_for_teacher} sessions created'))

        self.stdout.write(self.style.SUCCESS(f'\n  ✓ Total sessions created: {total_sessions}'))
