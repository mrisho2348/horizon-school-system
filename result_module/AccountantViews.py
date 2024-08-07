import datetime
from decimal import Decimal
import json
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum, F
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET,require_POST
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from result_module.forms import FeeStructureForm
from result_module.models import (
    Expenditure,
    FeeStructure,
    FeedBackStaff,
    LeaveReportStaffs,   
    SchoolFeesInstallment,
    SchoolFeesPayment,   
    Staffs,
    Students,
    )


@login_required
def accountant_home(request):
    try:
        staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        # Handle the case when the staff doesn't exist for the logged-in user
        return render(request, "accountant_template/error.html")

    # Counting the total number of students
    students_count = Students.objects.count()
 
    # Counting the total number of approved leaves for the current staff
    leave_count = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()

    # Calculating total fees collected
    total_fees_collected = SchoolFeesPayment.objects.aggregate(total_collected=models.Sum('amount_paid'))['total_collected'] or 0

    # Counting pending payments
    pending_payments_count = SchoolFeesPayment.objects.filter(amount_remaining__gt=0).count()

    # Calculating total expenditure
    total_expenditure = Expenditure.objects.aggregate(total_spent=models.Sum('amount'))['total_spent'] or 0
    net_profit =  total_fees_collected - total_expenditure
    context = {
     
        "student_count": students_count,
        "leave_count": leave_count,
        "total_fees_collected": total_fees_collected,
        "pending_payments_count": pending_payments_count,
        "total_expenditure": total_expenditure,
        "net_profit": net_profit,
        "staff": staff,
    }

    return render(request, "accountant_template/accountant_home.html", context)


def get_financial_yearly_data(request):
    if request.method == 'GET' and 'year' in request.GET:
        selected_year = request.GET.get('year')
        # Example query to fetch financial data for the selected year
        try:
            # Fetch fees collected (income)
            fees_collected = SchoolFeesPayment.objects.filter(date_paid__year=selected_year).aggregate(total_fees_collected=models.Sum('amount_paid'))['total_fees_collected'] or 0
           
            # Fetch expenditure (example: assuming you have an Expenditure model)
            expenditure = Expenditure.objects.filter(date__year=selected_year).aggregate(total_expenditure=models.Sum('amount'))['total_expenditure'] or 0

            # Prepare data to return as JSON
            data = {
                'income': (fees_collected),
                'expenditure': expenditure,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle invalid requests or missing parameters
    return JsonResponse({'error': 'Invalid request'})

@require_GET
def get_school_fees_monthly_data(request):
    year = request.GET.get('year')
    
    # Initialize monthly data dictionary
    monthly_data_dict = {}
    
    # Fetch monthly income data (fees collected)
    fees_collected_data = SchoolFeesPayment.objects.filter(date_paid__year=year).values('date_paid__month').annotate(
        income=Sum('amount_paid')
    ).order_by('date_paid__month')

    for entry in fees_collected_data:
        month = entry['date_paid__month']
        if month not in monthly_data_dict:
            monthly_data_dict[month] = {'income': 0, 'expenditure': 0}
        monthly_data_dict[month]['income'] += entry['income']

    # Prepare response data
    response_data = []
    for month in sorted(monthly_data_dict.keys()):
        response_data.append({
            'month': month,
            'income': monthly_data_dict[month]['income'],
            'expenditure': 0,  # No expenditure data for SchoolFeesPayment
        })

    return JsonResponse(response_data, safe=False)


@require_GET
def get_expenditure_monthly_data(request):
    year = request.GET.get('year')
    
    # Initialize monthly data dictionary
    monthly_data_dict = {}
    
    # Fetch monthly expenditure data
    expenditure_data = Expenditure.objects.filter(date__year=year).values('date__month').annotate(
        expenditure=Sum('amount')
    ).order_by('date__month')

    for entry in expenditure_data:
        month = entry['date__month']
        if month not in monthly_data_dict:
            monthly_data_dict[month] = {'income': 0, 'expenditure': 0}
        monthly_data_dict[month]['expenditure'] += entry['expenditure']

    # Prepare response data
    response_data = []
    for month in sorted(monthly_data_dict.keys()):
        response_data.append({
            'month': month,
            'income': 0,  # No income data for Expenditure
            'expenditure': monthly_data_dict[month]['expenditure'],
        })

    return JsonResponse(response_data, safe=False)

@require_GET
def get_classwise_fee_payment_data(request):
    try:
        year = request.GET.get('year')

        # Query to count number of distinct students per class who have made payments
        classwise_data = Students.objects.filter(
            schoolfeespayment__date_paid__year=year
        ).values('current_class').annotate(
            fee_payments_count=Count('id', distinct=True)
        ).order_by('current_class')

        # Prepare response data
        response_data = []
        for entry in classwise_data:
            response_data.append({
                'class_name': entry['current_class'],
                'fee_payments_count': entry['fee_payments_count'],
            })

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def student_list(request):
    students = Students.objects.all()
    context = {
        'students': students
    }
    return render(request, 'accountant_template/student_list.html', context)

def school_fees_installments_list(request):
    installments = SchoolFeesInstallment.objects.all()
    context = {
        'installments': installments
    }
    return render(request, 'accountant_template/school_fees_installments_list.html', context)

def fees_collected(request):
    total_fees_collected = SchoolFeesPayment.objects.aggregate(total_collected=models.Sum('amount_paid'))['total_collected'] or 0
    installments = SchoolFeesPayment.objects.filter(amount_remaining=0)
    context = {
        'installments': installments,
        'total_fees_collected': total_fees_collected
    }
    return render(request, 'accountant_template/fees_collected.html', context)

def pending_payments(request):
    pending_payments = SchoolFeesPayment.objects.filter(payment_status='Incomplete')
    context = {
        'pending_payments': pending_payments
    }
    return render(request, 'accountant_template/pending_payments.html', context)

def expenditure_list(request):
    expenditures = Expenditure.objects.all()
    total_expenditure = Expenditure.objects.aggregate(total=models.Sum('amount'))['total'] or 0
    context = {
        'expenditures': expenditures,
        'total_expenditure': total_expenditure
    }
    return render(request, 'accountant_template/expenditure.html', context)

@require_POST
@csrf_exempt
def add_expenditure_view(request):
    try:
        # Deserialize request data
        data = json.loads(request.body)
        
        # Extract form data
        expenditure_id = data.get('expenditure_id', None)  # If 'id' is present, it indicates an update request
        description = data.get('description')
        amount = Decimal(data.get('amount'))  # Convert amount to Decimal
        date = data.get('date')
        category = data.get('category')

        # Validate expenditure amount against available funds
        if category in ['Salary', 'Utilities', 'Supplies', 'Maintenance']:  # Assuming these categories are income related
            total_income = Decimal(SchoolFeesPayment.objects.aggregate(total_income=Sum('amount_paid'))['total_income'] or 0)
            total_expenditure = Decimal(Expenditure.objects.filter(category=category).aggregate(total_expenditure=Sum('amount'))['total_expenditure'] or 0)
            available_amount = total_income - total_expenditure
            if amount > available_amount:
                return JsonResponse({'success': False, 'error': f'Amount exceeds available funds ({available_amount}).'})

        # Validate expenditure amount against all amount paid
        if category == 'Other':  # Adjust the condition based on your specific logic
            total_amount_paid = Decimal(SchoolFeesPayment.objects.aggregate(total_amount_paid=Sum('amount_paid'))['total_amount_paid'] or 0)
            if amount > total_amount_paid:
                return JsonResponse({'success': False, 'error': f'Amount exceeds total amount paid ({total_amount_paid}).'})
        
        if expenditure_id:
            # Update existing expenditure object
            expenditure = Expenditure.objects.get(id=expenditure_id)
            expenditure.description = description
            expenditure.amount = amount
            expenditure.date = date
            expenditure.category = category
            expenditure.save()
            
            # Prepare success response for update
            response_data = {
                'success': True,
                'message': f'Expenditure "{expenditure}" updated successfully.'
            }
        else:
            # Create new Expenditure object
            expenditure = Expenditure.objects.create(
                description=description,
                amount=amount,
                date=date,
                category=category
            )
            
            # Prepare success response for creation
            response_data = {
                'success': True,
                'message': f'Expenditure "{expenditure}" added successfully.'
            }
        
        return JsonResponse(response_data)
    
    except ObjectDoesNotExist as e:
        return JsonResponse({'success': False, 'error': 'Expenditure not found.'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
@csrf_exempt
def delete_expenditure(request):
    try:
        expenditure_id = request.POST.get('expenditure_id')
        expenditure = get_object_or_404(Expenditure, id=expenditure_id)
        expenditure.delete()
        
        return JsonResponse({'success': True, 'message': f'Expenditure "{expenditure.description}" deleted successfully.'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def add_installment(request):
    if request.method == 'POST':
        installment_id = request.POST.get('installment_id')
        installment_name = request.POST.get('installment_name')
        amount_required = request.POST.get('amount_required')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        school_class = request.POST.get('school_class')
        
        try:
            start_date =  datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date =  datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if start_date >= end_date:
                return JsonResponse({'status': False, 'message': 'Start date must be before the end date.'})

           
            if installment_id:
                # Editing existing installment
                if SchoolFeesInstallment.objects.exclude(pk=installment_id).filter(
                    installment_name=installment_name,
                    end_date__gte=start_date,
                    school_class=school_class,
                ).exists():
                    return JsonResponse({'status': False, 'message': 'Another installment with the same name already exists.'})        

                installment = SchoolFeesInstallment.objects.get(pk=installment_id)
                installment.installment_name = installment_name
                installment.amount_required = amount_required
                installment.start_date = start_date
                installment.end_date = end_date
                installment.school_class = school_class
                installment.save()
                return JsonResponse({'status': True, 'message': 'Installment updated successfully!'})
            else:
                 # Check if the school class already has three installments
                if SchoolFeesInstallment.objects.filter(school_class=school_class).count() >= 3:
                    return JsonResponse({'status': False, 'message': 'Each school class can have only three installments.'})

                # Adding new installment              
                previous_installment_end_date = SchoolFeesInstallment.objects.filter(
                    school_class=school_class
                ).order_by('-end_date').first()

                if previous_installment_end_date and start_date <= previous_installment_end_date.end_date:
                    return JsonResponse({'status': False, 'message': 'Start date must be after the end date of the previous installment.'})

                if SchoolFeesInstallment.objects.filter(
                    installment_name=installment_name,
                    end_date__gte=start_date
                ).exists():
                    return JsonResponse({'status': False, 'message': 'An installment with similar details already exists.'})

                SchoolFeesInstallment.objects.create(
                    installment_name=installment_name,
                    amount_required=amount_required,
                    start_date=start_date,
                    end_date=end_date,
                    school_class=school_class
                )
                return JsonResponse({'status': True, 'message': 'Installment added successfully!'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request method.'})


@csrf_exempt
def delete_installment(request):
    if request.method == 'POST':
        installment_id = request.POST.get('installment_id')
        try:
            installment = SchoolFeesInstallment.objects.get(pk=installment_id)
            installment.delete()
            return JsonResponse({'status': True, 'message': 'Installment deleted successfully!'})
        except SchoolFeesInstallment.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Installment not found.'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def payment_list(request):
    payments = SchoolFeesPayment.objects.all().select_related('student', 'installment')
    students = Students.objects.all() 
    return render(request, 'accountant_template/payment_list.html', {'payments': payments,'students':students})


@csrf_exempt
def delete_payment(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('payment_id')
            payment = SchoolFeesPayment.objects.get(id=payment_id)
            payment.delete()
            return JsonResponse({'status': True, 'message': 'Payment deleted successfully'})
        except SchoolFeesPayment.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Payment does not exist'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request'})

@login_required
def staff_sendfeedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request,"accountant_template/staff_feedback.html",{"feedback_data":feedback_data,'staff':staff,})

def staff_sendfeedback_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("staff_sendfeedback"))
    
    else:
       feedback_msg = request.POST.get("feedback_msg") 
       staff_obj = Staffs.objects.get(admin=request.user.id)
       try:           
          feedback_report = FeedBackStaff(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
          feedback_report.save()
          messages.success(request,"feedback Successfully  sent")
          return HttpResponseRedirect(reverse("staff_sendfeedback"))  
             
       except:
            messages.error(request,"feedback failed to be sent")
            return HttpResponseRedirect(reverse("staff_sendfeedback"))

@login_required
def   staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    staff_leave_report = LeaveReportStaffs.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request,"accountant_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report, 'staff':staff,})



def staff_apply_leave_save(request):
    if request.method!= "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")     
        staff_obj = Staffs.objects.get(admin=request.user.id)
       
        try:            
          leave_report =LeaveReportStaffs(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
          leave_report.save()
          messages.success(request,"Successfully  staff apply leave ")
          return HttpResponseRedirect(reverse("staff_apply_leave"))  
             
        except:
            messages.error(request,"failed for staff to apply for leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        


@login_required
def staff_detail(request):
    staff = Staffs.objects.get(admin=request.user.id)
    # Fetch additional staff-related data  
    context = {
        'staff': staff,     
    }
    return render(request, "accountant_template/staff_details.html", context) 



@csrf_exempt
def add_payment(request):
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student')
            amount_paid = int(request.POST.get('amount_paid'))
            date_paid = request.POST.get('date_paid')

            student = Students.objects.get(id=student_id)

            # Find the correct installment for the payment date
            installment = SchoolFeesInstallment.objects.filter(
                school_class=student.current_class,
                start_date__lte=date_paid,
                end_date__gte=date_paid
            ).first()

            if not installment:
                return JsonResponse({'status': False, 'message': 'No installment found for the given date'})

            # Fetch all previous payments for the student, ordered by date
            previous_payments = SchoolFeesPayment.objects.filter(student=student).order_by('date_paid')

            total_paid = amount_paid

            # Iterate over previous payments to clear any remaining amount and balance
            for payment in previous_payments:
                if payment.amount_remaining > 0:
                    if total_paid >= payment.amount_remaining:
                        total_paid -= payment.amount_remaining
                        payment.amount_paid += payment.amount_remaining
                        payment.amount_remaining = 0
                        payment.payment_status = 'Completed'
                    else:
                        payment.amount_remaining -= total_paid
                        payment.amount_paid += payment.amount_remaining
                        total_paid = 0
                        payment.payment_status = 'Incomplete'
                    payment.balance = max(payment.amount_paid - payment.installment.amount_required, 0)                    
                    payment.save()
                elif payment.balance > 0:
                    total_paid += payment.balance
                    payment.balance = 0
                    payment.save()

            
            # Check if there's an existing payment for the same installment and student
            existing_payment = SchoolFeesPayment.objects.filter(
                student=student,
                installment=installment
            ).first()

            if existing_payment:
                if existing_payment.amount_remaining == 0:
                    return JsonResponse({
                        'status': False,
                        'message': f'The current installment has no outstanding amount. Please pay {amount_paid} towards the next installment.'
                    })
                else:
                    existing_payment.amount_paid += min(total_paid, installment.amount_required)
                    existing_payment.date_paid = date_paid
                    existing_payment.amount_remaining = max(installment.amount_required - existing_payment.amount_paid, 0)
                    existing_payment.balance = max(existing_payment.amount_paid - installment.amount_required, 0)
                    existing_payment.payment_status = 'Completed' if existing_payment.amount_remaining == 0 else 'Incomplete'
                    existing_payment.save()
            else:
                # Create a new payment
                remaining_amount = max(installment.amount_required - total_paid, 0)
                balance = max(total_paid - installment.amount_required, 0)
                payment = SchoolFeesPayment(
                    student=student,
                    installment=installment,
                    amount_paid=min(total_paid, installment.amount_required),
                    date_paid=date_paid,
                    amount_remaining=remaining_amount,
                    balance=balance,
                    payment_status='Completed' if remaining_amount == 0 else 'Incomplete'
                )
                payment.save()

            return JsonResponse({'status': True, 'message': 'Payment added successfully'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request'})


@csrf_exempt
def update_payment(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('payment_id')
            amount_paid = Decimal(request.POST.get('amount_paid'))  # Convert to Decimal
            date_paid = request.POST.get('date_paid')

            payment = SchoolFeesPayment.objects.get(id=payment_id)
            student = payment.student

            # Find the correct installment for the payment date
            installment = SchoolFeesInstallment.objects.filter(
                school_class=student.current_class,
                start_date__lte=date_paid,
                end_date__gte=date_paid
            ).first()

            if not installment:
                return JsonResponse({'status': False, 'message': 'No installment found for the given date'})

            # Fetch all previous payments for the student, ordered by date
            previous_payments = SchoolFeesPayment.objects.filter(student=student).exclude(id=payment_id).order_by('date_paid')

            total_paid = amount_paid

            # Iterate over previous payments to clear any remaining amount and balance
            for prev_payment in previous_payments:
                if prev_payment:
                    if prev_payment.amount_remaining > 0:
                        if total_paid >= prev_payment.amount_remaining:
                            total_paid -= prev_payment.amount_remaining
                            prev_payment.amount_paid += prev_payment.amount_remaining
                            prev_payment.amount_remaining = Decimal('0.00')  # Convert to Decimal
                            prev_payment.payment_status = 'Completed'
                        else:
                            prev_payment.amount_remaining -= total_paid
                            prev_payment.amount_paid += total_paid
                            total_paid = Decimal('0.00')  # Convert to Decimal
                            prev_payment.payment_status = 'Incomplete'
                        prev_payment.balance = max(prev_payment.amount_paid - prev_payment.installment.amount_required, Decimal('0.00'))  # Convert to Decimal
                        prev_payment.save()
                    elif prev_payment.balance > Decimal('0.00'):  # Convert to Decimal
                        total_paid += prev_payment.balance
                        prev_payment.balance = Decimal('0.00')  # Convert to Decimal
                        prev_payment.save()

            # Update the selected payment
            payment.amount_paid = total_paid
            payment.date_paid = date_paid
            payment.amount_remaining = max(installment.amount_required - amount_paid, Decimal('0.00'))  # Convert to Decimal
            payment.balance = max(payment.amount_paid - installment.amount_required, Decimal('0.00'))  # Convert to Decimal
            payment.payment_status = 'Completed' if payment.amount_remaining == Decimal('0.00') else 'Incomplete'  # Convert to Decimal
            payment.amount_paid = min(total_paid, installment.amount_required)
            payment.save()

            return JsonResponse({'status': True, 'message': 'Payment updated successfully'})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Invalid request'})



@login_required
def filter_payments(request):
    installments  = SchoolFeesInstallment.objects.all()   
    return render(request, "accountant_template/filter_payments.html",{"installments":installments}) 

def search_payments(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Extract form data
        selected_class = request.POST.get('selected_class')
        installment_id = request.POST.get('installment_id')
        payment_status = request.POST.get('payment_status')
        
        # Fetch all students of the selected class
        students = Students.objects.filter(current_class=selected_class)
        
        # Create a list to store each student's payment results
        student_results = []
        
        # Iterate over each student to fetch their payment details
        for student in students:
            payments = SchoolFeesPayment.objects.filter(
                student=student,
                installment_id=installment_id,
                payment_status=payment_status
            )
            
            # Collect the payment details for each student
            for payment in payments:
                student_results.append({
                    'student_id': student.id,
                    'student_name': student.full_name,
                    'class': student.current_class,
                    'installment': payment.installment.installment_name,
                    'amount_paid': payment.amount_paid,
                    'amount_remaining': payment.amount_remaining,
                    'balance': payment.balance,
                    'payment_status': payment.payment_status,
                    'date_paid': payment.date_paid
                })
        
        # Render the HTML template with the fetched data
        html_result = render_to_string('accountant_template/filter_payments_table.html', {'student_results': student_results})
        
        # Return the HTML result as JSON response
        return JsonResponse({'html_result': html_result})
    
    return JsonResponse({'error': 'Invalid request'})

def view_all_payments(request, student_id):
    payments = SchoolFeesPayment.objects.filter(student__id=student_id)
    student = Students.objects.get(id=student_id)
    return render(request, 'accountant_template/view_all_payments.html', {'payments': payments,"student":student})

def student_receipt(request, student_id):
    payments = SchoolFeesPayment.objects.filter(student__id=student_id)
    student = Students.objects.get(id=student_id)
    return render(request, 'accountant_template/receipt.html', {'payments': payments,"student":student})

def fee_structure_list(request):
    fee_structures = FeeStructure.objects.all()
    return render(request, 'accountant_template/fee_structure_list.html', {'fee_structures': fee_structures})

def add_fee_structure(request, pk=None):
    try:
        if pk:
            fee_structure = get_object_or_404(FeeStructure, pk=pk)
        else:
            fee_structure = None

        if request.method == 'POST':
            form = FeeStructureForm(request.POST, instance=fee_structure)
            if form.is_valid():
                # Ensure unique fee structure per class
                school_class = form.cleaned_data['school_class']
                if FeeStructure.objects.filter(school_class=school_class).exclude(pk=pk).exists():
                    form.add_error('school_class', 'Fee structure for this class already exists.')
                else:
                    form.save()
                    messages.success(request, 'Fee structure saved successfully.')
                    if 'save_and_return' in request.POST:
                        return redirect('accountant_fee_structure_list')
                    elif 'save_and_add_another' in request.POST:
                        return redirect('accountant_add_fee_structure')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = FeeStructureForm(instance=fee_structure)
        
        return render(request, 'accountant_template/add_fee_structure.html', {'form': form, 'fee_structure': fee_structure})
    
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        return render(request, 'accountant_template/add_fee_structure.html', {'form': form, 'fee_structure': fee_structure})

def delete_fee_structure(request, pk):
    try:
        fee_structure = get_object_or_404(FeeStructure, pk=pk)
        if request.method == 'POST':
            fee_structure.delete()
            messages.success(request, 'Fee structure deleted successfully.')
            return redirect('accountant_fee_structure_list')
        
        return render(request, 'accountant_template/confirm_delete_fee_structure.html', {'fee_structure': fee_structure})
    
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        return redirect('accountant_fee_structure_list')
    
@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        try:
            # Get the user's profile
            staff = request.user.staffs
            # Accessing the uploaded picture from the form
            new_picture = request.FILES.get('profile_picture')  
            
            if new_picture:
                # Check if the uploaded file is an image
                if not new_picture.content_type.startswith('image'):
                    raise ValidationError("Invalid image file type. Please upload a valid image.")

                # Check if the file size is within limit (2MB)
                if new_picture.size > 2 * 1024 * 1024:  # 2MB in bytes
                    raise ValidationError("File size exceeds the limit. Please upload a file smaller than 2MB.")               
              
                
                if staff:
                    # Update the profile picture
                    staff.profile_pic = new_picture
                    
                    # Save the changes
                    staff.save()
                    
                    # Redirect to a success page or back to the profile page
                    return render(request, 'accountant_template/update_profile_picture.html')
                else:
                    raise ValidationError("User profile does not exist.")
            else:
                raise ValidationError("No profile picture uploaded.")
        except ValidationError as e:
            # Handle validation errors (e.g., invalid file type or size)
            messages.error(request, str(e))
        except Exception as e:
            # Handle any other unexpected errors
            messages.error(request, str(e))
            # You may want to log this error for debugging purposes
            
    return render(request, 'accountant_template/update_profile_picture.html')