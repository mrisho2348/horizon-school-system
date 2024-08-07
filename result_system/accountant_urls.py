from django.urls import path, re_path
from result_module import  AccountantViews

urlpatterns = [
    # Accountant home page
    path('accountant/home/', AccountantViews.accountant_home, name='accountant_home'),
    path('update_payment/', AccountantViews.update_payment, name='accountant_update_payment'),
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
    path('add_expenditure_view/', AccountantViews.add_expenditure_view, name='accountant_add_expenditure_view'),
    path('delete_expenditure/', AccountantViews.delete_expenditure, name='accountant_delete_expenditure'),
    path('update_profile_picture/', AccountantViews.update_profile_picture, name='accountant_update_profile_picture'),
    # Accountant detail page
    path('accountant/detail/', AccountantViews.staff_detail, name='accountant_staff_detail'),
     path('filter-payments/', AccountantViews.filter_payments, name='accountant_filter_payments'),
     path('search_payments/', AccountantViews.search_payments, name='accountant_search_payments'),

]
