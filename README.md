# Faculty Tracker System

A comprehensive Django-based web application for managing academic faculty, schedules, and institutional data efficiently.

## Table of Contents

- [Project Overview](#project-overview)
- [Screenshots](#screenshots)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Project Structure](#project-structure)
- [User Role System](#user-role-system)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Management Commands](#management-commands)
- [Contributing](#contributing)
- [License](#license)
- [GitHub Upload Guide](#github-upload-guide)

---

## Project Overview

The **Faculty Tracker System** is a robust web platform designed to streamline the administrative tasks of educational institutions. Built with **Django 4.x** and **Bootstrap 5**, it provides a centralized interface for managing departments, programs, teachers, classrooms, and faculty schedules. The system features a dynamic dashboard with real-time analytics, conflict detection for scheduling, and comprehensive reporting capabilities including PDF, CSV, and Excel exports.

This application is specifically tailored for educational institutions like the Easy2Learning Institute, providing a complete solution for faculty management, class scheduling, attendance tracking, and performance analytics. The system is designed to be scalable and can be customized to fit the specific needs of various educational organizations.

---

## Key Features

### Academic Management

The Faculty Tracker System provides comprehensive tools for managing the academic structure of your institution. You can create and manage departments to organize faculty members logically, define academic programs such as B.Tech, M.Tech, Diploma, and others, and track classroom resources including capacity, equipment, and availability. The program management feature supports multiple program types with configurable durations and start/end dates, making it suitable for various educational structures.

### Faculty Management

The teacher management module serves as the backbone of the system, allowing administrators to maintain detailed profiles for each faculty member. Each teacher profile includes personal information, professional qualifications, specialization areas, experience details, and emergency contact information. The system supports employee ID generation, email-based authentication, and status tracking to monitor active, inactive, and on-leave faculty members effectively.

### Schedule and Session Management

The scheduling system is designed to prevent conflicts and optimize resource utilization. You can assign teachers to subjects within specific programs, define weekly schedules with day and time slots, and track class durations in hours. The built-in conflict detection algorithm automatically prevents double-booking teachers for overlapping sessions, ensuring smooth operations. The system supports recurring and non-recurring sessions with status tracking (scheduled, in progress, completed, cancelled, rescheduled).

### Analytics and Reporting

The dashboard provides a real-time overview of institutional metrics including total teachers, active subjects, scheduled sessions, and department-wise distribution. Visual charts built with Chart.js display teacher utilization trends, sessions per day of the week, and department statistics. The reporting module allows generating comprehensive PDF reports, exporting teacher details to CSV/Excel formats, and filtering data by date ranges for specific analysis periods.

### Data Export Capabilities

The system includes robust export functionality for administrative purposes. You can export complete faculty reports as PDF documents, generate CSV files containing teacher details with their assigned subjects and schedules, export attendance records for compliance purposes, and create Excel-compatible spreadsheets for further analysis or integration with other systems.

---

## Technology Stack

The Faculty Tracker System is built using modern, reliable technologies that ensure scalability, security, and ease of maintenance. The backend is powered by Python 3.10+ with Django 4.x framework, providing robust security features, database ORM capabilities, and a mature ecosystem of extensions. For development purposes, SQLite is configured as the default database, while PostgreSQL can be configured for production deployments.

The frontend leverages Bootstrap 5 for responsive, mobile-first design, ensuring the application works seamlessly across all devices. HTML5, CSS3, and JavaScript are used for interactive elements and dynamic content. Chart.js provides data visualization capabilities for the analytics dashboard, while xhtml2pdf enables server-side PDF generation for report exports. Crispy forms with Bootstrap 5 template pack ensures clean, consistent form styling throughout the application.

---

## Installation and Setup

### Prerequisites

Before installing the Faculty Tracker System, ensure your development environment meets the following requirements:

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **Git** for version control
- **pip** package manager (comes with Python)
- **Virtual Environment** (recommended for isolation)

### Step-by-Step Installation

**Step 1: Clone or Extract the Project**

If you have the project as a ZIP file, extract it to your desired location:

```bash
cd /path/to/your/projects
unzip Faculty\ Tracker.zip
cd "Faculty Tracker"
```

**Step 2: Create a Virtual Environment**

Creating a virtual environment is essential to isolate project dependencies:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefixed to your command prompt, indicating the virtual environment is active.

**Step 3: Install Dependencies**

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

This will install Django, Pillow for image handling, crispy-forms for form styling, and xhtml2pdf for PDF generation.

**Step 4: Configure the Database**

Run database migrations to create the required tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database file (`db.sqlite3`) with all the necessary tables for teachers, departments, programs, subjects, sessions, classrooms, and attendance records.

**Step 5: Create a Superuser Account**

Create an administrative user to access the Django admin panel and the application:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter a username, email address, and password. This superuser account will have full access to all features of the system.

**Step 6: Load Sample Data (Optional)**

To populate the database with sample data for testing:

```bash
python manage.py create_dummy_data --num-teachers 20 --num-courses 25 --num-sessions 100
```

You can also clear existing data and start fresh:

```bash
python manage.py create_dummy_data --clear
```

**Step 7: Start the Development Server**

Launch the Django development server:

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/` by default.

**Step 8: Access the Application**

Open your web browser and navigate to the following URLs:

- **Main Application:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

Log in with the superuser credentials you created in Step 5 to access the admin panel.

---

## Project Structure

The Faculty Tracker System follows Django's conventional project structure, organized into a main project configuration directory and a faculty application directory. Understanding this structure is essential for navigation, customization, and future extensions.

```
faculty_tracker/
├── "Faculty Tracker"/                  # Main project root directory
│   ├── manage.py                       # Django management script
│   ├── requirements.txt                # Python dependencies
│   ├── db.sqlite3                      # SQLite database file
│   ├── README.md                       # This documentation file
│   ├── run.txt                         # Sample command references
│   │
│   ├── faculty_tracker/                # Main project configuration
│   │   ├── __init__.py                 # Python package marker
│   │   ├── settings.py                 # Django settings configuration
│   │   ├── urls.py                     # Root URL configuration
│   │   └── wsgi.py                     # WSGI application entry point
│   │
│   ├── faculty/                        # Main application app
│   │   ├── __init__.py                 # Python package marker
│   │   ├── admin.py                    # Django admin configuration
│   │   ├── apps.py                     # App configuration
│   │   ├── forms.py                    # Django forms for data input
│   │   ├── models.py                   # Database models
│   │   ├── urls.py                     # App URL routing
│   │   ├── views.py                    # View functions and classes
│   │   │
│   │   ├── migrations/                 # Database migration files
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_department_is_active_department_teachers.py
│   │   │   └── 0003_program_end_date_program_start_date.py
│   │   │
│   │   ├── management/                 # Custom management commands
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── create_dummy_data.py
│   │   │       └── create_teacher_sessions.py
│   │   │
│   │   ├── static/                     # Static assets
│   │   │   └── faculty/
│   │   │       ├── css/
│   │   │       │   └── style.css       # Custom styles
│   │   │       └── js/
│   │   │           └── main.js         # JavaScript functionality
│   │   │
│   │   └── templates/                  # HTML templates
│   │       ├── base.html               # Base template with common layout
│   │       └── faculty/                # App-specific templates
│   │           ├── dashboard.html
│   │           ├── teacher_list.html
│   │           ├── teacher_detail.html
│   │           ├── teacher_form.html
│   │           ├── subject_list.html
│   │           ├── subject_form.html
│   │           ├── schedule.html
│   │           ├── session_form.html
│   │           ├── department_list.html
│   │           ├── department_form.html
│   │           ├── program_list.html
│   │           ├── program_form.html
│   │           ├── reports.html
│   │           ├── report_pdf.html
│   │           └── *_confirm_delete.html
│   │
│   └── static/                         # Collected static files directory
```

---

## User Role System

The Faculty Tracker System is designed to support a multi-role user management system. Currently, the application utilizes Django's built-in authentication system with superuser accounts providing full administrative access. The following role-based access control structure is planned for future implementation to enhance security and provide tailored experiences for different user types.

### Owner (Super Administrator)

The Owner role represents the highest level of access within the system. This role is designed for institutional administrators or owners who need complete control over all aspects of the platform. Owners can manage all users including creating and removing administrator accounts, view and analyze global analytics and reports across all departments, configure system-wide settings and preferences, manage institutional information such as name, contact details, and branding, access financial data and teacher compensation information, and perform system backups and data exports. The Owner can perform any operation available in the system without restrictions.

### Teacher (Faculty Member)

The Teacher role is designed for faculty members who need access to their specific teaching assignments and related information. This role provides a restricted view focused on individual productivity and classroom management. Teachers can view their assigned subjects and corresponding programs, access their weekly teaching schedule, mark and update attendance for their sessions, view their teaching history and total hours taught, and export their personal teaching reports. Teachers cannot access data belonging to other faculty members or make changes to system configuration.

### Note on Current Implementation

As of the current version, the role-based access control system described above has not been fully implemented in the code. The application currently relies on Django's default permission system where any superuser has full access, and regular authenticated users have no specific permissions. To implement the complete role-based system, future development should include extending the User model to add role fields, creating custom permissions for each role type, implementing role-based view restrictions in the views.py file, and building separate dashboards for each role type.

---

## Usage Guide

### Managing Teachers

The teacher management module allows you to maintain a comprehensive database of faculty members. To add a new teacher, navigate to the Teachers section from the main navigation menu and click the "Add Teacher" button. Fill in the required personal information including first name, last name, email, phone, and employee ID. Optionally, you can add department assignment, qualification details, specialization areas, and hourly rate for payroll calculations. Save the form to create the teacher profile. You can later edit or delete teacher records as needed.

### Managing Departments and Programs

Departments help organize teachers into logical groups based on their area of expertise. To create a department, navigate to the Departments section and add a new entry with the department name and description. After creating departments, you can assign teachers to departments through the teacher edit form. Programs represent academic offerings such as B.Tech, M.Tech, or Diploma programs. Each program has a type, duration, and associated subjects. Create programs first, then add subjects that belong to each program.

### Creating Schedules

The scheduling system allows you to assign teachers to subjects within specific time slots. Navigate to the Schedule section and click "Add Session" to create a new class entry. Select the teacher who will conduct the class, choose the subject from the dropdown (subjects are filtered based on teacher assignments), select the day of the week and time slot, specify the duration in hours, and optionally enter the room number. The system automatically checks for scheduling conflicts and will alert you if the teacher has another session at the same time.

### Using the Dashboard

The dashboard provides an at-a-glance view of your institution's status. The statistics cards show total counts for teachers, subjects, programs, and sessions. Today's classes section lists all scheduled sessions for the current day, helping administrators and teachers plan their day effectively. The upcoming sessions section shows the next ten scheduled sessions across all teachers. The charts display teacher distribution by department and sessions per day of the week for capacity planning.

### Generating Reports

To generate reports, navigate to the Reports section. You can filter data by specifying a date range using the start date and end date fields. The teacher utilization chart shows total hours taught by each teacher, useful for workload assessment. Department statistics display teacher count, subject count, and session count for each department. Use the export buttons to download reports in PDF, CSV, or Excel formats for record-keeping or external analysis.

---

## API Endpoints

The Faculty Tracker System provides RESTful URLs for accessing various features. These endpoints can be accessed directly through the web interface or potentially integrated with external systems.

### Main Pages

| URL Pattern | View Name | Description |
|-------------|-----------|-------------|
| `/` | DashboardView | Main dashboard with statistics and charts |
| `/teachers/` | TeacherListView | List all teachers with search and filtering |
| `/teachers/add/` | TeacherCreateView | Add a new teacher |
| `/teachers/<pk>/` | TeacherDetailView | View detailed teacher profile |
| `/teachers/<pk>/edit/` | TeacherUpdateView | Edit teacher information |
| `/teachers/<pk>/delete/` | TeacherDeleteView | Delete a teacher |
| `/teachers/<pk>/export/` | ExportSingleTeacherView | Export teacher profile to CSV |
| `/subjects/` | SubjectListView | List all subjects |
| `/subjects/add/` | SubjectCreateView | Add a new subject |
| `/subjects/<pk>/edit/` | SubjectUpdateView | Edit subject information |
| `/subjects/<pk>/delete/` | SubjectDeleteView | Delete a subject |
| `/schedule/` | SessionListView | View all scheduled sessions |
| `/schedule/add/` | SessionCreateView | Schedule a new session |
| `/schedule/<pk>/edit/` | SessionUpdateView | Modify an existing session |
| `/schedule/<pk>/delete/` | SessionDeleteView | Remove a scheduled session |
| `/departments/` | DepartmentListView | List all departments |
| `/departments/add/` | DepartmentCreateView | Add a new department |
| `/departments/<pk>/edit/` | DepartmentUpdateView | Edit department details |
| `/departments/<pk>/delete/` | DepartmentDeleteView | Delete a department |
| `/programs/` | ProgramListView | List all academic programs |
| `/programs/add/` | ProgramCreateView | Add a new program |
| `/programs/<pk>/edit/` | ProgramUpdateView | Edit program details |
| `/programs/<pk>/delete/` | ProgramDeleteView | Delete a program |
| `/reports/` | ReportsView | View analytics and reports |
| `/reports/export/pdf/` | ExportPDFView | Export full report as PDF |
| `/reports/export/excel/` | ExportExcelView | Export schedule as Excel (CSV) |
| `/reports/export/csv/` | ExportCSVView | Export attendance as CSV |
| `/reports/export/teacher-details/` | ExportTeacherDetailsView | Export all teacher details |

### AJAX Endpoints

| URL Pattern | View Name | Description |
|-------------|-----------|-------------|
| `/check-conflicts/` | check_session_conflicts | Check for scheduling conflicts (AJAX) |
| `/get-teacher-subjects/` | get_teacher_subjects | Get subjects for a teacher (AJAX) |
| `/get-all-teachers/` | get_all_teachers | Get all active teachers (AJAX) |

---

## Management Commands

The Faculty Tracker System includes custom Django management commands for administrative tasks.

### create_dummy_data

This command populates the database with sample data for testing and demonstration purposes:

```bash
# Create default sample data
python manage.py create_dummy_data

# Create specific number of records
python manage.py create_dummy_data --num-teachers 20 --num-courses 25 --num-sessions 100

# Clear existing data and create fresh
python manage.py create_dummy_data --clear

# Combined options
python manage.py create_dummy_data --num-teachers 30 --num-courses 30 --num-sessions 150 --clear
```

### create_teacher_sessions

This command generates random sessions for existing teachers based on their assigned subjects:

```bash
python manage.py create_teacher_sessions
```

---

## Screenshots

The following screenshots demonstrate the key features and interface of the Faculty Tracker System. These images help new users understand the layout and functionality before setting up the application.

### Dashboard View

The dashboard provides a comprehensive overview of institutional metrics, including total counts of teachers, subjects, programs, and sessions. Interactive charts display teacher distribution by department and weekly session trends, enabling administrators to make data-driven decisions about resource allocation.

### Teacher List and Detail Views

The teacher management interface displays faculty members in a clean, searchable table format. Each teacher's detail page shows personal information, professional qualifications, assigned subjects, teaching schedule, and attendance records. Profile pages also include export functionality for generating CSV reports.

### Schedule Management

The schedule view presents all class sessions in an organized format with filtering options by teacher, day of week, subject, and status. The conflict detection system ensures teachers are not double-booked, maintaining scheduling integrity across the institution.

---

## Contributing

Contributions to the Faculty Tracker System are welcome and appreciated. Whether you want to fix bugs, add new features, improve documentation, or suggest enhancements, your contributions help make this project better for everyone.

### How to Contribute

First, fork the repository on GitHub to create your own copy of the project. Clone your forked repository locally and create a new branch for your feature or bug fix using `git checkout -b feature/your-feature-name`. Make your changes to the code, ensuring you follow the existing coding style and conventions. Write tests for any new functionality you add to maintain code quality. Commit your changes with a clear, descriptive commit message. Push your branch to your forked repository and submit a pull request to the main repository. Your pull request will be reviewed by the maintainers, and feedback will be provided.

### Coding Standards

When contributing code, please follow these guidelines: use consistent indentation (4 spaces), write docstrings for all functions and classes, add comments for complex logic, ensure all new features include appropriate tests, and run the existing test suite before submitting.

---

## License

The Faculty Tracker System is open source software licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and sell the software, subject to the conditions that the original copyright notice and permission notice appear in all copies of the software and its documentation.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
