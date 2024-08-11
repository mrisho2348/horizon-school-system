
from django.urls import   path
from result_module import ExcelTemplate, HodViews, Delete, imports

urlpatterns = [       
        path('admin_get_class_student_attendance_data/',HodViews.admin_get_class_student_attendance_data, name="admin_get_class_student_attendance_data"),
        path('classlevel/add/', HodViews.ClassLevelCreateUpdateView.as_view(), name='admin_classlevel_create'),
        path('classlevel/edit/<int:pk>/', HodViews.ClassLevelCreateUpdateView.as_view(), name='admin_classlevel_edit'),
        path('classlevel/delete/<int:pk>/', HodViews.ClassLevelDeleteView.as_view(), name='admin_classlevel_delete'),
        path('classlevel/', HodViews.ClassLevelListView.as_view(), name='admin_classlevel_list'),
        path('subject/add/', HodViews.SubjectCreateUpdateView.as_view(), name='admin_subject_create'),
        path('subject/edit/<int:pk>/', HodViews.SubjectCreateUpdateView.as_view(), name='admin_subject_edit'),
        path('subject/delete/<int:pk>/', HodViews.SubjectDeleteView.as_view(), name='admin_subject_delete'),
        
        path('installment/add/', HodViews.SchoolFeesInstallmentCreateView.as_view(), name='admin_installment_create'),
        path('installment/edit/<int:pk>/', HodViews.SchoolFeesInstallmentCreateView.as_view(), name='admin_installment_edit'),
        path('installments/', HodViews.SchoolFeesInstallmentListView.as_view(), name='admin_installment_list'), 
        path('installment/delete/<int:pk>/', HodViews.SchoolFeesInstallmentDeleteView.as_view(), name='admin_installment_delete'), 
        
        path('fee-structure/add/', HodViews.FeeStructureCreateView.as_view(), name='admin_fee_structure_create'),
        path('fee-structure/edit/<int:pk>/', HodViews.FeeStructureCreateView.as_view(), name='admin_fee_structure_edit'),
        path('fee-structure/list/', HodViews.FeeStructureListView.as_view(), name='admin_fee_structure_list'),
        path('fee-structure/delete/<int:pk>/', HodViews.FeeStructureDeleteView.as_view(), name='admin_fee_structure_delete'),
       
        
        path('expenditures/', HodViews.ExpenditureListView.as_view(), name='admin_expenditure_list'),
        path('expenditure/add/', HodViews.ExpenditureCreateView.as_view(), name='admin_add_expenditure'),
        path('expenditure/<int:pk>/edit/', HodViews.ExpenditureCreateView.as_view(), name='admin_edit_expenditure'),
        path('expenditure/<int:pk>/delete/', HodViews.ExpenditureDeleteView.as_view(), name='admin_delete_expenditure'),
        
        path('class_fees/', HodViews.ClassFeeListView.as_view(), name='admin_class_fee_list'),
        path('class_fee/add/', HodViews.ClassFeeCreateView.as_view(), name='admin_add_class_fee'),
        path('class_fee/<int:pk>/edit/', HodViews.ClassFeeCreateView.as_view(), name='admin_edit_class_fee'),
        path('class_fee/<int:pk>/delete/', HodViews.ClassFeeDeleteView.as_view(), name='admin_delete_class_fee'),
        
        path('madrasatul-fee/add/', HodViews.MadrasatulFeeCreateView.as_view(), name='admin_madrasatul_fee_create'),     
        path('madrasatul-fee/edit/<int:pk>/', HodViews.MadrasatulFeeCreateView.as_view(), name='admin_madrasatul_fee_edit'),       
        path('madrasatul-fee/list/', HodViews.MadrasatulFeeListView.as_view(), name='admin_madrasatul_fee_list'),
        path('madrasatul-fee/delete/<int:pk>/', HodViews.MadrasatulFeeDeleteView.as_view(), name='admin_madrasatul_fee_delete'),
         

        path('transport-fee/add/', HodViews.TransportFeeCreateUpdateView.as_view(), name='admin_transport_fee_create'),
        path('transport-fee/edit/<int:pk>/', HodViews.TransportFeeCreateUpdateView.as_view(), name='admin_transport_fee_edit'),
        path('transport-fee/', HodViews.TransportFeeListView.as_view(), name='admin_transport_fee_list'),
        path('transport-fee/delete/<int:pk>/', HodViews.TransportFeeDeleteView.as_view(), name='admin_transport_fee_delete'), 
        
  
        path('fee-payment/add/', HodViews.FeePaymentCreateUpdateView.as_view(), name='admin_fee_payment_create'),
        path('fee-payment/edit/<int:pk>/', HodViews.FeePaymentCreateUpdateView.as_view(), name='admin_fee_payment_edit'),
        path('fee-payment/', HodViews.FeePaymentListView.as_view(), name='admin_fee_payment_list'),
        path('fee-payment/delete/<int:pk>/', HodViews.FeePaymentDeleteView.as_view(), name='admin_fee_payment_delete'),
        
        path('madrasatul-fee-payments/add/', HodViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='admin_madrasatul_fee_payment_create'),
        path('madrasatul-fee-payments/edit/<int:pk>/', HodViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='admin_madrasatul_fee_payment_edit'),
        path('madrasatul-fee-payments/', HodViews.MadrasatulFeePaymentListView.as_view(), name='admin_madrasatul_fee_payment_list'),
        path('madrasatul-fee-payments/delete/<int:pk>/', HodViews.MadrasatulFeePaymentDeleteView.as_view(), name='admin_madrasatul_fee_payment_delete'),
        
        
        path('result/<int:exam_type_id>/<int:class_level_id>/', HodViews.ResultCreateUpdateView.as_view(), name='admin_add_result'),
        path('result/<int:exam_type_id>/<int:class_level_id>/<int:pk>/', HodViews.ResultCreateUpdateView.as_view(), name='admin_edit_result'),
        
        path('transport-fee-payments/', HodViews.TransportFeePaymentListView.as_view(), name='admin_transport_fee_payment_list'),
        path('transport-fee-payments/add/', HodViews.TransportFeePaymentCreateUpdateView.as_view(), name='admin_transport_fee_payment_create'),
        path('transport-fee-payments/edit/<int:pk>/', HodViews.TransportFeePaymentCreateUpdateView.as_view(), name='admin_transport_fee_payment_edit'),
        path('transport-fee-payments/delete/<int:pk>/', HodViews.TransportFeePaymentDeleteView.as_view(), name='admin_transport_fee_payment_delete'),
        
        
        path('student-result/add/<int:student_id>/<int:exam_type_id>/<int:class_level_id>/', HodViews.StudentResultCreateUpdateView.as_view(), name='admin_student_result_create_update'),

        path('admin_view_class_attendance/',HodViews.admin_view_class_attendance, name="admin_view_class_attendance"),
     
        path('admin_home/',HodViews.admin_home, name="admin_home"),
        path('display_results/',HodViews.display_results, name="admin_display_results"),
        path('save_student_result/',HodViews.save_student_result, name="admin_save_student_result"),       
        path('update_staff_status/',HodViews.update_staff_status, name="admin_update_staff_status"),
        path('manage_staff/',HodViews.manage_staff, name="admin_manage_staff"),
        path('check_email_exist', HodViews.check_email_exist, name='admin_check_email_exist'),
        path('check_username_exist', HodViews.check_username_exist, name='admin_check_username_exist'),
        path('student/<int:id>/', HodViews.student_details, name='admin_student_details'),
        path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied, name='admin_staff_feedback_message_replied'),
        path('staff_feedback_message', HodViews.staff_feedback_message, name='admin_staff_feedback_message'),
       
        path('staff_leave_view', HodViews.staff_leave_view, name='admin_staff_leave_view'), 
        path('download-template/<int:class_level_id>/', HodViews.download_excel_template, name='admin_download_excel_template'),

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
       
        path('student-results/', HodViews.student_results_view, name='admin_student_results'),
        path('exam-types/', HodViews.exam_type_list, name='admin_exam_type_list'),
        path('exam_type_to_view_class/<int:exam_type_id>/', HodViews.exam_type_to_view_class, name='admin_exam_type_to_view_class'),
        path('view_student_to_add_result/<int:exam_type_id>/<int:class_level_id>/', HodViews.view_student_to_add_result, name='admin_view_student_to_add_result'),
        path('get_financial_yearly_data/', HodViews.get_financial_yearly_data, name='admin_get_financial_yearly_data'),
        path('get_school_fees_monthly_data/', HodViews.get_school_fees_monthly_data, name='admin_get_school_fees_monthly_data'),
        path('get_expenditure_monthly_data/', HodViews.get_expenditure_monthly_data, name='admin_get_expenditure_monthly_data'),
        path('get_classwise_fee_payment_data/', HodViews.get_classwise_fee_payment_data, name='admin_get_classwise_fee_payment_data'),
        path('view_all_payments/<int:student_id>/', HodViews.view_all_payments, name='admin_view_all_payments'),
        path('get_students_by_class/', HodViews.get_students_by_class, name='admin_get_students_by_class'),
        path('fees_collected/', HodViews.fees_collected, name='admin_fees_collected'),
        path('pending_payments/', HodViews.pending_payments, name='admin_pending_payments'),
        
         path('subject-count-per-class-level/', HodViews.get_subject_count_per_class_level, name='admin_get_subject_count_per_class_level'),
        path('admin/fee-payment-monthly-data/', HodViews.get_fee_payment_monthly_data, name='admin_get_fee_payment_monthly_data'),
        path('admin/madrasatul-fee-payment-monthly-data/', HodViews.get_madrasatul_fee_payment_monthly_data, name='admin_get_madrasatul_fee_payment_monthly_data'),
        path('admin/transport-fee-payment-monthly-data/', HodViews.get_transport_fee_payment_monthly_data, name='admin_get_transport_fee_payment_monthly_data'),
        
        path('fetch-students-per-class/', HodViews.fetch_students_per_class, name='admin_fetch_students_per_class'),
       
        path('expenditure/', HodViews.expenditure_list, name='admin_expenditure'),
        path('student_list/', HodViews.student_list, name='admin_student_list'),
         path('update_profile_picture/', HodViews.update_profile_picture, name='admin_update_profile_picture'), 
        path('filter-payments/', HodViews.filter_payments, name='admin_filter_payments'),
        path('fetch-payments/', HodViews.student_payment_fetch, name='admin_student_payment_fetch'),
        path('fetch-payment/', HodViews.payment_fetch, name='admin_payment_fetch'),
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
        path('branch_student_counts/', HodViews.get_branch_student_counts, name='admin_branch_student_counts'),
        path('gender_branch_student_counts/', HodViews.get_gender_branch_student_counts, name='admin_gender_branch_student_counts'),
        path('class_level_branch_counts/', HodViews.get_class_level_branch_counts, name='admin_class_level_branch_counts'),
        path('manage_result/', HodViews.manage_result, name='admin_manage_result'),
        path('update_student_status/', HodViews.update_student_status, name='admin_update_student_status'),
        path('students_wise_result_page/', HodViews.students_wise_result_page, name='admin_students_wise_result_page'),
        path('student_subject_wise_result/', HodViews.student_subject_wise_result, name='admin_student_subject_wise_result'),
        path('student_subject_wise_result_page/<int:student_id>/', HodViews.student_subject_wise_result_page, name='admin_student_subject_wise_result_page'),
        path('student_general_attendance/<int:student_id>/', HodViews.student_general_attendance, name='admin_student_general_attendance'),
       
        # delete urls 
        path('delete_student/', Delete.delete_student, name='admin_delete_student'),
        path('delete_subject/<int:subject_id>/', Delete.delete_subject, name='admin_delete_subject'),
        path('delete_exam_type/', Delete.delete_exam_type, name='admin_delete_exam_type'),
        
        
        # imports urls 
         path('import_student_records', imports.import_student_records, name='admin_import_student_records'),
         path('import_subject_records', imports.import_subject_records, name='admin_import_subject_records'),
         path('import_exam_type_records', imports.import_exam_type_records, name='admin_import_exam_type_records'),
         path('import_subject_wise_result/<int:exam_type_id>/<int:class_level_id>/', imports.import_student_results, name='admin_import_student_results'),
         
         path('download/students-template/', ExcelTemplate.download_students_excel_template, name='admin_download_students_template'),
]
       
    
