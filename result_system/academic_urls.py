
from django.urls import include, path

from result_module import AcademicViews, StaffImports

urlpatterns = [
 # staff url paths  
   
    path('get_class_student_attendance_data', AcademicViews.get_class_student_attendance_data, name='academic_get_class_student_attendance_data'),  
    path('staff_view_class_attendance', AcademicViews.staff_view_class_attendance, name='academic_view_class_attendance'),  
    path('staff_home', AcademicViews.academic_home, name='academic_home'),  
    path('staff_take_class_attendance', AcademicViews.staff_take_class_attendance, name='academic_take_class_attendance'),  
    path('staff_take_attendance', AcademicViews.staff_take_attendance, name='academic_take_attendance'),  
    path('staff_fetch_students', AcademicViews.staff_fetch_students, name='academic_fetch_students'),  
    path('get_students', AcademicViews.get_students, name='academic_get_students'),  
    path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', AcademicViews.download_student_results_excel, name='academic_download_student_results_excel'),
    path('staff_update_class_attendance', AcademicViews.staff_update_class_attendance, name='academic_update_class_attendance'),  
    path('staff_save_class_attendance_data', AcademicViews.staff_save_class_attendance_data, name='academic_save_class_attendance_data'),  
   
    path('staff_get_class_attendance_date', AcademicViews.staff_get_class_attendance_date, name='academic_get_class_attendance_date'),  
 
    path('get_class_student_attendance', AcademicViews.get_class_student_attendance, name='academic_get_class_student_attendance'),  
    
 
    path('update_profile_picture/', AcademicViews.update_profile_picture, name='academic_update_profile_picture'),  
    path('save_class_updateattendance', AcademicViews.save_class_updateattendance, name='academic_save_class_updateattendance'),  
   
    path('staff_apply_leave', AcademicViews.staff_apply_leave, name='academic_apply_leave'),  
    path('staff_apply_leave_save', AcademicViews.staff_apply_leave_save, name='academic_apply_leave_save'),  
    path('staff_sendfeedback', AcademicViews.staff_sendfeedback, name='academic_sendfeedback'),  
    path('staff_sendfeedback_save', AcademicViews.staff_sendfeedback_save, name='academic_sendfeedback_save'),  
    path('staff_detail', AcademicViews.staff_detail, name='academic_detail'),  
    path('manage_student', AcademicViews.manage_student, name='academic_manage_student'),  
    path('student_general_attendance/<int:student_id>/', AcademicViews.student_general_attendance, name='academic_student_general_attendance'),
  
    
    path('import_subject_wise_result/<int:exam_type_id>/', StaffImports.import_subject_wise_result, name='academic_import_subject_wise_result'),
    

    path('result/<int:exam_type_id>/<int:class_level_id>/', AcademicViews.ResultCreateUpdateView.as_view(), name='academic_add_result'),
    path('result/<int:exam_type_id>/<int:class_level_id>/<int:pk>/', AcademicViews.ResultCreateUpdateView.as_view(), name='academic_edit_result'),
    path('student-result/add/<int:student_id>/<int:exam_type_id>/<int:class_level_id>/', AcademicViews.StudentResultCreateUpdateView.as_view(), name='academic_student_result_create_update'),
    
    path('save_marks_view/', AcademicViews.save_marks_view, name='academic_save_marks_endpoint'),
    path('delete_result_endpoint/', AcademicViews.delete_result_endpoint, name='academic_delete_result_endpoint'),
    path('student-results/', AcademicViews.student_results_view, name='academic_student_results'),
    path('exam-types/', AcademicViews.exam_type_list, name='academic_exam_type_list'),
    path('exam_type_to_view_class/<int:exam_type_id>/', AcademicViews.exam_type_to_view_class, name='academic_exam_type_to_view_class'),
    path('view_student_to_add_result/<int:exam_type_id>/<int:class_level_id>/', AcademicViews.view_student_to_add_result, name='academic_view_student_to_add_result'),
    path('manage_result/', AcademicViews.manage_result, name='academic_manage_result'),    
    path('students_wise_result_page/', AcademicViews.students_wise_result_page, name='academic_students_wise_result_page'),
    path('student_subject_wise_result/', AcademicViews.student_subject_wise_result, name='academic_student_subject_wise_result'),
    path('student_subject_wise_result_page/<int:student_id>/', AcademicViews.student_subject_wise_result_page, name='academic_student_subject_wise_result_page'),

 
]