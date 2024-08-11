
from django.urls import   path
from result_module import ExcelTemplate, HeadmasterViews, Delete, imports

urlpatterns = [       
        path('headmaster_get_class_student_attendance_data/',HeadmasterViews.get_class_student_attendance_data, name="headmaster_get_class_student_attendance_data"),
        path('classlevel/add/', HeadmasterViews.ClassLevelCreateUpdateView.as_view(), name='headmaster_classlevel_create'),
        path('classlevel/edit/<int:pk>/', HeadmasterViews.ClassLevelCreateUpdateView.as_view(), name='headmaster_classlevel_edit'),
        path('classlevel/delete/<int:pk>/', HeadmasterViews.ClassLevelDeleteView.as_view(), name='headmaster_classlevel_delete'),
        path('classlevel/', HeadmasterViews.ClassLevelListView.as_view(), name='headmaster_classlevel_list'),
        path('subject/add/', HeadmasterViews.SubjectCreateUpdateView.as_view(), name='headmaster_subject_create'),
        path('subject/edit/<int:pk>/', HeadmasterViews.SubjectCreateUpdateView.as_view(), name='headmaster_subject_edit'),
        path('subject/delete/<int:pk>/', HeadmasterViews.SubjectDeleteView.as_view(), name='headmaster_subject_delete'),
        
        path('installment/add/', HeadmasterViews.SchoolFeesInstallmentCreateView.as_view(), name='headmaster_installment_create'),
        path('installment/edit/<int:pk>/', HeadmasterViews.SchoolFeesInstallmentCreateView.as_view(), name='headmaster_installment_edit'),
        path('installments/', HeadmasterViews.SchoolFeesInstallmentListView.as_view(), name='headmaster_installment_list'), 
        path('installment/delete/<int:pk>/', HeadmasterViews.SchoolFeesInstallmentDeleteView.as_view(), name='headmaster_installment_delete'), 
        
        path('fee-structure/add/', HeadmasterViews.FeeStructureCreateView.as_view(), name='headmaster_fee_structure_create'),
        path('fee-structure/edit/<int:pk>/', HeadmasterViews.FeeStructureCreateView.as_view(), name='headmaster_fee_structure_edit'),
        path('fee-structure/list/', HeadmasterViews.FeeStructureListView.as_view(), name='headmaster_fee_structure_list'),
        path('fee-structure/delete/<int:pk>/', HeadmasterViews.FeeStructureDeleteView.as_view(), name='headmaster_fee_structure_delete'),
       
        
        path('expenditures/', HeadmasterViews.ExpenditureListView.as_view(), name='headmaster_expenditure_list'),
        path('expenditure/add/', HeadmasterViews.ExpenditureCreateView.as_view(), name='headmaster_add_expenditure'),
        path('expenditure/<int:pk>/edit/', HeadmasterViews.ExpenditureCreateView.as_view(), name='headmaster_edit_expenditure'),
        path('expenditure/<int:pk>/delete/', HeadmasterViews.ExpenditureDeleteView.as_view(), name='headmaster_delete_expenditure'),
        
        path('class_fees/', HeadmasterViews.ClassFeeListView.as_view(), name='headmaster_class_fee_list'),
        path('class_fee/add/', HeadmasterViews.ClassFeeCreateView.as_view(), name='headmaster_add_class_fee'),
        path('class_fee/<int:pk>/edit/', HeadmasterViews.ClassFeeCreateView.as_view(), name='headmaster_edit_class_fee'),
        path('class_fee/<int:pk>/delete/', HeadmasterViews.ClassFeeDeleteView.as_view(), name='headmaster_delete_class_fee'),
        
        path('madrasatul-fee/add/', HeadmasterViews.MadrasatulFeeCreateView.as_view(), name='headmaster_madrasatul_fee_create'),     
        path('madrasatul-fee/edit/<int:pk>/', HeadmasterViews.MadrasatulFeeCreateView.as_view(), name='headmaster_madrasatul_fee_edit'),       
        path('madrasatul-fee/list/', HeadmasterViews.MadrasatulFeeListView.as_view(), name='headmaster_madrasatul_fee_list'),
        path('madrasatul-fee/delete/<int:pk>/', HeadmasterViews.MadrasatulFeeDeleteView.as_view(), name='headmaster_madrasatul_fee_delete'),
         

        path('transport-fee/add/', HeadmasterViews.TransportFeeCreateUpdateView.as_view(), name='headmaster_transport_fee_create'),
        path('transport-fee/edit/<int:pk>/', HeadmasterViews.TransportFeeCreateUpdateView.as_view(), name='headmaster_transport_fee_edit'),
        path('transport-fee/', HeadmasterViews.TransportFeeListView.as_view(), name='headmaster_transport_fee_list'),
        path('transport-fee/delete/<int:pk>/', HeadmasterViews.TransportFeeDeleteView.as_view(), name='headmaster_transport_fee_delete'), 
        
  
        path('fee-payment/add/', HeadmasterViews.FeePaymentCreateUpdateView.as_view(), name='headmaster_fee_payment_create'),
        path('fee-payment/edit/<int:pk>/', HeadmasterViews.FeePaymentCreateUpdateView.as_view(), name='headmaster_fee_payment_edit'),
        path('fee-payment/', HeadmasterViews.FeePaymentListView.as_view(), name='headmaster_fee_payment_list'),
        path('fee-payment/delete/<int:pk>/', HeadmasterViews.FeePaymentDeleteView.as_view(), name='headmaster_fee_payment_delete'),
        
        path('madrasatul-fee-payments/add/', HeadmasterViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='headmaster_madrasatul_fee_payment_create'),
        path('madrasatul-fee-payments/edit/<int:pk>/', HeadmasterViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='headmaster_madrasatul_fee_payment_edit'),
        path('madrasatul-fee-payments/', HeadmasterViews.MadrasatulFeePaymentListView.as_view(), name='headmaster_madrasatul_fee_payment_list'),
        path('madrasatul-fee-payments/delete/<int:pk>/', HeadmasterViews.MadrasatulFeePaymentDeleteView.as_view(), name='headmaster_madrasatul_fee_payment_delete'),
        
        
        path('result/<int:exam_type_id>/<int:class_level_id>/', HeadmasterViews.ResultCreateUpdateView.as_view(), name='headmaster_add_result'),
        path('result/<int:exam_type_id>/<int:class_level_id>/<int:pk>/', HeadmasterViews.ResultCreateUpdateView.as_view(), name='headmaster_edit_result'),
        
        path('transport-fee-payments/', HeadmasterViews.TransportFeePaymentListView.as_view(), name='headmaster_transport_fee_payment_list'),
        path('transport-fee-payments/add/', HeadmasterViews.TransportFeePaymentCreateUpdateView.as_view(), name='headmaster_transport_fee_payment_create'),
        path('transport-fee-payments/edit/<int:pk>/', HeadmasterViews.TransportFeePaymentCreateUpdateView.as_view(), name='headmaster_transport_fee_payment_edit'),
        path('transport-fee-payments/delete/<int:pk>/', HeadmasterViews.TransportFeePaymentDeleteView.as_view(), name='headmaster_transport_fee_payment_delete'),
        
        
        path('student-result/add/<int:student_id>/<int:exam_type_id>/<int:class_level_id>/', HeadmasterViews.StudentResultCreateUpdateView.as_view(), name='headmaster_student_result_create_update'),

        path('headmaster_view_class_attendance/',HeadmasterViews.view_class_attendance, name="headmaster_view_class_attendance"),
     
        path('headmaster_home/',HeadmasterViews.headmaster_home, name="headmaster_home"),
        
        path('display_results/',HeadmasterViews.display_results, name="headmaster_display_results"),         
        path('update_staff_status/',HeadmasterViews.update_staff_status, name="headmaster_update_staff_status"),
        path('manage_staff/',HeadmasterViews.manage_staff, name="headmaster_manage_staff"),
        path('check_email_exist', HeadmasterViews.check_email_exist, name='headmaster_check_email_exist'),
        path('check_username_exist', HeadmasterViews.check_username_exist, name='headmaster_check_username_exist'),
        path('student/<int:id>/', HeadmasterViews.student_details, name='headmaster_student_details'),
        path('staff_feedback_message_replied', HeadmasterViews.staff_feedback_message_replied, name='headmaster_staff_feedback_message_replied'),
        path('staff_feedback_message', HeadmasterViews.staff_feedback_message, name='headmaster_staff_feedback_message'),
       
        path('staff_leave_view', HeadmasterViews.staff_leave_view, name='headmaster_staff_leave_view'), 
        path('download-template/<int:class_level_id>/', HeadmasterViews.download_excel_template, name='headmaster_download_excel_template'),

        path('staff_approve_leave/<str:leave_id>', HeadmasterViews.staff_approve_leave, name='headmaster_staff_approve_leave'), 
        path('staff_disapprove_leave/<str:leave_id>', HeadmasterViews.staff_disapprove_leave, name='headmaster_staff_disapprove_leave'), 
        
        path('headmaster_view_attendance', HeadmasterViews.view_attendance, name='headmaster_view_attendance'), 
   
        path('delete_staff/', HeadmasterViews.delete_staff, name='headmaster_delete_staff'),    
        path('save_exam_type/', HeadmasterViews.save_exam_type, name='headmaster_save_exam_type'),  
        path('save_marks_view/', HeadmasterViews.save_marks_view, name='headmaster_save_marks_endpoint'),
        path('delete_result_endpoint/', HeadmasterViews.delete_result_endpoint, name='headmaster_delete_result_endpoint'),              
       
        path('student-results/', HeadmasterViews.student_results_view, name='headmaster_student_results'),
        path('exam-types/', HeadmasterViews.exam_type_list, name='headmaster_exam_type_list'),
        path('exam_type_to_view_class/<int:exam_type_id>/', HeadmasterViews.exam_type_to_view_class, name='headmaster_exam_type_to_view_class'),
        path('view_student_to_add_result/<int:exam_type_id>/<int:class_level_id>/', HeadmasterViews.view_student_to_add_result, name='headmaster_view_student_to_add_result'),
        path('get_financial_yearly_data/', HeadmasterViews.get_financial_yearly_data, name='headmaster_get_financial_yearly_data'),
        path('get_school_fees_monthly_data/', HeadmasterViews.get_school_fees_monthly_data, name='headmaster_get_school_fees_monthly_data'),
        path('get_expenditure_monthly_data/', HeadmasterViews.get_expenditure_monthly_data, name='headmaster_get_expenditure_monthly_data'),
        path('get_classwise_fee_payment_data/', HeadmasterViews.get_classwise_fee_payment_data, name='headmaster_get_classwise_fee_payment_data'),
        path('view_all_payments/<int:student_id>/', HeadmasterViews.view_all_payments, name='headmaster_view_all_payments'),
        path('get_students_by_class/', HeadmasterViews.get_students_by_class, name='headmaster_get_students_by_class'),
        path('fees_collected/', HeadmasterViews.fees_collected, name='headmaster_fees_collected'),
        path('pending_payments/', HeadmasterViews.pending_payments, name='headmaster_pending_payments'),
        
         path('subject-count-per-class-level/', HeadmasterViews.get_subject_count_per_class_level, name='headmaster_get_subject_count_per_class_level'),
        path('admin/fee-payment-monthly-data/', HeadmasterViews.get_fee_payment_monthly_data, name='headmaster_get_fee_payment_monthly_data'),
        path('admin/madrasatul-fee-payment-monthly-data/', HeadmasterViews.get_madrasatul_fee_payment_monthly_data, name='headmaster_get_madrasatul_fee_payment_monthly_data'),
        path('admin/transport-fee-payment-monthly-data/', HeadmasterViews.get_transport_fee_payment_monthly_data, name='headmaster_get_transport_fee_payment_monthly_data'),
        
        path('fetch-students-per-class/', HeadmasterViews.fetch_students_per_class, name='headmaster_fetch_students_per_class'),
       
        path('expenditure/', HeadmasterViews.expenditure_list, name='headmaster_expenditure'),
        path('student_list/', HeadmasterViews.student_list, name='headmaster_student_list'),
        path('update_profile_picture/', HeadmasterViews.update_profile_picture, name='headmaster_update_profile_picture'), 
        path('filter-payments/', HeadmasterViews.filter_payments, name='headmaster_filter_payments'),
        path('fetch-payments/', HeadmasterViews.student_payment_fetch, name='headmaster_student_payment_fetch'),
        path('fetch-payment/', HeadmasterViews.payment_fetch, name='headmaster_payment_fetch'),
        path('add_student/', HeadmasterViews.add_or_edit_student, name='headmaster_add_student'),
        path('edit_student/<int:pk>/', HeadmasterViews.add_or_edit_student, name='headmaster_edit_student'),
        path('download-results/<int:student_id>/<int:exam_type_id>/<str:year>/', HeadmasterViews.download_student_results_excel, name='headmaster_download_student_results_excel'),
        path('school_fees_installments_list/', HeadmasterViews.school_fees_installments_list, name='headmaster_school_fees_installments_list'),
        path('search_payments/', HeadmasterViews.search_payments, name='headmaster_search_payments'),
        path('students/', HeadmasterViews.manage_student, name='headmaster_manage_student'),        
        path('staff/add/', HeadmasterViews.add_staff, name='headmaster_add_staff'),
        path('staff/edit/<int:pk>/', HeadmasterViews.edit_staff, name='headmaster_edit_staff'),
        path('manage_exam_type/', HeadmasterViews.manage_exam_type, name='headmaster_manage_exam_type'),
        path('manage_subject/', HeadmasterViews.manage_subject, name='headmaster_manage_subject'),    
        path('update_student_status/', HeadmasterViews.update_student_status, name='headmaster_update_student_status'),
        path('students_wise_result_page/', HeadmasterViews.students_wise_result_page, name='headmaster_students_wise_result_page'),
        path('student_subject_wise_result/', HeadmasterViews.student_subject_wise_result, name='headmaster_student_subject_wise_result'),
        path('student_subject_wise_result_page/<int:student_id>/', HeadmasterViews.student_subject_wise_result_page, name='headmaster_student_subject_wise_result_page'),
        path('student_general_attendance/<int:student_id>/', HeadmasterViews.student_general_attendance, name='headmaster_student_general_attendance'),
       
        # delete urls 
        path('delete_student/', Delete.delete_student, name='headmaster_delete_student'),
        path('delete_subject/<int:subject_id>/', Delete.delete_subject, name='headmaster_delete_subject'),
        path('delete_exam_type/', Delete.delete_exam_type, name='headmaster_delete_exam_type'),
        
        
        # imports urls 
         path('import_student_records', imports.import_student_records, name='headmaster_import_student_records'),
         path('import_subject_records', imports.import_subject_records, name='headmaster_import_subject_records'),
         path('import_exam_type_records', imports.import_exam_type_records, name='headmaster_import_exam_type_records'),
         path('import_subject_wise_result/<int:exam_type_id>/<int:class_level_id>/', imports.import_student_results, name='headmaster_import_student_results'),
         
         path('download/students-template/', ExcelTemplate.download_students_excel_template, name='headmaster_download_students_template'),
]
       
    
