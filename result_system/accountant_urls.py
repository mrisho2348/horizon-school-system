from django.urls import path, re_path
from result_module import  AccountantViews

urlpatterns = [
    # Accountant home page
    path('accountant/home/', AccountantViews.accountant_home, name='accountant_home'),
    path('update_payment/', AccountantViews.update_payment, name='accountant_update_payment'),
    path('update_student_status/', AccountantViews.update_student_status, name='accountant_update_student_status'),
    path('student_general_attendance/<int:student_id>/', AccountantViews.student_general_attendance, name='accountant_student_general_attendance'),
    path('student/<int:id>/', AccountantViews.student_details, name='accountant_student_details'),
    path('add_student/', AccountantViews.add_or_edit_student, name='accountant_add_student'),
    path('edit_student/<int:pk>/', AccountantViews.add_or_edit_student, name='accountant_edit_student'),
    path('student_subject_wise_result_page/<int:student_id>/', AccountantViews.student_subject_wise_result_page, name='accountant_student_subject_wise_result_page'),
    path('students/', AccountantViews.manage_student, name='accountant_manage_student'),  
    # Accountant leave application URLs
    path('accountant/leave/apply/', AccountantViews.staff_apply_leave, name='accountant_staff_apply_leave'),
    path('accountant/leave/apply/save/', AccountantViews.staff_apply_leave_save, name='accountant_staff_apply_leave_save'),

    # Accountant feedback URLs
    path('accountant/feedback/send/', AccountantViews.staff_sendfeedback, name='accountant_staff_sendfeedback'),
    path('accountant/feedback/send/save/', AccountantViews.staff_sendfeedback_save, name='accountant_staff_sendfeedback_save'),
    path('school-fees-installments/', AccountantViews.school_fees_installments_list, name='accountant_school_fees_installments_list'),
    path('add-installment/', AccountantViews.add_installment, name='accountant_add_installment'),
    path('delete/installment/', AccountantViews.delete_installment, name='accountant_delete_installment'),
    path('payments/', AccountantViews.payment_list, name='accountant_payment_list'),  
    path('add_payment/', AccountantViews.add_payment, name='accountant_add_payment'),
    path('delete_payment/', AccountantViews.delete_payment, name='accountant_delete_payment'),
    path('view_all_payments/<int:student_id>/', AccountantViews.view_all_payments, name='accountant_view_all_payments'),
    path('student_receipt/<int:student_id>/', AccountantViews.student_receipt, name='accountant_student_receipt'),
    path('fees_collected/', AccountantViews.fees_collected, name='accountant_fees_collected'),
    path('pending_payments/', AccountantViews.pending_payments, name='accountant_pending_payments'),
    path('expenditure/', AccountantViews.expenditure_list, name='accountant_expenditure'),
    path('fee_structure_list/', AccountantViews.fee_structure_list, name='accountant_fee_structure_list'),
    path('add_fee_structure/', AccountantViews.add_fee_structure, name='accountant_add_fee_structure'),
    path('fee-structures/edit/<int:pk>/', AccountantViews.add_fee_structure, name='accountant_edit_fee_structure'),
    path('fee-delete/delete/<int:pk>/', AccountantViews.delete_fee_structure, name='accountant_delete_fee_structure'),
    path('student_list/', AccountantViews.student_list, name='accountant_student_list'),
    path('get_financial_yearly_data/', AccountantViews.get_financial_yearly_data, name='accountant_get_financial_yearly_data'),
    path('get_school_fees_monthly_data/', AccountantViews.get_school_fees_monthly_data, name='accountant_get_school_fees_monthly_data'),
    path('get_expenditure_monthly_data/', AccountantViews.get_expenditure_monthly_data, name='accountant_get_expenditure_monthly_data'),
    path('get_classwise_fee_payment_data/', AccountantViews.get_classwise_fee_payment_data, name='accountant_get_classwise_fee_payment_data'),
   
    path('delete_expenditure/', AccountantViews.delete_expenditure, name='accountant_delete_expenditure'),
    path('update_profile_picture/', AccountantViews.update_profile_picture, name='accountant_update_profile_picture'),
    
    path('fee-structure/add/', AccountantViews.FeeStructureCreateView.as_view(), name='accountant_fee_structure_create'),
    path('fee-structure/edit/<int:pk>/', AccountantViews.FeeStructureCreateView.as_view(), name='accountant_fee_structure_edit'),
    path('fee-structure/list/', AccountantViews.FeeStructureListView.as_view(), name='accountant_fee_structure_list'),
    path('fee-structure/delete/<int:pk>/', AccountantViews.FeeStructureDeleteView.as_view(), name='accountant_fee_structure_delete'),
    
    
    path('expenditures/', AccountantViews.ExpenditureListView.as_view(), name='accountant_expenditure_list'),
    path('expenditure/add/', AccountantViews.ExpenditureCreateView.as_view(), name='accountant_add_expenditure'),
    path('expenditure/<int:pk>/edit/', AccountantViews.ExpenditureCreateView.as_view(), name='accountant_edit_expenditure'),
    path('expenditure/<int:pk>/delete/', AccountantViews.ExpenditureDeleteView.as_view(), name='accountant_delete_expenditure'),
    path('error/', AccountantViews.ErrorPageView.as_view(), name='accountant_error_page'),
    path('class_fees/', AccountantViews.ClassFeeListView.as_view(), name='accountant_class_fee_list'),
    path('class_fee/add/', AccountantViews.ClassFeeCreateView.as_view(), name='accountant_add_class_fee'),
    path('class_fee/<int:pk>/edit/', AccountantViews.ClassFeeCreateView.as_view(), name='accountant_edit_class_fee'),
    path('class_fee/<int:pk>/delete/', AccountantViews.ClassFeeDeleteView.as_view(), name='accountant_delete_class_fee'),
    
    path('madrasatul-fee/add/', AccountantViews.MadrasatulFeeCreateView.as_view(), name='accountant_madrasatul_fee_create'),     
    path('madrasatul-fee/edit/<int:pk>/', AccountantViews.MadrasatulFeeCreateView.as_view(), name='accountant_madrasatul_fee_edit'),       
    path('madrasatul-fee/list/', AccountantViews.MadrasatulFeeListView.as_view(), name='accountant_madrasatul_fee_list'),
    path('madrasatul-fee/delete/<int:pk>/', AccountantViews.MadrasatulFeeDeleteView.as_view(), name='accountant_madrasatul_fee_delete'),
        

    path('transport-fee/add/', AccountantViews.TransportFeeCreateUpdateView.as_view(), name='accountant_transport_fee_create'),
    path('transport-fee/edit/<int:pk>/', AccountantViews.TransportFeeCreateUpdateView.as_view(), name='accountant_transport_fee_edit'),
    path('transport-fee/', AccountantViews.TransportFeeListView.as_view(), name='accountant_transport_fee_list'),
    path('transport-fee/delete/<int:pk>/', AccountantViews.TransportFeeDeleteView.as_view(), name='accountant_transport_fee_delete'), 
    

    path('fee-payment/add/', AccountantViews.FeePaymentCreateUpdateView.as_view(), name='accountant_fee_payment_create'),
    path('fee-payment/edit/<int:pk>/', AccountantViews.FeePaymentCreateUpdateView.as_view(), name='accountant_fee_payment_edit'),
    path('fee-payment/', AccountantViews.FeePaymentListView.as_view(), name='accountant_fee_payment_list'),
    path('fee-payment/delete/<int:pk>/', AccountantViews.FeePaymentDeleteView.as_view(), name='accountant_fee_payment_delete'),
    
    path('madrasatul-fee-payments/add/', AccountantViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='accountant_madrasatul_fee_payment_create'),
    path('madrasatul-fee-payments/edit/<int:pk>/', AccountantViews.MadrasatulFeePaymentCreateUpdateView.as_view(), name='accountant_madrasatul_fee_payment_edit'),
    path('madrasatul-fee-payments/', AccountantViews.MadrasatulFeePaymentListView.as_view(), name='accountant_madrasatul_fee_payment_list'),
    path('madrasatul-fee-payments/delete/<int:pk>/', AccountantViews.MadrasatulFeePaymentDeleteView.as_view(), name='accountant_madrasatul_fee_payment_delete'),
    
    path('transport-fee-payments/', AccountantViews.TransportFeePaymentListView.as_view(), name='accountant_transport_fee_payment_list'),
    path('transport-fee-payments/add/', AccountantViews.TransportFeePaymentCreateUpdateView.as_view(), name='accountant_transport_fee_payment_create'),
    path('transport-fee-payments/edit/<int:pk>/', AccountantViews.TransportFeePaymentCreateUpdateView.as_view(), name='accountant_transport_fee_payment_edit'),
    path('transport-fee-payments/delete/<int:pk>/', AccountantViews.TransportFeePaymentDeleteView.as_view(), name='accountant_transport_fee_payment_delete'),
    
    path('fetch-payments/', AccountantViews.student_payment_fetch, name='accountant_student_payment_fetch'),
    path('fetch-payment/', AccountantViews.payment_fetch, name='accountant_payment_fetch'),
    path('fetch-students-per-class/', AccountantViews.fetch_students_per_class, name='accountant_fetch_students_per_class'),
    path('admin/fee-payment-monthly-data/', AccountantViews.get_fee_payment_monthly_data, name='accountant_get_fee_payment_monthly_data'),
    path('admin/madrasatul-fee-payment-monthly-data/', AccountantViews.get_madrasatul_fee_payment_monthly_data, name='accountant_get_madrasatul_fee_payment_monthly_data'),
    path('admin/transport-fee-payment-monthly-data/', AccountantViews.get_transport_fee_payment_monthly_data, name='accountant_get_transport_fee_payment_monthly_data'),
    path('subject-count-per-class-level/', AccountantViews.get_subject_count_per_class_level, name='accountant_get_subject_count_per_class_level'),
    # Accountant detail page
    path('accountant/detail/', AccountantViews.staff_detail, name='accountant_staff_detail'),
     path('filter-payments/', AccountantViews.filter_payments, name='accountant_filter_payments'),
     path('search_payments/', AccountantViews.search_payments, name='accountant_search_payments'),

]
