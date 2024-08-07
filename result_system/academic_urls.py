
from django.urls import include, path

from result_module import AcademicViews, StaffImports

urlpatterns = [
 # staff url paths  
   
    path('get_class_student_attendance_data', AcademicViews.get_class_student_attendance_data, name='staff_get_class_student_attendance_data'),  
    path('staff_view_class_attendance', AcademicViews.staff_view_class_attendance, name='staff_view_class_attendance'),  
    path('staff_home', AcademicViews.staff_home, name='staff_home'),  
    path('staff_take_class_attendance', AcademicViews.staff_take_class_attendance, name='staff_take_class_attendance'),  
    path('staff_take_attendance', AcademicViews.staff_take_attendance, name='staff_take_attendance'),  
    path('staff_fetch_students', AcademicViews.staff_fetch_students, name='staff_fetch_students'),  
    path('get_students', AcademicViews.get_students, name='staff_get_students'),  
    path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', AcademicViews.download_student_results_excel, name='staff_download_student_results_excel'),
    path('staff_update_class_attendance', AcademicViews.staff_update_class_attendance, name='staff_update_class_attendance'),  
    path('staff_save_class_attendance_data', AcademicViews.staff_save_class_attendance_data, name='staff_save_class_attendance_data'),  
   
    path('staff_get_class_attendance_date', AcademicViews.staff_get_class_attendance_date, name='staff_get_class_attendance_date'),  
 
    path('get_class_student_attendance', AcademicViews.get_class_student_attendance, name='staff_get_class_student_attendance'),  
    
    path('staff_update_attendance', AcademicViews.staff_update_attendance, name='staff_update_attendance'),
    path('update_profile_picture/', AcademicViews.update_profile_picture, name='staff_update_profile_picture'),  
    path('save_class_updateattendance', AcademicViews.save_class_updateattendance, name='staff_save_class_updateattendance'),  
   
    path('staff_apply_leave', AcademicViews.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', AcademicViews.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', AcademicViews.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', AcademicViews.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_detail', AcademicViews.staff_detail, name='staff_detail'),  
    path('manage_student', AcademicViews.manage_student, name='staff_manage_student'),  
    path('student_general_attendance/<int:student_id>/', AcademicViews.student_general_attendance, name='staff_student_general_attendance'),
  
    
    path('import_subject_wise_result/<int:exam_type_id>/', StaffImports.import_subject_wise_result, name='staff_import_subject_wise_result'),
    
    path('add_results/', AcademicViews.add_results, name='staff_add_results'),
    path('add_student_result/', AcademicViews.add_student_result, name='staff_add_student_result'),
    path('save_marks_view/', AcademicViews.save_marks_view, name='staff_save_marks_endpoint'),
    path('delete_result_endpoint/', AcademicViews.delete_result_endpoint, name='staff_delete_result_endpoint'),
    path('student-results/', AcademicViews.student_results_view, name='staff_student_results'),
    path('exam-types/', AcademicViews.exam_type_list, name='staff_exam_type_list'),
    path('exam_type_to_view_class/<int:exam_type_id>/', AcademicViews.exam_type_to_view_class, name='staff_exam_type_to_view_class'),
    path('view_student_to_add_result/<int:exam_type_id>/<str:class_name>/', AcademicViews.view_student_to_add_result, name='staff_view_student_to_add_result'),
    path('manage_result/', AcademicViews.manage_result, name='staff_manage_result'),    
    path('students_wise_result_page/', AcademicViews.students_wise_result_page, name='staff_students_wise_result_page'),
    path('student_subject_wise_result/', AcademicViews.student_subject_wise_result, name='staff_student_subject_wise_result'),
    path('student_subject_wise_result_page/<int:student_id>/', AcademicViews.student_subject_wise_result_page, name='staff_student_subject_wise_result_page'),

 
]