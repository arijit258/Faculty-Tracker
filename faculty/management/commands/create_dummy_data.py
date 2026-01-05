"""
Django management command to create dummy data for Faculty Tracker.
Run with: python manage.py create_dummy_data

Easy2Learning Institute Structure:
- Programs: JELET, WBJEE, Diploma, B.Tech, M.Tech, Others
- Subjects: Under each program (semester-wise)
- Teachers: Assigned to subjects (many-to-many)
- Sessions: Classes logged for teachers teaching subjects
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from faculty.models import Department, Teacher, Program, Subject, Session, ClassRoom


class Command(BaseCommand):
    help = 'Create dummy data for testing the Faculty Tracker application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num-teachers',
            type=int,
            default=25,
            help='Number of teachers to create (default: 25)'
        )
        parser.add_argument(
            '--num-sessions',
            type=int,
            default=150,
            help='Number of sessions to create (default: 150)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    def handle(self, *args, **options):
        num_teachers = options['num_teachers']
        num_sessions = options['num_sessions']
        clear_data = options['clear']

        self.stdout.write(self.style.NOTICE('=' * 70))
        self.stdout.write(self.style.NOTICE('Creating Dummy Data for Faculty Tracker'))
        self.stdout.write(self.style.NOTICE('Easy2Learning Institute - Programs & Subjects Structure'))
        self.stdout.write(self.style.NOTICE('=' * 70))

        # Clear existing data if requested
        if clear_data:
            self.clear_data()
            self.stdout.write(self.style.WARNING('Cleared all existing data.'))
        
        # Create departments
        self.create_departments()
        
        # Create classrooms
        self.create_classrooms()
        
        # Create programs
        self.create_programs()
        
        # Create subjects
        self.create_subjects()
        
        # Create teachers
        self.create_teachers(num_teachers)
        
        # Assign teachers to subjects
        self.assign_teachers_to_subjects()
        
        # Create sessions
        self.create_sessions(num_sessions)
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.HTTP_INFO(f'\nSummary:'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Department.objects.count()} Departments'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {ClassRoom.objects.count()} Classrooms'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Program.objects.count()} Programs'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Subject.objects.count()} Subjects'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Teacher.objects.count()} Teachers'))
        self.stdout.write(self.style.HTTP_INFO(f'  - {Session.objects.count()} Sessions'))
        self.stdout.write(self.style.HTTP_INFO('\nRun: python manage.py runserver'))

    def clear_data(self):
        """Clear all existing data in correct order"""
        Session.objects.all().delete()
        Subject.objects.all().delete()  # Clears ManyToMany with teachers
        Teacher.objects.all().delete()
        Program.objects.all().delete()
        Department.objects.all().delete()
        ClassRoom.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared all existing data...'))

    def create_departments(self):
        """Create department records"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Departments...'))
        
        departments_data = [
            {'name': 'Computer Science & Engineering', 'description': 'Software development, algorithms, and computing theory'},
            {'name': 'Electrical Engineering', 'description': 'Electrical systems and circuit design'},
            {'name': 'Mechanical Engineering', 'description': 'Mechanical systems and design'},
            {'name': 'Civil Engineering', 'description': 'Infrastructure and construction'},
            {'name': 'Electronics & Communication', 'description': 'Electronic systems and communication'},
            {'name': 'Information Technology', 'description': 'IT infrastructure and software'},
            {'name': 'Basic Sciences', 'description': 'Physics, Chemistry, and Mathematics'},
            {'name': 'Humanities & Management', 'description': 'Language, economics, and management'},
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
            {'name': 'Room 101', 'building': 'Main Building', 'floor': '1st Floor', 'capacity': 50, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Room 102', 'building': 'Main Building', 'floor': '1st Floor', 'capacity': 45, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Room 201', 'building': 'Main Building', 'floor': '2nd Floor', 'capacity': 40, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Room 202', 'building': 'Main Building', 'floor': '2nd Floor', 'capacity': 35, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Room 301', 'building': 'Main Building', 'floor': '3rd Floor', 'capacity': 40, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Room 302', 'building': 'Main Building', 'floor': '3rd Floor', 'capacity': 35, 'room_type': 'classroom', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Lab CS-1', 'building': 'Tech Block', 'floor': '1st Floor', 'capacity': 30, 'room_type': 'lab', 'has_projector': True, 'has_whiteboard': True, 'has_computer': True},
            {'name': 'Lab CS-2', 'building': 'Tech Block', 'floor': '1st Floor', 'capacity': 30, 'room_type': 'lab', 'has_projector': True, 'has_whiteboard': True, 'has_computer': True},
            {'name': 'Lab EE-1', 'building': 'Tech Block', 'floor': '2nd Floor', 'capacity': 25, 'room_type': 'lab', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Lab ME-1', 'building': 'Tech Block', 'floor': 'Ground Floor', 'capacity': 25, 'room_type': 'lab', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Lab EC-1', 'building': 'Tech Block', 'floor': '2nd Floor', 'capacity': 25, 'room_type': 'lab', 'has_projector': True, 'has_whiteboard': True, 'has_computer': True},
            {'name': 'Auditorium', 'building': 'Main Building', 'floor': 'Ground Floor', 'capacity': 250, 'room_type': 'auditorium', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Seminar Hall', 'building': 'Admin Block', 'floor': '1st Floor', 'capacity': 100, 'room_type': 'auditorium', 'has_projector': True, 'has_whiteboard': True},
            {'name': 'Conference Room', 'building': 'Admin Block', 'floor': '2nd Floor', 'capacity': 20, 'room_type': 'meeting_room', 'has_projector': True, 'has_whiteboard': True},
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
        """Create program records for Easy2Learning"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Programs...'))
        
        programs_data = [
            {'name': 'JELET', 'code': 'JELET', 'program_type': 'jelet', 'duration_years': 3, 'description': 'Joint Entrance Lateral Entry Test - Lateral entry to B.Tech'},
            {'name': 'WBJEE', 'code': 'WBJEE', 'program_type': 'wbjee', 'duration_years': 4, 'description': 'West Bengal Joint Entrance Examination - B.Tech admission'},
            {'name': 'Diploma in Engineering', 'code': 'DIPLOMA', 'program_type': 'diploma', 'duration_years': 3, 'description': '3-year Diploma Engineering program'},
            {'name': 'B.Tech', 'code': 'BTECH', 'program_type': 'btech', 'duration_years': 4, 'description': 'Bachelor of Technology - 4-year undergraduate program'},
            {'name': 'M.Tech', 'code': 'MTECH', 'program_type': 'mtech', 'duration_years': 2, 'description': 'Master of Technology - 2-year postgraduate program'},
            {'name': 'Other Programs', 'code': 'OTHER', 'program_type': 'others', 'duration_years': 1, 'description': 'Short-term courses and certification programs'},
        ]
        
        for prog_data in programs_data:
            prog, created = Program.objects.get_or_create(
                code=prog_data['code'],
                defaults=prog_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {prog.name} ({prog.get_program_type_display()})'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Already exists: {prog.name}'))

    def create_subjects(self):
        """Create subjects for each program"""
        self.stdout.write(self.style.HTTP_INFO('\nCreating Subjects for all Programs...'))
        
        # Subject templates organized by program code and semester
        subject_templates = {
            'BTECH': {
                1: [
                    {'code': 'BS101', 'name': 'Mathematics-I', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'BS102', 'name': 'Physics-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'BS103', 'name': 'Chemistry-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'ES101', 'name': 'Basic Electrical Engineering', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'ES102', 'name': 'Programming in C', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'HU101', 'name': 'English Communication', 'subject_type': 'theory', 'credits': 2, 'total_hours': 25},
                ],
                2: [
                    {'code': 'BS201', 'name': 'Mathematics-II', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'BS202', 'name': 'Physics-II', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'BS203', 'name': 'Chemistry-II', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'ES201', 'name': 'Basic Electronics', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'ES202', 'name': 'Data Structures', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'HU201', 'name': 'Professional Ethics', 'subject_type': 'theory', 'credits': 2, 'total_hours': 25},
                ],
                3: [
                    {'code': 'CS301', 'name': 'Object Oriented Programming', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS302', 'name': 'Database Management Systems', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS303', 'name': 'Operating Systems', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS304', 'name': 'Computer Networks', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'BS301', 'name': 'Numerical Methods', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                ],
                4: [
                    {'code': 'CS401', 'name': 'Algorithms', 'subject_type': 'theory', 'credits': 4, 'total_hours': 45},
                    {'code': 'CS402', 'name': 'Software Engineering', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS403', 'name': 'Web Technologies', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS404', 'name': 'Machine Learning', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS405', 'name': 'Compiler Design', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                ],
                5: [
                    {'code': 'CS501', 'name': 'Artificial Intelligence', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS502', 'name': 'Cloud Computing', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS503', 'name': 'Cyber Security', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS504', 'name': 'Internet of Things', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS505', 'name': 'Big Data Analytics', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                6: [
                    {'code': 'CS601', 'name': 'Distributed Systems', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS602', 'name': 'Mobile Computing', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS603', 'name': 'DevOps', 'subject_type': 'both', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS604', 'name': 'Blockchain Technology', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'CS605', 'name': 'Project Management', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                ],
                7: [
                    {'code': 'CS701', 'name': 'Deep Learning', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS702', 'name': 'Natural Language Processing', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS703', 'name': 'Computer Vision', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'CS704', 'name': 'Industry 4.0', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                ],
                8: [
                    {'code': 'CS801', 'name': 'Major Project', 'subject_type': 'practical', 'credits': 8, 'total_hours': 100},
                    {'code': 'CS802', 'name': 'Internship/Industrial Training', 'subject_type': 'practical', 'credits': 4, 'total_hours': 50},
                ],
            },
            'JELET': {
                1: [
                    {'code': 'JL101', 'name': 'Mathematics-I', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'JL102', 'name': 'Physics-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'JL103', 'name': 'Chemistry-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'JL104', 'name': 'Electrical Technology', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'JL105', 'name': 'Programming Fundamentals', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                2: [
                    {'code': 'JL201', 'name': 'Mathematics-II', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'JL202', 'name': 'Electronics-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'JL203', 'name': 'Mechanical Engineering', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'JL204', 'name': 'Data Structures', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'JL205', 'name': 'Digital Electronics', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                3: [
                    {'code': 'JL301', 'name': 'Microprocessors', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'JL302', 'name': 'Computer Architecture', 'subject_type': 'theory', 'credits': 3, 'total_hours': 40},
                    {'code': 'JL303', 'name': 'Web Development', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'JL304', 'name': 'Database Systems', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
            },
            'WBJEE': {
                1: [
                    {'code': 'WB101', 'name': 'Mathematics-I', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'WB102', 'name': 'Physics-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'WB103', 'name': 'Chemistry-I', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'WB104', 'name': 'Basic Engineering', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'WB105', 'name': 'Computer Programming', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                2: [
                    {'code': 'WB201', 'name': 'Mathematics-II', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'WB202', 'name': 'Physics-II', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'WB203', 'name': 'Chemistry-II', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'WB204', 'name': 'Electrical Circuits', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'WB205', 'name': 'Engineering Drawing', 'subject_type': 'practical', 'credits': 3, 'total_hours': 45},
                ],
            },
            'DIPLOMA': {
                1: [
                    {'code': 'DP101', 'name': 'Applied Mathematics', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'DP102', 'name': 'Applied Physics', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'DP103', 'name': 'Applied Chemistry', 'subject_type': 'both', 'credits': 4, 'total_hours': 45},
                    {'code': 'DP104', 'name': 'Workshop Practice', 'subject_type': 'practical', 'credits': 3, 'total_hours': 50},
                    {'code': 'DP105', 'name': 'Basic Engineering', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                ],
                2: [
                    {'code': 'DP201', 'name': 'Engineering Mechanics', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'DP202', 'name': 'Electrical Technology', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'DP203', 'name': 'Electronic Devices', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                    {'code': 'DP204', 'name': 'Computer Fundamentals', 'subject_type': 'both', 'credits': 3, 'total_hours': 40},
                ],
                3: [
                    {'code': 'DP301', 'name': 'Industrial Management', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'DP302', 'name': 'Project Work', 'subject_type': 'practical', 'credits': 8, 'total_hours': 100},
                    {'code': 'DP303', 'name': 'Industrial Training', 'subject_type': 'practical', 'credits': 4, 'total_hours': 60},
                ],
            },
            'MTECH': {
                1: [
                    {'code': 'MT101', 'name': 'Advanced Mathematics', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                    {'code': 'MT102', 'name': 'Research Methodology', 'subject_type': 'theory', 'credits': 3, 'total_hours': 35},
                    {'code': 'MT103', 'name': 'Advanced Algorithms', 'subject_type': 'theory', 'credits': 4, 'total_hours': 45},
                    {'code': 'MT104', 'name': 'Machine Learning Advanced', 'subject_type': 'both', 'credits': 4, 'total_hours': 50},
                ],
                2: [
                    {'code': 'MT201', 'name': 'Thesis/Dissertation', 'subject_type': 'practical', 'credits': 12, 'total_hours': 150},
                    {'code': 'MT202', 'name': 'Seminar', 'subject_type': 'theory', 'credits': 4, 'total_hours': 40},
                ],
            },
            'OTHER': {
                1: [
                    {'code': 'OT101', 'name': 'Python Programming', 'subject_type': 'both', 'credits': 3, 'total_hours': 40},
                    {'code': 'OT102', 'name': 'Data Science Basics', 'subject_type': 'both', 'credits': 3, 'total_hours': 40},
                    {'code': 'OT103', 'name': 'Web Development Basics', 'subject_type': 'both', 'credits': 3, 'total_hours': 40},
                    {'code': 'OT104', 'name': 'Digital Marketing', 'subject_type': 'theory', 'credits': 2, 'total_hours': 30},
                    {'code': 'OT105', 'name': 'Excel for Professionals', 'subject_type': 'both', 'credits': 2, 'total_hours': 30},
                ],
            },
        }
        
        programs = list(Program.objects.all())
        created_count = 0
        
        for program in programs:
            program_key = program.code if program.code in subject_templates else 'BTECH'
            templates = subject_templates.get(program_key, subject_templates['BTECH'])
            
            for semester, subjects in templates.items():
                for subj_data in subjects:
                    subject, created = Subject.objects.get_or_create(
                        code=subj_data['code'],
                        program=program,
                        defaults={
                            'name': subj_data['name'],
                            'subject_type': subj_data['subject_type'],
                            'semester': semester,
                            'credits': subj_data['credits'],
                            'total_hours': subj_data['total_hours'],
                            'is_active': True
                        }
                    )
                    if created:
                        created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} subjects across all programs'))

    def create_teachers(self, count):
        """Create teacher records"""
        self.stdout.write(self.style.HTTP_INFO(f'\nCreating {count} Teachers...'))
        
        first_names = [
            'John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Amanda',
            'James', 'Ashley', 'Daniel', 'Michelle', 'Christopher', 'Stephanie', 'Matthew',
            'Nicole', 'Andrew', 'Elizabeth', 'Joshua', 'Heather', 'Ryan', 'Samantha',
            'Brandon', 'Kimberly', 'Justin', 'Lisa', 'Tyler', 'Angela', 'Zachary', 'Melissa',
            'Arijit', 'Priya', 'Rahul', 'Swati', 'Debashis', 'Moumita', 'Sanjay', 'Ananya',
            'Subrata', 'Riya', 'Bikram', 'Trisha', 'Kartik', 'Oindrila', 'Souvik', 'Payel'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
            'Das', 'Gupta', 'Sharma', 'Patel', 'Singh', 'Banerjee', 'Ghosh', 'Mukherjee',
            'Halder', 'Sinha', 'Bhaduri', 'Chatterjee', 'Mitra', 'Bose', 'Dutta', 'Nath'
        ]
        
        subjects_taught = [
            'Computer Science', 'Data Structures', 'Algorithms', 'Database Management',
            'Web Development', 'Machine Learning', 'Calculus', 'Linear Algebra',
            'Differential Equations', 'Statistics', 'Physics', 'Chemistry', 'Biology',
            'English Literature', 'Creative Writing', 'World History', 'Economics',
            'Business Management', 'Digital Marketing', 'Network Security',
            'Microprocessors', 'Digital Electronics', 'Electrical Circuits', 'Java Programming',
            'Python Programming', 'C Programming', 'Operating Systems', 'Compiler Design',
            'Artificial Intelligence', 'Cloud Computing', 'Cyber Security'
        ]
        
        qualifications = [
            'B.Sc Computer Science', 'M.Sc Computer Science', 'Ph.D. Computer Science',
            'B.Sc Mathematics', 'M.Sc Mathematics', 'Ph.D. Mathematics',
            'B.Sc Physics', 'M.Sc Physics', 'Ph.D. Physics',
            'M.A. English Literature', 'M.A. History',
            'MBA', 'B.Sc Chemistry', 'M.Sc Chemistry',
            'B.Tech Computer Science', 'M.Tech Computer Science',
            'B.Tech Electrical', 'M.Tech Electrical',
            'B.Tech Electronics', 'M.Tech Electronics'
        ]
        
        departments = list(Department.objects.all())
        random.seed(42)
        
        created_count = 0
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            employee_id = f'FAC{str(i + 1).zfill(4)}'
            
            if Teacher.objects.filter(employee_id=employee_id).exists():
                continue
            
            teacher = Teacher(
                first_name=first_name,
                last_name=last_name,
                email=f'{first_name.lower()}.{last_name.lower()}{i}@easy2learning.com',
                phone=f'+91 98765{str(random.randint(10000, 99999))}',
                address=f'{random.randint(1, 100)} Academic Way, Kolkata-7000{random.randint(1, 99)}',
                date_of_birth=datetime(1970, 1, 1) + timedelta(days=random.randint(1, 365 * 20)),
                gender=random.choice(['male', 'female', 'other', 'prefer_not_to_say']),
                photo=None,
                employee_id=employee_id,
                department=random.choice(departments) if departments else None,
                qualification=random.choice(qualifications),
                specialization=random.choice(subjects_taught),
                experience_years=random.randint(1, 25),
                hourly_rate=random.randint(500, 3000) + random.randint(0, 99) / 100,
                status=random.choice(['active', 'active', 'active', 'active', 'on_leave', 'inactive']),
                emergency_contact_name=f'{random.choice(first_names)} {random.choice(last_names)}',
                emergency_contact_phone=f'+91 98765{str(random.randint(10000, 99999))}',
                hire_date=datetime(2010, 1, 1) + timedelta(days=random.randint(1, 365 * 10))
            )
            teacher.save()
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} teachers'))

    def assign_teachers_to_subjects(self):
        """Assign teachers to subjects (many-to-many relationship)"""
        self.stdout.write(self.style.HTTP_INFO('\nAssigning Teachers to Subjects...'))
        
        teachers = list(Teacher.objects.filter(status='active'))
        subjects = list(Subject.objects.all())
        
        if not teachers:
            self.stdout.write(self.style.ERROR('  ✗ No teachers found.'))
            return
        
        if not subjects:
            self.stdout.write(self.style.ERROR('  ✗ No subjects found.'))
            return
        
        random.seed(42)
        total_assignments = 0
        
        for subject in subjects:
            # Assign 1-3 teachers to each subject
            num_teachers = random.randint(1, min(3, len(teachers)))
            selected_teachers = random.sample(teachers, num_teachers)
            
            for teacher in selected_teachers:
                if not subject.teachers.filter(pk=teacher.pk).exists():
                    subject.teachers.add(teacher)
                    total_assignments += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {total_assignments} teacher-subject assignments'))

    def create_sessions(self, count):
        """Create session/class records"""
        self.stdout.write(self.style.HTTP_INFO(f'\nCreating {count} Sessions...'))
        
        teachers = list(Teacher.objects.filter(status='active'))
        subjects = list(Subject.objects.filter(is_active=True))
        rooms = list(ClassRoom.objects.all())
        
        if not teachers:
            self.stdout.write(self.style.ERROR('  ✗ No teachers found. Please create teachers first.'))
            return
        
        if not subjects:
            self.stdout.write(self.style.ERROR('  ✗ No subjects found. Please create subjects first.'))
            return
        
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        time_slots = [
            ('08:00', '09:00', 1.0),
            ('09:00', '10:00', 1.0),
            ('10:00', '11:00', 1.0),
            ('11:00', '12:00', 1.0),
            ('12:00', '13:00', 1.0),
            ('14:00', '15:00', 1.0),
            ('15:00', '16:00', 1.0),
            ('16:00', '17:00', 1.0),
            ('17:00', '18:00', 1.0),
            ('09:00', '11:00', 2.0),  # Double period
            ('14:00', '16:00', 2.0),  # Double period
        ]
        
        today = timezone.now().date()
        
        random.seed(42)
        created_count = 0
        
        for i in range(count):
            teacher = random.choice(teachers)
            subject = random.choice(subjects)
            day = random.choice(days_of_week)
            start_time_str, end_time_str, duration = random.choice(time_slots)
            
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            # Find a date that matches the day of week
            days_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
            target_day = days_map[day]
            
            current_weekday = today.weekday()
            days_ahead = target_day - current_weekday
            if days_ahead <= 0:
                days_ahead += 7
            
            session_date = today + timedelta(days=days_ahead + random.randint(0, 20))
            
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
                status=random.choice(['scheduled', 'scheduled', 'scheduled', 'completed']),
                notes=f'Class for {subject.name} ({subject.program.name})',
                is_recurring=random.choice([True, False])
            )
            session.save()
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {created_count} sessions'))
