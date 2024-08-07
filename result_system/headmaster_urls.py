
from django.urls import   path

from result_module import ExcelTemplate, HeadmasterViews, imports, Delete


urlpatterns = [       
        path('admin_get_class_student_attendance_data/',HeadmasterViews.admin_get_class_student_attendance_data, name="admin_get_class_student_attendance_data"),
     
        path('admin_view_class_attendance/',HeadmasterViews.admin_view_class_attendance, name="admin_view_class_attendance"),

        path('admin_home/',HeadmasterViews.admin_home, name="admin_home"),
        path('display_results/',HeadmasterViews.display_results, name="admin_display_results"),
        path('save_student_result/',HeadmasterViews.save_student_result, name="admin_save_student_result"),
        path('add_staff_record/',HeadmasterViews.add_staff_record, name="admin_add_staff_record"),
        path('update_staff_status/',HeadmasterViews.update_staff_status, name="admin_update_staff_status"),
        path('manage_staff/',HeadmasterViews.manage_staff, name="admin_manage_staff"),
        path('check_email_exist', HeadmasterViews.check_email_exist, name='admin_check_email_exist'),
        path('check_username_exist', HeadmasterViews.check_username_exist, name='admin_check_username_exist'),
        
        path('staff_feedback_message_replied', HeadmasterViews.staff_feedback_message_replied, name='admin_staff_feedback_message_replied'),

        path('staff_leave_view', HeadmasterViews.staff_leave_view, name='admin_staff_leave_view'), 
        path('download-template/<str:class_name>/', HeadmasterViews.download_excel_template, name='admin_download_excel_template'),
    
        path('staff_approve_leave/<str:leave_id>', HeadmasterViews.staff_approve_leave, name='admin_staff_approve_leave'), 
        path('staff_disapprove_leave/<str:leave_id>', HeadmasterViews.staff_disapprove_leave, name='admin_staff_disapprove_leave'), 
        path('admin_view_attendance', HeadmasterViews.admin_view_attendance, name='admin_view_attendance'), 

        path('delete_staff/', HeadmasterViews.delete_staff, name='admin_delete_staff'),
        path('save_student/', HeadmasterViews.save_student, name='admin_save_student'),
        path('add_student_result/', HeadmasterViews.add_student_result, name='admin_add_student_result'),
        path('save_subject/', HeadmasterViews.save_subject, name='admin_save_subject'),
        path('save_exam_type/', HeadmasterViews.save_exam_type, name='admin_save_exam_type'),
        path('add_results/', HeadmasterViews.add_results, name='admin_add_results'),
        path('save_marks_view/', HeadmasterViews.save_marks_view, name='admin_save_marks_endpoint'),
        path('delete_result_endpoint/', HeadmasterViews.delete_result_endpoint, name='admin_delete_result_endpoint'),             
        path('student-results/', HeadmasterViews.student_results_view, name='student_results'),
        path('exam-types/', HeadmasterViews.exam_type_list, name='admin_exam_type_list'),
        path('exam_type_to_view_class/<int:exam_type_id>/', HeadmasterViews.exam_type_to_view_class, name='admin_exam_type_to_view_class'),
        path('view_student_to_add_result/<int:exam_type_id>/<str:class_name>/', HeadmasterViews.view_student_to_add_result, name='admin_view_student_to_add_result'),
        path('get_financial_yearly_data/', HeadmasterViews.get_financial_yearly_data, name='admin_get_financial_yearly_data'),
        path('get_school_fees_monthly_data/', HeadmasterViews.get_school_fees_monthly_data, name='admin_get_school_fees_monthly_data'),
        path('get_expenditure_monthly_data/', HeadmasterViews.get_expenditure_monthly_data, name='admin_get_expenditure_monthly_data'),
        path('get_classwise_fee_payment_data/', HeadmasterViews.get_classwise_fee_payment_data, name='admin_get_classwise_fee_payment_data'),
        path('view_all_payments/<int:student_id>/', HeadmasterViews.view_all_payments, name='admin_view_all_payments'),
        path('get_students_by_class/', HeadmasterViews.get_students_by_class, name='admin_get_students_by_class'),
        path('fees_collected/', HeadmasterViews.fees_collected, name='admin_fees_collected'),
        path('pending_payments/', HeadmasterViews.pending_payments, name='admin_pending_payments'),    
        path('expenditure/', HeadmasterViews.expenditure_list, name='admin_expenditure'),
        path('student_list/', HeadmasterViews.student_list, name='admin_student_list'),
         path('update_profile_picture/', HeadmasterViews.update_profile_picture, name='admin_update_profile_picture'), 
        path('filter-payments/', HeadmasterViews.filter_payments, name='admin_filter_payments'),
        path('add_student/', HeadmasterViews.add_or_edit_student, name='admin_add_student'),
        path('edit_student/<int:pk>/', HeadmasterViews.add_or_edit_student, name='admin_edit_student'),
        path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', HeadmasterViews.download_student_results_excel, name='admin_download_student_results_excel'),
        path('school_fees_installments_list/', HeadmasterViews.school_fees_installments_list, name='admin_school_fees_installments_list'),
        path('search_payments/', HeadmasterViews.search_payments, name='admin_search_payments'),
        path('students/', HeadmasterViews.manage_student, name='admin_manage_student'),        
        path('staff/add/', HeadmasterViews.add_staff, name='admin_add_staff'),
        path('staff/edit/<int:pk>/', HeadmasterViews.edit_staff, name='admin_edit_staff'),
        path('manage_exam_type/', HeadmasterViews.manage_exam_type, name='admin_manage_exam_type'),
        path('manage_subject/', HeadmasterViews.manage_subject, name='admin_manage_subject'),
        path('manage_result/', HeadmasterViews.manage_result, name='admin_manage_result'),
        path('update_student_status/', HeadmasterViews.update_student_status, name='admin_update_student_status'),
        path('students_wise_result_page/', HeadmasterViews.students_wise_result_page, name='admin_students_wise_result_page'),
        path('student_subject_wise_result/', HeadmasterViews.student_subject_wise_result, name='admin_student_subject_wise_result'),
        path('student_subject_wise_result_page/<int:student_id>/', HeadmasterViews.student_subject_wise_result_page, name='admin_student_subject_wise_result_page'),
        path('student_general_attendance/<int:student_id>/', HeadmasterViews.student_general_attendance, name='admin_student_general_attendance'),
       
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
       
    
