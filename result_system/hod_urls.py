
from django.urls import   path
from result_module import ExcelTemplate, HodViews, Delete, imports

urlpatterns = [       
        path('admin_get_class_student_attendance_data/',HodViews.admin_get_class_student_attendance_data, name="admin_get_class_student_attendance_data"),
       
        path('admin_view_class_attendance/',HodViews.admin_view_class_attendance, name="admin_view_class_attendance"),
     
        path('admin_home/',HodViews.admin_home, name="admin_home"),
        path('display_results/',HodViews.display_results, name="admin_display_results"),
        path('save_student_result/',HodViews.save_student_result, name="admin_save_student_result"),
        path('add_staff_record/',HodViews.add_staff_record, name="admin_add_staff_record"),
        path('update_staff_status/',HodViews.update_staff_status, name="admin_update_staff_status"),
        path('manage_staff/',HodViews.manage_staff, name="admin_manage_staff"),
        path('check_email_exist', HodViews.check_email_exist, name='admin_check_email_exist'),
        path('check_username_exist', HodViews.check_username_exist, name='admin_check_username_exist'),
        
        path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied, name='admin_staff_feedback_message_replied'),
        path('staff_feedback_message', HodViews.staff_feedback_message, name='admin_staff_feedback_message'),
       
        path('staff_leave_view', HodViews.staff_leave_view, name='admin_staff_leave_view'), 
        path('download-template/<str:class_name>/', HodViews.download_excel_template, name='admin_download_excel_template'),

        path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave, name='admin_staff_approve_leave'), 
        path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave, name='admin_staff_disapprove_leave'), 
        path('admin_view_attendance', HodViews.admin_view_attendance, name='admin_view_attendance'), 
   
        path('delete_staff/', HodViews.delete_staff, name='admin_delete_staff'),
        path('save_student/', HodViews.save_student, name='admin_save_student'),
        path('add_student_result/', HodViews.add_student_result, name='admin_add_student_result'),
        path('save_subject/', HodViews.save_subject, name='admin_save_subject'),
        path('save_exam_type/', HodViews.save_exam_type, name='admin_save_exam_type'),
        path('add_results/', HodViews.add_results, name='admin_add_results'),
        path('save_marks_view/', HodViews.save_marks_view, name='admin_save_marks_endpoint'),
        path('delete_result_endpoint/', HodViews.delete_result_endpoint, name='admin_delete_result_endpoint'),              
       
        path('student-results/', HodViews.student_results_view, name='student_results'),
        path('exam-types/', HodViews.exam_type_list, name='admin_exam_type_list'),
        path('exam_type_to_view_class/<int:exam_type_id>/', HodViews.exam_type_to_view_class, name='admin_exam_type_to_view_class'),
        path('view_student_to_add_result/<int:exam_type_id>/<str:class_name>/', HodViews.view_student_to_add_result, name='admin_view_student_to_add_result'),
        path('get_financial_yearly_data/', HodViews.get_financial_yearly_data, name='admin_get_financial_yearly_data'),
        path('get_school_fees_monthly_data/', HodViews.get_school_fees_monthly_data, name='admin_get_school_fees_monthly_data'),
        path('get_expenditure_monthly_data/', HodViews.get_expenditure_monthly_data, name='admin_get_expenditure_monthly_data'),
        path('get_classwise_fee_payment_data/', HodViews.get_classwise_fee_payment_data, name='admin_get_classwise_fee_payment_data'),
        path('view_all_payments/<int:student_id>/', HodViews.view_all_payments, name='admin_view_all_payments'),
        path('get_students_by_class/', HodViews.get_students_by_class, name='admin_get_students_by_class'),
        path('fees_collected/', HodViews.fees_collected, name='admin_fees_collected'),
        path('pending_payments/', HodViews.pending_payments, name='admin_pending_payments'),
       
        path('expenditure/', HodViews.expenditure_list, name='admin_expenditure'),
        path('student_list/', HodViews.student_list, name='admin_student_list'),
         path('update_profile_picture/', HodViews.update_profile_picture, name='admin_update_profile_picture'), 
        path('filter-payments/', HodViews.filter_payments, name='admin_filter_payments'),
        path('add_student/', HodViews.add_or_edit_student, name='admin_add_student'),
        path('edit_student/<int:pk>/', HodViews.add_or_edit_student, name='admin_edit_student'),
        path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', HodViews.download_student_results_excel, name='admin_download_student_results_excel'),
        path('school_fees_installments_list/', HodViews.school_fees_installments_list, name='admin_school_fees_installments_list'),
        path('search_payments/', HodViews.search_payments, name='admin_search_payments'),
        path('students/', HodViews.manage_student, name='admin_manage_student'),        
        path('staff/add/', HodViews.add_staff, name='admin_add_staff'),
        path('staff/edit/<int:pk>/', HodViews.edit_staff, name='admin_edit_staff'),
        path('manage_exam_type/', HodViews.manage_exam_type, name='admin_manage_exam_type'),
        path('manage_subject/', HodViews.manage_subject, name='admin_manage_subject'),
        path('manage_result/', HodViews.manage_result, name='admin_manage_result'),
        path('update_student_status/', HodViews.update_student_status, name='admin_update_student_status'),
        path('students_wise_result_page/', HodViews.students_wise_result_page, name='admin_students_wise_result_page'),
        path('student_subject_wise_result/', HodViews.student_subject_wise_result, name='admin_student_subject_wise_result'),
        path('student_subject_wise_result_page/<int:student_id>/', HodViews.student_subject_wise_result_page, name='admin_student_subject_wise_result_page'),
        path('student_general_attendance/<int:student_id>/', HodViews.student_general_attendance, name='admin_student_general_attendance'),
       
        # delete urls 
        path('delete_student/', Delete.delete_student, name='admin_delete_student'),
        path('delete_subject/<int:subject_id>/', Delete.delete_subject, name='admin_delete_subject'),
        path('delete_exam_type/<int:exam_id>/', Delete.delete_exam_type, name='admin_delete_exam_type'),
        
        
        # imports urls 
         path('import_student_records', imports.import_student_records, name='admin_import_student_records'),
         path('import_subject_records', imports.import_subject_records, name='admin_import_subject_records'),
         path('import_exam_type_records', imports.import_exam_type_records, name='admin_import_exam_type_records'),
         path('import_subject_wise_result/<int:exam_type_id>/', imports.import_subject_wise_result, name='admin_import_subject_wise_result'),
         
         path('download/students-template/', ExcelTemplate.download_students_excel_template, name='admin_download_students_template'),
]
       
    
