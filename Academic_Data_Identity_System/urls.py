from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('', views.login_user, name='login_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('department/', views.department, name='department'),
    path('corse/', views.corse, name='corse'),
    path('certificate/', views.certificate, name='certificate'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_certificates/', views.manage_certificates, name='manage_certificates'),
    path('manage_grades/', views.manage_grades, name='manage_grades'),
    path('manage_student/', views.manage_student, name='manage_student'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('manage_departments/', views.manage_departments, name='manage_departments'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('edit_course/<int:id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:id>/', views.delete_course, name='delete_course'),
    path('add_course/', views.add_course, name='add_course'),
    path('manage_exams/', views.manage_exams, name='manage_exams'),
    path('add_mcq/<int:exam_id>/', views.add_mcq, name='add_mcq'),
    path('add_essay/<int:exam_id>/', views.add_essay, name='add_essay'),
    path('assign_exam/<int:exam_id>/', views.assign_exam, name='assign_exam'),
    path('student_exams/', views.student_exams, name='student_exams'),
    path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('submit_exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('add_module/<int:course_id>/', views.add_module, name='add_module'),
    path('grade_essays/<int:exam_id>/', views.grade_essays, name='grade_essays'),
    path('delete_grade/<int:id>/', views.delete_grade, name='delete_grade'),
    path('departments/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('manage_certificates/', views.manage_certificates, name="manage_certificates"),
    path('edit_certificate/<int:cert_id>/', views.edit_certificate, name="edit_certificate"),
    path('delete_certificate/<int:cert_id>/', views.delete_certificate, name="delete_certificate"),
    path('staff/', views.manage_staff, name='manage_staff'),
    path('staff/edit/<int:id>/', views.edit_staff, name='edit_staff'),
    path('staff/delete/<int:id>/', views.delete_staff, name='delete_staff'),
    path('institutions/', views.manage_institutions, name='manage_institutions'),
    path('academic-records/', views.academic_records, name='academic_records'),
    path('research/', views.research_view, name='research'),
    path('accreditation/', views.accreditation, name='accreditation'),
    path('analytics/', views.analytics, name='analytics'),
    path('data-requests/', views.data_requests, name='data_requests'),
    path('assign-role/<int:user_id>/', views.assign_role_view, name='assign_role'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)