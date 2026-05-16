from django.contrib import admin

# Register your models here.
from .models import Student, AdminUser, Course, Grade, Department, Certificate, Module, StudentCourses, Exam, MCQQuestion, EssayQuestion, StudentExam, MCQAnswer, EssayAnswer, StudentExamAssignment, StudentModuleGrade, Institution
from .models import Institution, Research, Accreditation, DataRequest, AcademicRecord, Staff
admin.site.register (Student)
admin.site.register (AdminUser)
admin.site.register (Course)
admin.site.register (Grade)
admin.site.register (Department)
admin.site.register (Certificate)
admin.site.register (Module)
admin.site.register (StudentCourses)
admin.site.register (Exam)
admin.site.register (MCQQuestion)
admin.site.register (EssayQuestion)
admin.site.register (StudentExam)
admin.site.register (MCQAnswer)
admin.site.register (EssayAnswer)
admin.site.register (StudentExamAssignment)
admin.site.register (StudentModuleGrade)
admin.site.register (Institution)
admin.site.register (Research)
admin.site.register (Accreditation)
admin.site.register (DataRequest)
admin.site.register (AcademicRecord)
admin.site.register (Staff)
