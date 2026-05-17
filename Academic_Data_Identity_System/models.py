from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Staff(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    profile_photo = models.ImageField(upload_to='profiles/', null=True)
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Research(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100)  # ongoing, completed

class Accreditation(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    agency = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    date = models.DateField()


class DataRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_text = models.TextField()
    status = models.CharField(max_length=50, default="pending")
    
class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField()
    remarks = models.TextField()


class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField(null=True)

    def __str__(self):
        return self.name



class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}: {self.grade}"
    

class Department(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    contact = models.EmailField()
    courses = models.TextField(help_text="Separate courses with commas")

    def __str__(self):
        return self.name

    def get_courses(self):
        return self.courses.split(",")

class Certificate(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='certificates/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class StudentCourses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}"
    

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


# ---------------- MCQ QUESTION ----------------
class MCQQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ]
    )

    def __str__(self):
        return self.question


# ---------------- ESSAY QUESTION ----------------
class EssayQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField()
    marks = models.IntegerField(default=10)

    def __str__(self):
        return self.question


# ---------------- STUDENT ANSWERS ----------------
class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # NEW


class MCQAnswer(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)


class EssayAnswer(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    marks_awarded = models.FloatField(default=0)

class StudentExamAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.student.full_name} - {self.exam.title}"
    
class StudentModuleGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.student.full_name} - {self.module.name} - {self.grade}"




    
