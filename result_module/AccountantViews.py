import datetime
from decimal import Decimal
import json
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum, F
from django.db import models
from django.db.models import Q
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET,require_POST
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from result_module.forms import ClassFeeForm, ExpenditureForm, FeePaymentForm, FeeStructureForm, MadrasatulFeeForm, MadrasatulFeePaymentForm, StudentForm, TransportFeeForm, TransportFeePaymentForm
from result_module.models import (
    ClassFee,
    ClassLevel,
    ExamType,
    Expenditure,
    FeePayment,
    FeeStructure,
    FeedBackStaff,
    LeaveReportStaffs,
    MadrasatulFee,
    MadrasatulFeePayment,
    Result,   
    SchoolFeesInstallment,
    SchoolFeesPayment,
    Service,   
    Staffs,
    StudentClassAttendance,
    Students,
    Subject,
    TransportFee,
    TransportFeePayment,
    )


@login_required
def accountant_home(request):
    # Get the branch of the currently logged-in staff
    staff = request.user.staffs
    staff_branch = staff.branch

    try:
        # Fetch total number of students corresponding to the staff branch
        total_students = Students.objects.filter(branch=staff_branch).count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error fetching total students: {str(e)}"})  
    
    try:
        # Fetch total number of subjects (no branch filtering assumed)
        total_subjects = Subject.objects.count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error fetching total subjects: {str(e)}"})

    try:
        # Fetch total number of female students corresponding to the staff branch
        total_female_students = Students.objects.filter(gender='Female', branch=staff_branch).count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error fetching total female students: {str(e)}"})

    try:
        # Fetch total number of male students corresponding to the staff branch
        total_male_students = Students.objects.filter(gender='Male', branch=staff_branch).count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error fetching total male students: {str(e)}"})

    try:
        # Counting the total number of students corresponding to the staff branch
        students_count = Students.objects.filter(branch=staff_branch).count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error counting total students: {str(e)}"})

    try:
        # Calculating total fees collected corresponding to the staff branch
        total_school_fees = SchoolFeesPayment.objects.filter(student__branch=staff_branch).aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
        total_madrasatul_fees = MadrasatulFeePayment.objects.filter(student__branch=staff_branch).aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
        total_transport_fees = TransportFeePayment.objects.filter(student__branch=staff_branch).aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0
        total_fee_payment = FeePayment.objects.filter(student__branch=staff_branch).aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0

        total_fees_collected = (total_school_fees + total_madrasatul_fees +
                                total_transport_fees + total_fee_payment)
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error calculating total fees collected: {str(e)}"})

    try:
        # Counting pending payments corresponding to the staff branch
        pending_payments_count = SchoolFeesPayment.objects.filter(student__branch=staff_branch, amount_remaining__gt=0).count()
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error counting pending payments: {str(e)}"})

    try:
        # Calculating total expenditure corresponding to the staff branch
        total_expenditure = Expenditure.objects.filter(branch=staff_branch).aggregate(total_spent=Sum('amount'))['total_spent'] or 0
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error calculating total expenditure: {str(e)}"})

    try:
        net_profit = total_fees_collected - total_expenditure
    except Exception as e:
        return render(request, "accountant_template/error.html", {"error_message": f"Error calculating net profit: {str(e)}"})

    return render(request, "accountant_template/accountant_home.html", {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_female_students': total_female_students,
        'total_male_students': total_male_students,
        'student_count': students_count,
        'total_fees_collected': total_fees_collected,
        'pending_payments_count': pending_payments_count,
        'total_expenditure': total_expenditure,
        'net_profit': net_profit,
        'total_school_fees': total_school_fees,
        'total_madrasatul_fees': total_madrasatul_fees,
        'total_transport_fees': total_transport_fees,
        'total_fee_payment': total_fee_payment
    })

@login_required
def get_financial_yearly_data(request):
    if request.method == 'GET' and 'year' in request.GET:
        selected_year = request.GET.get('year')
        try:
            # Get the branch of the currently logged-in staff
            staff = request.user.staffs
            if not staff:
                raise PermissionDenied("Staff information not available.")
            staff_branch = staff.branch
            
            # Fetch fees collected (income) for the selected year and corresponding branch
            fees_collected = SchoolFeesPayment.objects.filter(
                date_paid__year=selected_year,
                student__branch=staff_branch
            ).aggregate(total_fees_collected=models.Sum('amount_paid'))['total_fees_collected'] or 0
           
            # Fetch expenditure for the selected year and corresponding branch
            expenditure = Expenditure.objects.filter(
                date__year=selected_year,
                branch=staff_branch
            ).aggregate(total_expenditure=models.Sum('amount'))['total_expenditure'] or 0

            # Prepare data to return as JSON
            data = {
                'income': fees_collected,
                'expenditure': expenditure,
            }
            return JsonResponse(data)
        except PermissionDenied as e:
            return JsonResponse({'error': str(e)}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle invalid requests or missing parameters
    return JsonResponse({'error': 'Invalid request or year parameter missing'}, status=400)


@login_required
@require_GET
def get_school_fees_monthly_data(request):
    year = request.GET.get('year')
    
    if not year:
        return JsonResponse({'error': 'Year parameter is required'}, status=400)
    
    # Get the branch of the currently logged-in staff
    staff_branch = request.user.staffs.branch    
    # Initialize monthly data dictionary
    monthly_data_dict = {}
    
    # Fetch monthly income data (fees collected) for the selected year and corresponding branch
    fees_collected_data = SchoolFeesPayment.objects.filter(
        date_paid__year=year,
        student__branch=staff_branch
    ).values('date_paid__month').annotate(
        income=Sum('amount_paid')
    ).order_by('date_paid__month')

    # Populate the dictionary with income data
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


@login_required
@require_GET
def get_expenditure_monthly_data(request):
    year = request.GET.get('year')
    
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return JsonResponse({'error': 'Staff member not found'}, status=404)
    
    # Ensure the branch of the staff is considered
    staff_branch = current_staff.branch

    # Initialize monthly data dictionary
    monthly_data_dict = {}
    
    # Fetch monthly expenditure data for the staff's branch
    expenditure_data = Expenditure.objects.filter(
        date__year=year,
        branch=staff_branch  # Filter expenditures by the branch of the current staff
    ).values('date__month').annotate(
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


@login_required
def get_classwise_fee_payment_data(request):
    try:
        # Get the year from request parameters
        year = request.GET.get('year')
        
        # Get the currently logged-in staff member
        current_staff = Staffs.objects.get(admin=request.user)

        # Ensure the branch of the staff is considered
        staff_branch = current_staff.branch

        # Query to count number of distinct students per class who have made payments
        classwise_data = Students.objects.filter(
            schoolfeespayment__date_paid__year=year,
            branch=staff_branch  # Filter students by the branch of the current staff
        ).values('class_level').annotate(
            fee_payments_count=Count('id', distinct=True)
        ).order_by('class_level')

        # Prepare response data
        response_data = []
        for entry in classwise_data:
            response_data.append({
                'class_name': entry['class_level'],
                'fee_payments_count': entry['fee_payments_count'],
            })

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@login_required
def student_list(request):
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return render(request, 'error.html', {'error': 'Staff member not found'})

    # Extract the branch of the staff member
    staff_branch = current_staff.branch

    # Filter students by the branch of the current staff member
    students = Students.objects.filter(branch=staff_branch)

    context = {
        'students': students
    }
    return render(request, 'accountant_template/student_list.html', context)


@login_required
def school_fees_installments_list(request):
    installments = SchoolFeesInstallment.objects.all()
    class_levels = ClassLevel.objects.all()
    context = {
        'installments': installments,
        'class_levels': class_levels
    }
    return render(request, 'accountant_template/school_fees_installments_list.html', context)


@login_required
def fees_collected(request):
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return render(request, 'error.html', {'error': 'Staff member not found'})

    # Extract the branch of the staff member
    staff_branch = current_staff.branch

    # Filter SchoolFeesPayment by the staff's branch
    total_fees_collected = SchoolFeesPayment.objects.filter(
        student__branch=staff_branch
    ).aggregate(total_collected=Sum('amount_paid'))['total_collected'] or 0

    installments = SchoolFeesPayment.objects.filter(
        amount_remaining=0,
        student__branch=staff_branch
    )

    context = {
        'installments': installments,
        'total_fees_collected': total_fees_collected
    }
    return render(request, 'accountant_template/fees_collected.html', context)


@login_required
def pending_payments(request):
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return render(request, 'error.html', {'error': 'Staff member not found'})

    # Extract the branch of the staff member
    staff_branch = current_staff.branch

    # Filter pending payments by the staff's branch
    pending_payments = SchoolFeesPayment.objects.filter(
        payment_status='Incomplete',
        student__branch=staff_branch
    )

    context = {
        'pending_payments': pending_payments
    }
    return render(request, 'accountant_template/pending_payments.html', context)


@login_required
def expenditure_list(request):
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return render(request, 'error.html', {'error': 'Staff member not found'})

    # Extract the branch of the staff member
    staff_branch = current_staff.branch

    # Filter expenditures by the staff's branch
    expenditures = Expenditure.objects.filter(
        branch=staff_branch
    )
    total_expenditure = expenditures.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenditures': expenditures,
        'total_expenditure': total_expenditure
    }
    return render(request, 'accountant_template/expenditure.html', context)


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
        class_level_id = request.POST.get('class_level')
        
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
                    class_level_id=class_level_id,
                ).exists():
                    return JsonResponse({'status': False, 'message': 'Another installment with the same name already exists.'})        

                installment = SchoolFeesInstallment.objects.get(pk=installment_id)
                installment.installment_name = installment_name
                installment.amount_required = amount_required
                installment.start_date = start_date
                installment.end_date = end_date
                installment.class_level_id = class_level_id
                installment.save()
                return JsonResponse({'status': True, 'message': 'Installment updated successfully!'})
            else:
                 # Check if the school class already has three installments
                if SchoolFeesInstallment.objects.filter(class_level_id=class_level_id).count() >= 3:
                    return JsonResponse({'status': False, 'message': 'Each school class can have only three installments.'})

                # Adding new installment              
                previous_installment_end_date = SchoolFeesInstallment.objects.filter(
                    class_level_id=class_level_id
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
                    class_level_id=class_level_id
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

@login_required
def payment_list(request):
    # Get the currently logged-in staff member
    try:
        current_staff = Staffs.objects.get(admin=request.user)
    except Staffs.DoesNotExist:
        return render(request, 'error.html', {'error': 'Staff member not found'})

    # Extract the branch of the staff member
    staff_branch = current_staff.branch

    # Filter payments by the staff's branch
    payments = SchoolFeesPayment.objects.filter(
        student__branch=staff_branch
    ).select_related('student', 'installment')

    # Filter students by the staff's branch
    students = Students.objects.filter(
        branch=staff_branch
    )

    return render(request, 'accountant_template/payment_list.html', {
        'payments': payments,
        'students': students
    })


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
                class_level=student.class_level,
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
                class_level=student.class_level,
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
    class_levels = ClassLevel.objects.all()  
    return render(request, "accountant_template/filter_payments.html",{"installments":installments,"class_levels":class_levels}) 

@login_required
def search_payments(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Extract form data
        class_level_id = request.POST.get('class_level')
        installment_id = request.POST.get('installment_id')
        payment_status = request.POST.get('payment_status')
        
        # Retrieve the current staff member and branch
        try:
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            return JsonResponse({'error': 'Staff member not found'})

        try:
            # Get class level object
            class_level = ClassLevel.objects.get(id=class_level_id)
        except ClassLevel.DoesNotExist:
            return JsonResponse({'error': 'Invalid class level selected'})

        # Fetch students of the selected class and branch
        students = Students.objects.filter(class_level_id=class_level, branch=staff_branch)

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
                    'class': student.class_level,
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

@login_required
def student_payment_fetch(request):    
    class_levels = ClassLevel.objects.all()
    return render(request, "accountant_template/student_payment_fetch.html",{"class_levels":class_levels}) 

@login_required
def payment_fetch(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Extract form data
        class_level_id = request.POST.get('class_level')
        service = request.POST.get('services')
        payment_status = request.POST.get('payment_status')

        # Retrieve the current staff member and branch
        try:
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            return JsonResponse({'error': 'Staff member not found'})

        # Get class level object
        try:
            class_level = ClassLevel.objects.get(id=class_level_id)
        except ClassLevel.DoesNotExist:
            return JsonResponse({'error': 'Invalid class level selected'})

        # Fetch students of the selected class and branch
        students = Students.objects.filter(class_level=class_level, branch=staff_branch)

        # Initialize student_results list
        student_results = []

        # Determine which payment model and template to use based on the selected service
        if service == 'Madrasa':
            payments_model = MadrasatulFeePayment
            template_name = 'accountant_template/payment_fetch_madrasa_table.html'
            for student in students:
                payments = payments_model.objects.filter(
                    student=student,
                    payment_status=payment_status
                )
                for payment in payments:
                    student_results.append({
                        'student_name': student.full_name,
                        'class': student.class_level,
                        'amount_paid': payment.amount_paid,
                        'amount_remaining': payment.amount_remaining,
                        'payment_status': payment.payment_status,
                        'date_paid': payment.payment_date
                    })
        
        elif service == 'Transport':
            payments_model = TransportFeePayment
            template_name = 'accountant_template/payment_fetch_transport_table.html'
            for student in students:
                payments = payments_model.objects.filter(
                    student=student,
                    payment_status=payment_status
                )
                for payment in payments:
                    student_results.append({
                        'student_name': student.full_name,
                        'class': student.class_level,
                        'amount_paid': payment.amount_paid,
                        'amount_remaining': payment.amount_remaining,
                        'payment_status': payment.payment_status,
                        'date_paid': payment.payment_date
                    })

        elif service in ['Registration', 'Boarding']:
            payments_model = FeePayment
            template_name = 'accountant_template/payment_fetch_registration_boarding_table.html'
            
            for student in students:
                # Filter ClassFee based on the service type
                fee_type = 'Registration' if service == 'Registration' else 'Boarding'
                class_fees = ClassFee.objects.filter(
                    class_level=student.class_level,
                    fee_type=fee_type
                )
                
                for class_fee in class_fees:
                    payments = payments_model.objects.filter(
                        student=student,
                        class_fee=class_fee,
                        payment_status=payment_status
                    )
                    for payment in payments:
                        student_results.append({
                            'student_name': student.full_name,
                            'class': student.class_level,
                            'fee_type': class_fee.fee_type,
                            'amount_paid': payment.amount_paid,
                            'amount_remaining': payment.amount_remaining,
                            'payment_status': payment.payment_status,
                            'date_paid': payment.payment_date
                        })

        else:
            return JsonResponse({'error': 'Invalid service selected'})

        # Render the HTML template with the fetched data
        html_result = render_to_string(template_name, {'student_results': student_results})

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
                class_level = form.cleaned_data['class_level']
                if FeeStructure.objects.filter(class_level=class_level).exclude(pk=pk).exists():
                    form.add_error('class_level', 'Fee structure for this class already exists.')
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


@method_decorator(login_required, name='dispatch')
class FeeStructureListView(ListView):
    model = FeeStructure
    template_name = 'accountant_template/school_fees_structure_list.html'
    context_object_name = 'fee_structures'
    paginate_by = 20  # Optional: If you want to paginate the results

    def get_queryset(self):
        # Retrieve the current staff member and branch
        try:
            current_staff = Staffs.objects.get(admin=self.request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            staff_branch = None

        # Return filtered queryset based on the staff's branch
        if staff_branch:
            return FeeStructure.objects.filter(branch=staff_branch)
        else:
            return FeeStructure.objects.none()  # Return no results if staff member is not found
    
class FeeStructureDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        class_level = get_object_or_404(FeeStructure, pk=pk)
        class_level.delete()
        return redirect('accountant_fee_structure_list')       
    
class FeeStructureCreateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            fee_structure = get_object_or_404(FeeStructure, pk=pk)
            form = FeeStructureForm(instance=fee_structure)
        else:
            form = FeeStructureForm()

        return render(request, 'accountant_template/add_fee_structure_form.html', {'form': form})

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            fee_structure = get_object_or_404(FeeStructure, pk=pk)
            form = FeeStructureForm(request.POST, instance=fee_structure)
        else:
            form = FeeStructureForm(request.POST)

        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('accountant_fee_structure_list')
            elif action == 'save_and_continue':
                return redirect('accountant_fee_structure_create')

        return render(request, 'accountant_template/add_fee_structure_form.html', {'form': form})   
    
    
@method_decorator(login_required, name='dispatch')
class ExpenditureListView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the current staff member and their branch
        try:
            current_staff = Staffs.objects.get(admin=self.request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            staff_branch = None

        # Filter expenditures by the staff's branch
        if staff_branch:
            expenditures = Expenditure.objects.filter(branch=staff_branch)
        else:
            expenditures = Expenditure.objects.none()  # Return no results if staff member is not found

        return render(request, 'accountant_template/expenditure_list.html', {'expenditures': expenditures})
    
class ExpenditureDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        expenditure = get_object_or_404(Expenditure, pk=pk)
        expenditure.delete()
        return redirect('accountant_expenditure_list')       
    
class ExpenditureCreateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            expenditure = get_object_or_404(Expenditure, pk=pk)
            form = ExpenditureForm(instance=expenditure)
        else:
            form = ExpenditureForm()

        return render(request, 'accountant_template/add_expenditure_form.html', {'form': form})

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            expenditure = get_object_or_404(Expenditure, pk=pk)
            form = ExpenditureForm(request.POST, instance=expenditure)
        else:
            form = ExpenditureForm(request.POST)

        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('accountant_expenditure_list')  # Adjust the redirect to match your URL name
            elif action == 'save_and_continue':
                return redirect('accountant_add_expenditure')  # Adjust the redirect to match your URL name

        return render(request, 'accountant_template/add_expenditure_form.html', {'form': form}) 
    
    
class ClassFeeListView(ListView):
    model = ClassFee
    template_name = 'accountant_template/class_fee_list.html'
    context_object_name = 'class_fees'
    paginate_by = 10  # Adjust the number of items per page if needed

    def get_queryset(self):
        return ClassFee.objects.all().order_by('class_level', 'fee_type')
    
class ClassFeeDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        class_fee = get_object_or_404(ClassFee, pk=pk)
        class_fee.delete()
        return redirect('accountant_class_fee_list')      
        
class ClassFeeCreateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            class_fee = get_object_or_404(ClassFee, pk=pk)
            form = ClassFeeForm(instance=class_fee)
        else:
            form = ClassFeeForm()

        return render(request, 'accountant_template/add_class_fee_form.html', {'form': form})

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            class_fee = get_object_or_404(ClassFee, pk=pk)
            form = ClassFeeForm(request.POST, instance=class_fee)
        else:
            form = ClassFeeForm(request.POST)

        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('accountant_class_fee_list')  # Adjust the redirect to match your URL name
            elif action == 'save_and_continue':
                return redirect('accountant_add_class_fee')  # Adjust the redirect to match your URL name

        return render(request, 'accountant_template/add_class_fee_form.html', {'form': form})    
    


class MadrasatulFeeListView(ListView):
    model = MadrasatulFee
    template_name = 'accountant_template/madrasatul_fee_list.html'
    context_object_name = 'fees'
    paginate_by = 10  # Optional: to paginate the list if you have many records

    def get_queryset(self):
        return MadrasatulFee.objects.select_related('class_level').order_by('class_level', 'fee_amount')
    
class MadrasatulFeeDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        class_fee = get_object_or_404(MadrasatulFee, pk=pk)
        class_fee.delete()
        return redirect('accountant_madrasatul_fee_list')        
    
class MadrasatulFeeCreateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            fee = get_object_or_404(MadrasatulFee, pk=pk)
            form = MadrasatulFeeForm(instance=fee)
        else:
            form = MadrasatulFeeForm()

        return render(request, 'accountant_template/add_madrasatul_fee_form.html', {'form': form})

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            fee = get_object_or_404(MadrasatulFee, pk=pk)
            form = MadrasatulFeeForm(request.POST, instance=fee)
        else:
            form = MadrasatulFeeForm(request.POST)

        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                messages.success(request, 'Madrasatul Fee saved successfully!')
                return redirect('accountant_madrasatul_fee_list')
            elif action == 'save_and_continue':
                messages.success(request, 'Madrasatul Fee saved successfully! You can add another fee.')
                return redirect('accountant_madrasatul_fee_create')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'accountant_template/add_madrasatul_fee_form.html', {'form': form})    
    
    
class TransportFeeListView(ListView):
    model = TransportFee
    template_name = 'accountant_template/transport_fee_list.html'
    context_object_name = 'transport_fees'
    paginate_by = 10  # Optional: to paginate the list if you have many records


    
class TransportFeeDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        class_fee = get_object_or_404(TransportFee, pk=pk)
        class_fee.delete()
        return redirect('accountant_transport_fee_list')          


class TransportFeeCreateUpdateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            transport_fee = get_object_or_404(TransportFee, pk=pk)
            form = TransportFeeForm(instance=transport_fee)
            context = {
                'form': form,
                'is_edit': True
            }
        else:
            form = TransportFeeForm()
            context = {
                'form': form,
                'is_edit': False
            }
        return render(request, 'accountant_template/add_transport_fee_form.html', context)
    
    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            transport_fee = get_object_or_404(TransportFee, pk=pk)
            form = TransportFeeForm(request.POST, instance=transport_fee)
        else:
            form = TransportFeeForm(request.POST)

        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                messages.success(request, 'Transport Fee has been saved successfully!')
                return redirect('accountant_transport_fee_list')
            elif action == 'save_and_continue':
                messages.success(request, 'Transport Fee has been saved! You can add another one.')
                return redirect('accountant_transport_fee_create')

        context = {
            'form': form,
            'is_edit': pk is not None
        }
        return render(request, 'accountant_template/add_transport_fee_form.html', context)
    

@method_decorator(login_required, name='dispatch')
class FeePaymentListView(ListView):
    model = FeePayment
    template_name = 'accountant_template/fee_payment_list.html'
    context_object_name = 'fee_payments'
    paginate_by = 10  # Adjust the number of items per page if needed

    def get_queryset(self):
        # Retrieve the current staff member and their branch
        try:
            current_staff = Staffs.objects.get(admin=self.request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            staff_branch = None

        # Filter FeePayment based on the branch of the student's branch
        if staff_branch:
            return FeePayment.objects.filter(
                student__branch=staff_branch
            ).select_related('student', 'class_fee').order_by('-payment_date')
        else:
            return FeePayment.objects.none()  # Return no results if staff member is not found
    

class FeePaymentDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        fee_payment = get_object_or_404(FeePayment, pk=pk)
        fee_payment.delete()
        return redirect('accountant_fee_payment_list')  
            
  
@method_decorator(login_required, name='dispatch')    
class FeePaymentCreateUpdateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page

        # Get students from the branch of the current staff
        branch_students = Students.objects.filter(branch=staff_branch)

        if pk:
            fee_payment = get_object_or_404(FeePayment, pk=pk)
            form = FeePaymentForm(instance=fee_payment, branch_students=branch_students)
            context = {
                'form': form,
                'is_edit': True
            }
        else:
            form = FeePaymentForm(branch_students=branch_students)
            context = {
                'form': form,
                'is_edit': False
            }
        
        return render(request, 'accountant_template/add_fee_payment_form.html', context)

    def post(self, request, pk=None, *args, **kwargs):
        try:
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page

        # Get students from the branch of the current staff
        branch_students = Students.objects.filter(branch=staff_branch)

        if pk:
            fee_payment = get_object_or_404(FeePayment, pk=pk)
            form = FeePaymentForm(request.POST, instance=fee_payment, branch_students=branch_students)
        else:
            form = FeePaymentForm(request.POST, branch_students=branch_students)

        if form.is_valid():
            fee_payment = form.save()
            action = request.POST.get('action')
            if action == 'save':
                messages.success(request, 'Fee Payment has been saved successfully!')
                return redirect('accountant_fee_payment_list')
            elif action == 'save_and_continue':
                messages.success(request, 'Fee Payment has been saved! You can add another one.')
                return redirect('accountant_fee_payment_create')

        context = {
            'form': form,
            'is_edit': pk is not None
        }
        return render(request, 'accountant_template/add_fee_payment_form.html', context)
    

@method_decorator(login_required, name='dispatch')
class MadrasatulFeePaymentCreateUpdateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            # Get the 'Madrasatul' service
            madrasatul_service = Service.objects.get(name='Madrasa')
            branch_students = Students.objects.filter(branch=request.user.staffs.branch, services=madrasatul_service)
            
            if pk:
                madrasatul_fee_payment = get_object_or_404(MadrasatulFeePayment, pk=pk)
                form = MadrasatulFeePaymentForm(instance=madrasatul_fee_payment, branch_students=branch_students)
                context = {
                    'form': form,
                    'is_edit': True
                }
            else:
                form = MadrasatulFeePaymentForm(branch_students=branch_students)
                context = {
                    'form': form,
                    'is_edit': False
                }
        except Service.DoesNotExist:
            messages.error(request, 'The specified service does not exist.')
            return redirect('accountant_madrasatul_fee_payment_list')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('accountant_madrasatul_fee_payment_list')

        return render(request, 'accountant_template/add_madrasatul_fee_payment_form.html', context)
    
    def post(self, request, pk=None, *args, **kwargs):
        try:
            # Get the 'Madrasatul' service
            madrasatul_service = Service.objects.get(name='Madrasa')
            branch_students = Students.objects.filter(branch=request.user.staffs.branch, services=madrasatul_service)
            
            if pk:
                madrasatul_fee_payment = get_object_or_404(MadrasatulFeePayment, pk=pk)
                form = MadrasatulFeePaymentForm(request.POST, instance=madrasatul_fee_payment, branch_students=branch_students)
            else:
                form = MadrasatulFeePaymentForm(request.POST, branch_students=branch_students)

            if form.is_valid():
                fee_payment = form.save()
                action = request.POST.get('action')
                if action == 'save':
                    messages.success(request, 'Madrasatul Fee Payment has been saved successfully!')
                    return redirect('accountant_madrasatul_fee_payment_list')
                elif action == 'save_and_continue':
                    messages.success(request, 'Madrasatul Fee Payment has been saved! You can add another one.')
                    return redirect('accountant_madrasatul_fee_payment_create')
            
        except Service.DoesNotExist:
            messages.error(request, 'The specified service does not exist.')
            return redirect('accountant_madrasatul_fee_payment_list')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('accountant_madrasatul_fee_payment_list')

        context = {
            'form': form,
            'is_edit': pk is not None
        }
        return render(request, 'accountant_template/add_madrasatul_fee_payment_form.html', context)
    

@method_decorator(login_required, name='dispatch')
class MadrasatulFeePaymentListView(ListView):
    model = MadrasatulFeePayment
    template_name = 'accountant_template/madrasatul_fee_payment_list.html'
    context_object_name = 'fee_payments'
    paginate_by = 10  # Optional: to paginate the list view

    def get_queryset(self):
        # Retrieve the current staff member and their branch
        try:
            current_staff = Staffs.objects.get(admin=self.request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            staff_branch = None

        # Filter MadrasatulFeePayment based on the branch of the student's branch
        if staff_branch:
            return MadrasatulFeePayment.objects.filter(
                student__branch=staff_branch
            ).select_related('student').order_by('-payment_date')
        else:
            return MadrasatulFeePayment.objects.none()  # Return no results if staff member is not found
    
  
    
class MadrasatulFeePaymentDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        fee_payment = get_object_or_404(MadrasatulFeePayment, pk=pk)
        fee_payment.delete()
        return redirect('accountant_madrasatul_fee_payment_list')               

@method_decorator(login_required, name='dispatch')
class TransportFeePaymentCreateUpdateView(View):
    def get(self, request, pk=None, *args, **kwargs):
        try:
            # Retrieve the current staff member and their branch
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch

            # Get the 'Transport' service
            transport_service = Service.objects.get(name='Transport')
            
            # Get students from the branch of the current staff who are enrolled in the 'Transport' service
            branch_students = Students.objects.filter(branch=staff_branch, services=transport_service)

            if pk:
                transport_fee_payment = get_object_or_404(TransportFeePayment, pk=pk)
                form = TransportFeePaymentForm(instance=transport_fee_payment, branch_students=branch_students)
                context = {
                    'form': form,
                    'is_edit': True
                }
            else:
                form = TransportFeePaymentForm(branch_students=branch_students)
                context = {
                    'form': form,
                    'is_edit': False
                }
            
            return render(request, 'accountant_template/add_transport_fee_payment_form.html', context)

        except Staffs.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page
        except Service.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page
        except Exception as e:
            # Handle any other exceptions
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('accountant_error_page')  # Replace with an appropriate error page

    def post(self, request, pk=None, *args, **kwargs):
        try:
            # Retrieve the current staff member and their branch
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch

            # Get the 'Transport' service
            transport_service = Service.objects.get(name='Transport')
            
            # Get students from the branch of the current staff who are enrolled in the 'Transport' service
            branch_students = Students.objects.filter(branch=staff_branch, services=transport_service)

            if pk:
                transport_fee_payment = get_object_or_404(TransportFeePayment, pk=pk)
                form = TransportFeePaymentForm(request.POST, instance=transport_fee_payment, branch_students=branch_students)
            else:
                form = TransportFeePaymentForm(request.POST, branch_students=branch_students)

            if form.is_valid():
                transport_fee_payment = form.save()
                action = request.POST.get('action')
                if action == 'save':
                    messages.success(request, 'Transport Fee Payment has been saved successfully!')
                    return redirect('accountant_transport_fee_payment_list')
                elif action == 'save_and_continue':
                    messages.success(request, 'Transport Fee Payment has been saved! You can add another one.')
                    return redirect('accountant_transport_fee_payment_create')

            context = {
                'form': form,
                'is_edit': pk is not None
            }
            return render(request, 'accountant_template/add_transport_fee_payment_form.html', context)
        
        except Staffs.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page
        except Service.DoesNotExist:
            return redirect('accountant_error_page')  # Replace with an appropriate error page
        except Exception as e:
            # Handle any other exceptions
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('accountant_error_page')  # Replace with an appropriate error page
        

class ErrorPageView(TemplateView):
    template_name = 'accountant_template/accountant_error_page.html'        
    
@method_decorator(login_required, name='dispatch')
class TransportFeePaymentListView(ListView):
    model = TransportFeePayment
    template_name = 'accountant_template/transport_fee_payment_list.html'
    context_object_name = 'transport_fee_payments'
    paginate_by = 10  # Optional: to paginate the list view

    def get_queryset(self):
        # Retrieve the current staff member and their branch
        try:
            current_staff = Staffs.objects.get(admin=self.request.user)
            staff_branch = current_staff.branch
        except Staffs.DoesNotExist:
            staff_branch = None

        # Filter TransportFeePayment based on the branch of the student's branch
        if staff_branch:
            return TransportFeePayment.objects.filter(
                student__branch=staff_branch
            ).select_related('student').order_by('-payment_date')
        else:
            return TransportFeePayment.objects.none()  # Return no results if staff member is not found    
    
class TransportFeePaymentDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        fee_payment = get_object_or_404(TransportFeePayment, pk=pk)
        fee_payment.delete()
        return redirect('accountant_transport_fee_payment_list')   
    
def get_subject_count_per_class_level(request):
    data = Subject.objects.values('class_level__class_name').annotate(subject_count=models.Count('id'))
    return JsonResponse(list(data), safe=False)  

def fetch_students_per_class(request):
    # Get the total number of students for each class level
    class_levels = Students.objects.values('class_level__class_name').annotate(total_students=Count('id'))
    
    # Prepare data for JSON response
    labels = [item['class_level__class_name'] for item in class_levels]
    data = [item['total_students'] for item in class_levels]
    
    return JsonResponse({
        'labels': labels,
        'data': data
    })    
             
             
@require_GET
def get_madrasatul_fee_payment_monthly_data(request):
    year = request.GET.get('year')

    # Initialize monthly data dictionary
    monthly_data_dict = {month: {'income': 0} for month in range(1, 13)}

    # Retrieve the current staff member and their branch
    try:
        current_staff = Staffs.objects.get(admin=request.user)
        staff_branch = current_staff.branch
    except Staffs.DoesNotExist:
        return JsonResponse({'error': 'Staff member not found'})

    # Fetch monthly income data from MadrasatulFeePayment
    madrasatul_fee_payment_data = MadrasatulFeePayment.objects.filter(
        payment_date__year=year,
        student__branch=staff_branch
    ).values('payment_date__month').annotate(
        income=Sum('amount_paid')
    ).order_by('payment_date__month')

    # Combine all data into the monthly_data_dict
    for entry in madrasatul_fee_payment_data:
        month = entry['payment_date__month']
        monthly_data_dict[month]['income'] += entry['income']

    # Prepare response data
    response_data = [{'month': month, 'income': monthly_data_dict[month]['income']} for month in range(1, 13)]

    return JsonResponse(response_data, safe=False)


@require_GET
def get_transport_fee_payment_monthly_data(request):
    year = request.GET.get('year')

    # Initialize monthly data dictionary
    monthly_data_dict = {month: {'income': 0} for month in range(1, 13)}

    # Retrieve the current staff member and their branch
    try:
        current_staff = Staffs.objects.get(admin=request.user)
        staff_branch = current_staff.branch
    except Staffs.DoesNotExist:
        return JsonResponse({'error': 'Staff member not found'})

    # Fetch monthly income data from TransportFeePayment
    transport_fee_payment_data = TransportFeePayment.objects.filter(
        payment_date__year=year,
        student__branch=staff_branch
    ).values('payment_date__month').annotate(
        income=Sum('amount_paid')
    ).order_by('payment_date__month')

    # Combine all data into the monthly_data_dict
    for entry in transport_fee_payment_data:
        month = entry['payment_date__month']
        monthly_data_dict[month]['income'] += entry['income']

    # Prepare response data
    response_data = [{'month': month, 'income': monthly_data_dict[month]['income']} for month in range(1, 13)]

    return JsonResponse(response_data, safe=False)


@require_GET
def get_fee_payment_monthly_data(request):
    year = request.GET.get('year')

    # Initialize monthly data dictionary
    monthly_data_dict = {month: {'income': 0} for month in range(1, 13)}

    # Retrieve the current staff member and their branch
    try:
        current_staff = Staffs.objects.get(admin=request.user)
        staff_branch = current_staff.branch
    except Staffs.DoesNotExist:
        return JsonResponse({'error': 'Staff member not found'})

    # Fetch monthly income data from FeePayment
    fee_payment_data = FeePayment.objects.filter(
        payment_date__year=year,
        student__branch=staff_branch
    ).values('payment_date__month').annotate(
        income=Sum('amount_paid')
    ).order_by('payment_date__month')

    # Combine all data into the monthly_data_dict
    for entry in fee_payment_data:
        month = entry['payment_date__month']
        monthly_data_dict[month]['income'] += entry['income']

    # Prepare response data
    response_data = [{'month': month, 'income': monthly_data_dict[month]['income']} for month in range(1, 13)]

    return JsonResponse(response_data, safe=False)


@login_required
def student_subject_wise_result_page(request,student_id): 
    student = Students.objects.get(id=student_id)
    exam_types = ExamType.objects.all()
    distinct_dates= Result.objects.order_by('date_of_exam').values_list('date_of_exam', flat=True).distinct()
    print(distinct_dates)
    return render(request, 'accountant_template/subject_wise_results.html',
                  {
                      'student': student,
                      'exam_types': exam_types,
                      'distinct_dates': distinct_dates,
                   })
    
@login_required
def student_general_attendance(request, student_id):
    try:
        if student_id:
            student_object = Students.objects.get(id=student_id)
        else:
            # Redirect to the student login page if not logged in
            return render(request, "accountant_template/student_general_attendance.html")

        # Retrieve attendance data for the student


        class_attendance_present = StudentClassAttendance.objects.filter(student=student_object, status=True).count()
        class_attendance_absent = StudentClassAttendance.objects.filter(student=student_object, status=False).count()
        class_attendance_total = StudentClassAttendance.objects.filter(student=student_object).count()      
      
        total_subjects_taken = Subject.objects.all().count()

       

        # Pass data to the template for rendering
        return render(
            request,
            "accountant_template/student_general_attendance.html",
            {
              
                "class_attendance_present": class_attendance_present,
                "class_attendance_absent": class_attendance_absent,
                "class_attendance_total": class_attendance_total,
                "total_subjects_taken": total_subjects_taken,
                                 
                "student": student_object,  # Renamed 'students' to 'student'
            },
        )

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist.")
        return render(request, "accountant_template/student_general_attendance.html")

    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return render(request, "accountant_template/student_general_attendance.html")    
    
def student_details(request, id):
    student = get_object_or_404(Students, id=id)
    return render(request, 'accountant_template/student_details.html', {'student': student})    

def add_or_edit_student(request, pk=None):
    if pk:
        student = get_object_or_404(Students, pk=pk)
    else:
        student = Students()

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save':
                return redirect('accountant_manage_student')
            elif action == 'save_and_continue':
                return redirect('accountant_add_student')
    else:
        form = StudentForm(instance=student)

    return render(request, 'accountant_template/add_student.html', {'form': form, 'student': student})


@login_required
def manage_student(request):
    # Get the branch of the currently logged-in staff
    staff = request.user.staffs
    current_branch = staff.branch

    # Fetch students corresponding to the branch of the logged-in staff
    students = Students.objects.filter(branch=current_branch)
    
    # Fetch all exam types
    exam_types = ExamType.objects.all()

    # Render the template with the filtered students and exam types
    return render(request, 'accountant_template/manage_student.html', {
        'students': students,
        'exam_types': exam_types,
    })
    
    
def update_student_status(request):
    try:
        if request.method == 'POST':
            # Get the user_id and is_active values from POST data
            user_id = request.POST.get('user_id')
            is_active = request.POST.get('is_active')

            # Retrieve the staff object or return a 404 response if not found
            student = get_object_or_404(Students, id=user_id)

            # Toggle the is_active status based on the received value
            if is_active == '1':
                student.is_active = False
            elif is_active == '0':
                student.is_active = True
            else:
                messages.error(request, 'Invalid request')
                return JsonResponse("Invalid request") # Make sure 'manage_staffs' is the name of your staff list URL

            student.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid request method')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    # Redirect back to the staff list page
    return redirect('accountant_manage_student')  # Make sure 'manage_staffs' is the name of your staff list URL   

 