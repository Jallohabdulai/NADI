from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Grade
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Department, Certificate, Module, StudentCourses
from .models import Exam, MCQQuestion, EssayQuestion, StudentModuleGrade, StudentExam, MCQAnswer, EssayAnswer, StudentExamAssignment
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, Institution, Research, Accreditation, DataRequest, AcademicRecord, Staff
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth.models import Group
import json



@login_required
def manage_institutions(request):
    if not request.user.is_staff:
        return redirect("dashboard")

    institutions = Institution.objects.all()

    if request.method == "POST":
        Institution.objects.create(
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
        )
        return redirect("manage_institutions")

    return render(request, "manage_institutions.html", {
        "institutions": institutions
    })

@login_required
def manage_staff(request):
    if not request.user.is_staff:
        return redirect("dashboard")

    staff = Staff.objects.all()

    if request.method == "POST":
        Staff.objects.create(
            institution_id=request.POST.get("institution"),
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            role=request.POST.get("role")
        )
        return redirect("manage_staff")

    return render(request, "manage_staff.html", {
        "staff": staff,
        "institutions": Institution.objects.all()
    })

@login_required
def edit_staff(request, id):
    staff = get_object_or_404(Staff, id=id)

    if request.method == "POST":
        staff.full_name = request.POST.get("full_name")
        staff.email = request.POST.get("email")
        staff.role = request.POST.get("role")
        staff.save()
        return redirect("manage_staff")

    return render(request, "edit_staff.html", {"staff": staff})

@login_required
def delete_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    staff.delete()
    return redirect("manage_staff")

@login_required
def academic_records(request):
    records = AcademicRecord.objects.select_related("student").all()

    return render(request, "academic_records.html", {
        "records": records
    })

def research_view(request):
    research = Research.objects.all()

    if request.method == "POST":
        Research.objects.create(
            institution_id=request.POST.get("institution"),
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            status=request.POST.get("status")
        )
        return redirect("research")

    return render(request, "research.html", {
        "research": research,
        "institutions": Institution.objects.all()
    })

def accreditation(request):
    data = Accreditation.objects.all()

    if request.method == "POST":
        Accreditation.objects.create(
            institution_id=request.POST.get("institution"),
            agency=request.POST.get("agency"),
            status=request.POST.get("status"),
            date=request.POST.get("date")
        )
        return redirect("accreditation")

    return render(request, "accreditation.html", {
        "data": data,
        "institutions": Institution.objects.all()
    })

@login_required
def analytics(request):
    students_by_level = Student.objects.values('level').annotate(total=Count('id'))
    courses = Course.objects.count()
    staff = Staff.objects.count()

    return render(request, "analytics.html", {
        "students_by_level": students_by_level,
        "courses": courses,
        "staff": staff
    })

def data_requests(request):
    requests = DataRequest.objects.all()

    if request.method == "POST":
        DataRequest.objects.create(
            user=request.user,
            request_text=request.POST.get("request_text")
        )
        return redirect("data_requests")

    return render(request, "data_requests.html", {
        "requests": requests
    })
from django.contrib.auth.models import User

@login_required
def assign_role_view(request, user_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.all()

    if request.method == "POST":
        role_name = request.POST.get("role")
        group, created = Group.objects.get_or_create(name=role_name)

        user.groups.clear()  # optional: remove old roles
        user.groups.add(group)

        return redirect("assign_role", user_id=user.id)

    return render(request, "assign_role.html", {
        "user_obj": user,
        "groups": groups
    })

def assign_role(user, role_name):
    group, created = Group.objects.get_or_create(name=role_name)
    user.groups.add(group)

def registration(request):
    if request.method == "POST":

        full_name = request.POST.get("fullname")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        level = request.POST.get("level")
        department = request.POST.get("department")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        password = request.POST.get("password")

        # CORRECTED
        photo = request.FILES.get("profile_photo")

        if User.objects.filter(username=student_id).exists():
            return render(request, "registration.html", {"error": "Student ID already registered."})

        # Create Django user
        user = User.objects.create_user(
            username=student_id,
            email=email,
            password=password
        )

        # Create student profile
        Student.objects.create(
            user=user,
            full_name=full_name,
            student_id=student_id,
            email=email,
            department=department,
            level=level,
            dob=dob,
            gender=gender,

            # CORRECTED
            profile_photo=photo  
        )

        return redirect("login_user")

    return render(request, "registration.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect("admin_dashboard")

            return redirect("dashboard")

        return render(request, "login_user.html", {"error": "Invalid Student ID or Password"})

    return render(request, "login_user.html")


@login_required
def dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    student_courses = StudentCourses.objects.filter(
        student=student
    ).select_related("course")

    assigned_exams = StudentExamAssignment.objects.filter(
        student=student
    ).select_related("exam", "exam__module")

    completed_exams = StudentExam.objects.filter(
        student=student,
        completed=True
    )

    # ✅ ADD THIS LINE (THIS IS WHAT YOU MISSED)
    grades = StudentModuleGrade.objects.filter(student=student)

    return render(request, "dashboard.html", {
        "student": student,
        "student_courses": student_courses,
        "assigned_exams": assigned_exams,
        "completed_exams": completed_exams,
        "grades": grades   # 🔥 REQUIRED
    })

@login_required
def department(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {
        "departments": departments
    })



def corse(request):
    student = Student.objects.get(user=request.user)

    grades = {
        "Math": "A",
        "English": "B",
        "Physics": "A",
        "Biology": "C",
    }

    return render(request, "corse.html", {
        "student": student,
        "grades": grades
    })


@login_required
def certificate(request):
    try:
        student = Student.objects.get(user=request.user)
        certificates = Certificate.objects.filter(student=student)
    except Student.DoesNotExist:
        student = None
        certificates = []

    return render(request, "certificate.html", {
        "certificates": certificates
    })


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    total_certificates = Certificate.objects.count()

    try:
        total_courses = Course.objects.count()
    except:
        total_courses = 0

    # ✅ MONTHLY STUDENT REGISTRATION DATA (BAR CHART)
    monthly_data = (
        Student.objects
        .annotate(month=TruncMonth('user__date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    counts = []

    for item in monthly_data:
        months.append(item['month'].strftime("%b"))
        counts.append(item['count'])

    # fallback if empty
    if not months:
        months = ["Jan","Feb","Mar","Apr","May","Jun"]
        counts = [0,0,0,0,0,0]

    # ✅ LEVEL DISTRIBUTION (PIE CHART)
    levels = Student.objects.values('level').annotate(count=Count('id'))

    level_labels = [l['level'] for l in levels]
    level_counts = [l['count'] for l in levels]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'total_certificates': total_certificates,

        # charts
        'months': json.dumps(months),
        'counts': json.dumps(counts),
        'level_labels': json.dumps(level_labels),
        'level_counts': json.dumps(level_counts),
    }

    return render(request, 'admin_dashboard.html', context)

# ----------------- ADMIN: Manage Certificates -----------------

def manage_certificates(request):
    students = Student.objects.all()
    certificates = Certificate.objects.all()

    if request.method == "POST":
        title = request.POST['title']
        student_id = request.POST['student_id']
        file = request.FILES.get('file')

        student = Student.objects.get(id=student_id)

        Certificate.objects.create(
            title=title,
            student=student,
            file=file
        )

        messages.success(request, "Certificate uploaded successfully!")
        return redirect('manage_certificates')

    return render(request, "manage_certificates.html", {
        "students": students,
        "certificates": certificates
    })


# ----------------- ADMIN: Edit Certificate -----------------

def edit_certificate(request, cert_id):
    cert = get_object_or_404(Certificate, id=cert_id)
    students = Student.objects.all()

    if request.method == "POST":
        cert.title = request.POST['title']
        student_id = request.POST['student_id']
        cert.student = Student.objects.get(id=student_id)

        if request.FILES.get("file"):
            cert.file = request.FILES["file"]

        cert.save()
        messages.success(request, "Certificate updated!")
        return redirect('manage_certificates')

    return render(request, "edit_certificate.html", {
        "cert": cert,
        "students": students
    })


# ----------------- ADMIN: Delete Certificate -----------------

def delete_certificate(request, cert_id):
    cert = get_object_or_404(Certificate, id=cert_id)
    cert.delete()
    messages.success(request, "Certificate deleted!")
    return redirect('manage_certificates')


# ----------------- STUDENT VIEW -----------------

def certificates(request):
    student = request.user.student
    certificates = Certificate.objects.filter(student=student)

    return render(request, "certificate.html", {
        "certificates": certificates
    })

def manage_courses(request):
    courses = Course.objects.all()
    students = Student.objects.all()

    if request.method == "POST":

        # CREATE COURSE
        if "create_course" in request.POST:
            Course.objects.create(
                name=request.POST.get("name"),
                code=request.POST.get("code"),
                credits=request.POST.get("credits")
            )

        # CREATE MODULE
        elif "create_module" in request.POST:
            course = get_object_or_404(Course, id=request.POST.get("course_id"))

            Module.objects.create(
                course=course,
                name=request.POST.get("module_name"),
                code=request.POST.get("module_code")
            )

        # ASSIGN COURSE TO STUDENT
        elif "assign_course" in request.POST:
            student = get_object_or_404(Student, id=request.POST.get("student_id"))
            course = get_object_or_404(Course, id=request.POST.get("course_id"))

            StudentCourses.objects.get_or_create(
                student=student,
                course=course
            )

        return redirect("manage_courses")

    return render(request, "manage_courses.html", {
        "courses": courses,
        "students": students
    })

@login_required
def manage_grades(request):
    if not request.user.is_staff:
        return redirect("dashboard")

    students = Student.objects.all()
    modules = Module.objects.all()
    grades = StudentModuleGrade.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        module_id = request.POST.get("module_id")
        grade_value = request.POST.get("grade")

        student = get_object_or_404(Student, id=student_id)
        module = get_object_or_404(Module, id=module_id)

        StudentModuleGrade.objects.update_or_create(
            student=student,
            module=module,
            defaults={"grade": grade_value}
        )

        return redirect("manage_grades")

    return render(request, "manage_grades.html", {
        "students": students,
        "modules": modules,
        "grades": grades
    })


@login_required
def delete_grade(request, id):
    if not request.user.is_staff:
        return redirect("dashboard")

    grade = get_object_or_404(StudentModuleGrade, id=id)
    grade.delete()
    return redirect("manage_grades")

@login_required
def manage_student(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    students = Student.objects.all()

    return render(request, 'manage_student.html', {
        'students': students
    })




# ADMIN — LIST & CREATE DEPARTMENTS
def manage_departments(request):
    departments = Department.objects.all()

    if request.method == "POST":
        Department.objects.create(
            name=request.POST.get("name"),
            head=request.POST.get("head"),
            contact=request.POST.get("contact"),
            courses=request.POST.get("courses")
        )
        return redirect("manage_departments")

    return render(request, "manage_departments.html", {
        "departments": departments
    })


def edit_department(request, dept_id):
    dept = Department.objects.get(id=dept_id)

    if request.method == "POST":
        dept.name = request.POST['name']
        dept.head = request.POST['head']
        dept.contact = request.POST['contact']
        dept.courses = request.POST['courses']
        dept.save()
        return redirect('manage_departments')

    return render(request, 'edit_department.html', {"dept": dept})


def delete_department(request, dept_id):
    dept = Department.objects.get(id=dept_id)

    if request.method == "POST":
        dept.delete()
        return redirect('manage_departments')

    return render(request, 'delete_department.html', {"dept": dept})

@login_required
def edit_student(request, id):
    if not request.user.is_staff:
        return redirect('dashboard')

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.full_name = request.POST.get("fullname")
        student.email = request.POST.get("email")
        student.level = request.POST.get("level")
        student.department = request.POST.get("department")
        student.save()

        return redirect('manage_student')

    return render(request, 'edit_student.html', {
        'student': student
    })

@login_required
def delete_student(request, id):
    if not request.user.is_staff:
        return redirect('dashboard')

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.user.delete()   # deletes both user & student
        return redirect('manage_student')

    return render(request, 'delete_student.html', {
        'student': student
    })

@login_required
def delete_course(request, id):
    if not request.user.is_staff:
        return redirect("dashboard")

    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect("manage_courses")

@login_required
def edit_course(request, id):
    if not request.user.is_staff:
        return redirect("dashboard")

    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.name = request.POST.get("name")
        course.code = request.POST.get("code")
        course.credits = request.POST.get("credits")
        course.save()
        return redirect("manage_courses")

    return render(request, "edit_course.html", {"course": course})


@login_required
def add_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        credit = request.POST.get("credit")

        Course.objects.create(
            name=name,
            code=code,
            credit=credit
        )
        return redirect('manage_courses')

    return render(request, "add_course.html")

@login_required
def manage_exams(request):
    courses = Course.objects.prefetch_related("modules").all()
    exams = Exam.objects.select_related("course", "module").all()

    if request.method == "POST":
        course_id = request.POST.get("course")
        module_id = request.POST.get("module")
        title = request.POST.get("title")
        duration = request.POST.get("duration")

        course = Course.objects.get(id=course_id)
        module = Module.objects.get(id=module_id)

        Exam.objects.create(
            course=course,
            module=module,
            title=title,
            duration=duration
        )

        return redirect("manage_exams")

    return render(request, "manage_exams.html", {
        "courses": courses,
        "exams": exams
    })

@login_required
def add_mcq(request, exam_id):
    exam = Exam.objects.get(id=exam_id)

    if request.method == "POST":
        MCQQuestion.objects.create(
            exam=exam,
            question=request.POST.get("question"),
            option_a=request.POST.get("a"),
            option_b=request.POST.get("b"),
            option_c=request.POST.get("c"),
            option_d=request.POST.get("d"),
            correct_answer=request.POST.get("correct")
        )

        return redirect("manage_exams")

    return render(request, "add_mcq.html", {"exam": exam})

@login_required
def add_essay(request, exam_id):
    exam = Exam.objects.get(id=exam_id)

    if request.method == "POST":
        EssayQuestion.objects.create(
            exam=exam,
            question=request.POST.get("question"),
            marks=request.POST.get("marks")
        )

        return redirect("manage_exams")

    return render(request, "add_essay.html", {"exam": exam})


@login_required
def student_exams(request):
    student = Student.objects.get(user=request.user)
    exams = Exam.objects.all()

    return render(request, "student_exams.html", {
        "exams": exams,
        "student": student
    })

@login_required
def take_exam(request, exam_id):
    student = get_object_or_404(Student, user=request.user)
    exam = get_object_or_404(Exam, id=exam_id)

    assignment = get_object_or_404(StudentExamAssignment, student=student, exam=exam)

    # Prevent retake
    if assignment.is_completed:
        return redirect("dashboard")

    # Start timer only once
    if assignment.started_at is None:
        assignment.started_at = timezone.now()
        assignment.save()

    # Timer logic
    end_time = assignment.started_at + timezone.timedelta(minutes=exam.duration)
    remaining_seconds = max(0, int((end_time - timezone.now()).total_seconds()))

    mcqs = MCQQuestion.objects.filter(exam=exam)
    essays = EssayQuestion.objects.filter(exam=exam)

    return render(request, "take_exam.html", {
        "exam": exam,
        "mcqs": mcqs,
        "essays": essays,
        "remaining_seconds": remaining_seconds
    })

def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        Module.objects.create(
            course=course,
            name=request.POST.get("name"),
            code=request.POST.get("code")
        )
        return redirect("manage_courses")

    return render(request, "add_module.html", {"course": course})


@login_required
def assign_course(request, student_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course")
        course = get_object_or_404(Course, id=course_id)

        StudentCourses.objects.get_or_create(
            student=student,
            course=course
        )

        return redirect("manage_student")

    return render(request, "assign_course.html", {
        "student": student,
        "courses": courses
    })

@login_required
def assign_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = get_object_or_404(Student, id=student_id)

        StudentExamAssignment.objects.get_or_create(
            student=student,
            exam=exam
        )

        return redirect("manage_exams")

    return render(request, "assign_exam.html", {
        "exam": exam,
        "students": students
    })



@login_required
def submit_exam(request, exam_id):

    if request.method != "POST":
        return redirect("dashboard")

    student = get_object_or_404(Student, user=request.user)
    exam = get_object_or_404(Exam, id=exam_id)

    assignment = get_object_or_404(StudentExamAssignment, student=student, exam=exam)

    if assignment.is_completed:
        return redirect("dashboard")

    student_exam = StudentExam.objects.create(student=student, exam=exam)

    score = 0

    # MCQ auto marking
    for q in MCQQuestion.objects.filter(exam=exam):
        selected = request.POST.get(f"mcq_{q.id}", "")

        MCQAnswer.objects.create(
            student_exam=student_exam,
            question=q,
            selected_answer=selected
        )

        if selected == q.correct_answer:
            score += 1

    # Essay saving
    for q in EssayQuestion.objects.filter(exam=exam):
        EssayAnswer.objects.create(
            student_exam=student_exam,
            question=q,
            answer_text=request.POST.get(f"essay_{q.id}", ""),
            marks_awarded=0
        )

    student_exam.score = score
    student_exam.completed = True
    student_exam.save()

    assignment.is_completed = True
    assignment.save()

    return redirect("dashboard")

@login_required
def grade_essays(request, exam_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    exam = get_object_or_404(Exam, id=exam_id)

    # Get all student exam submissions for this exam
    student_exams = StudentExam.objects.filter(exam=exam)

    if request.method == "POST":
        # Loop through all essay answers and update marks
        for ans in EssayAnswer.objects.filter(student_exam__exam=exam):
            marks = request.POST.get(f"marks_{ans.id}")
            if marks:
                ans.marks_awarded = int(marks)
                ans.save()

        # 🔥 UPDATE TOTAL SCORE (MCQ + ESSAY)
        for se in student_exams:
            total = se.score  # existing MCQ marks

            for ans in se.essayanswer_set.all():
                total += ans.marks_awarded

            se.score = total
            se.save()

        return redirect("grade_essays", exam_id=exam.id)

    return render(request, "grade_essays.html", {
        "exam": exam,
        "student_exams": student_exams
    })