
from django.urls import include, path

from result_module import ClassTeacherViews, StaffImports

urlpatterns = [
 # staff url paths  
   
    path('get_class_student_attendance_data', ClassTeacherViews.get_class_student_attendance_data, name='staff_get_class_student_attendance_data'),  
    path('staff_view_class_attendance', ClassTeacherViews.staff_view_class_attendance, name='staff_view_class_attendance'),  
    path('staff_home', ClassTeacherViews.staff_home, name='staff_home'),  
    path('staff_take_class_attendance', ClassTeacherViews.staff_take_class_attendance, name='staff_take_class_attendance'),  
    path('staff_take_attendance', ClassTeacherViews.staff_take_attendance, name='staff_take_attendance'),  
    path('staff_fetch_students', ClassTeacherViews.staff_fetch_students, name='staff_fetch_students'),  
    path('get_students', ClassTeacherViews.get_students, name='staff_get_students'),  
    path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', ClassTeacherViews.download_student_results_excel, name='staff_download_student_results_excel'),
    path('staff_update_class_attendance', ClassTeacherViews.staff_update_class_attendance, name='staff_update_class_attendance'),  
    path('staff_save_class_attendance_data', ClassTeacherViews.staff_save_class_attendance_data, name='staff_save_class_attendance_data'),  
   
    path('staff_get_class_attendance_date', ClassTeacherViews.staff_get_class_attendance_date, name='staff_get_class_attendance_date'),  
 
    path('get_class_student_attendance', ClassTeacherViews.get_class_student_attendance, name='staff_get_class_student_attendance'),  
    
    path('staff_update_attendance', ClassTeacherViews.staff_update_attendance, name='staff_update_attendance'),
    path('update_profile_picture/', ClassTeacherViews.update_profile_picture, name='staff_update_profile_picture'),  
    path('save_class_updateattendance', ClassTeacherViews.save_class_updateattendance, name='staff_save_class_updateattendance'),  
   
    path('staff_apply_leave', ClassTeacherViews.staff_apply_leave, name='staff_apply_leave'),  
    path('staff_apply_leave_save', ClassTeacherViews.staff_apply_leave_save, name='staff_apply_leave_save'),  
    path('staff_sendfeedback', ClassTeacherViews.staff_sendfeedback, name='staff_sendfeedback'),  
    path('staff_sendfeedback_save', ClassTeacherViews.staff_sendfeedback_save, name='staff_sendfeedback_save'),  
    path('staff_detail', ClassTeacherViews.staff_detail, name='staff_detail'),  
    path('manage_student', ClassTeacherViews.manage_student, name='staff_manage_student'),  
    path('student_general_attendance/<int:student_id>/', ClassTeacherViews.student_general_attendance, name='staff_student_general_attendance'),
  
    
    path('import_subject_wise_result/<int:exam_type_id>/', StaffImports.import_subject_wise_result, name='staff_import_subject_wise_result'),
    
    path('add_results/', ClassTeacherViews.add_results, name='staff_add_results'),
    path('add_student_result/', ClassTeacherViews.add_student_result, name='staff_add_student_result'),
    path('save_marks_view/', ClassTeacherViews.save_marks_view, name='staff_save_marks_endpoint'),
    path('delete_result_endpoint/', ClassTeacherViews.delete_result_endpoint, name='staff_delete_result_endpoint'),
    path('student-results/', ClassTeacherViews.student_results_view, name='staff_student_results'),
    path('exam-types/', ClassTeacherViews.exam_type_list, name='staff_exam_type_list'),
    path('exam_type_to_view_class/<int:exam_type_id>/', ClassTeacherViews.exam_type_to_view_class, name='staff_exam_type_to_view_class'),
    path('view_student_to_add_result/<int:exam_type_id>/<str:class_name>/', ClassTeacherViews.view_student_to_add_result, name='staff_view_student_to_add_result'),
    path('manage_result/', ClassTeacherViews.manage_result, name='staff_manage_result'),    
    path('students_wise_result_page/', ClassTeacherViews.students_wise_result_page, name='staff_students_wise_result_page'),
    path('student_subject_wise_result/', ClassTeacherViews.student_subject_wise_result, name='staff_student_subject_wise_result'),
    path('student_subject_wise_result_page/<int:student_id>/', ClassTeacherViews.student_subject_wise_result_page, name='staff_student_subject_wise_result_page'),

 
]