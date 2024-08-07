from datetime import datetime
import json
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.serializers import serialize
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from result_module.models import (

    ClassAttendance,   
    ExamMetrics,  
    FeedBackStaff,
    LeaveReportStaffs,   
    Staffs,
    StudentClassAttendance,
    StudentExamInfo,
    StudentPositionInfo, 
    Students, 
    Subject,
    ExamType,
    Result,
    SujbectWiseResults
    )


@login_required
def student_general_attendance(request, student_id):
    try:
        if student_id:
            student_object = Students.objects.get(id=student_id)
        else:
            # Redirect to the student login page if not logged in
            return render(request, "staff_template/student_general_attendance.html")

        # Retrieve attendance data for the student   

        class_attendance_present = StudentClassAttendance.objects.filter(student=student_object, status=True).count()
        class_attendance_absent = StudentClassAttendance.objects.filter(student=student_object, status=False).count()
        class_attendance_total = StudentClassAttendance.objects.filter(student=student_object).count()

        # Get subject-related data
        subject_data = Subject.objects.all()
        subject_name = []
        data_present = []
        data_absent = []
        total_subjects_taken = Subject.objects.all().count()

       

        # Pass data to the template for rendering
        return render(
            request,
            "staff_template/student_general_attendance.html",
            {
            
                "class_attendance_present": class_attendance_present,
                "class_attendance_absent": class_attendance_absent,
                "class_attendance_total": class_attendance_total,
                "total_subjects_taken": total_subjects_taken,
                "subject_name": subject_name,
                "data_present": data_present,
                "data_absent": data_absent,         
                "student": student_object,  # Renamed 'students' to 'student'
            },
        )

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist.")
        return render(request, "staff_template/student_general_attendance.html")

    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return render(request, "staff_template/student_general_attendance.html")
    
@login_required
def manage_student(request):
    students = Students.objects.all()
    exam_types = ExamType.objects.all()
    return render(request, 'staff_template/manage_student.html', {
        'students': students,
        'exam_types': exam_types,
        })    

@login_required
def staff_home(request):
    if request.user.is_authenticated:
        try:
            staff = Staffs.objects.get(admin=request.user)            
            subjects = staff.subjects.all()
            current_class = staff.current_class
            students_count = Students.objects.filter(current_class=current_class).count()
           
            leave_count = LeaveReportStaffs.objects.filter(staff_id=staff.id, leave_status=1).count()
            subject_count = subjects.count()

            
            return render(request, "staff_template/staff_home.html",
                          {
                "student_count": students_count,               
                "leave_count": leave_count,
                "subject_count": subject_count,         
                "staff": staff,
            })
        except Staffs.DoesNotExist:
            # Handle the case when the staff doesn't exist for the logged-in user
            # You can redirect them to a page or show an error message
            return render(request, "staff_template/error.html")
    else:
        # Redirect the user to the login page
        return redirect("login")  # Replace "login" with the actual URL name of your login page

@login_required    
def staff_take_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)
    # Assuming that the educational level is a ForeignKey in Staffs model
    current_class = staff.current_class
    subjects = staff.subjects.all()   
    class_options = ["Form One", "Form Two", "Form Three", "Form Four"] 
    return render(request, "staff_template/staff_take_attendance.html", {
        "current_class": current_class,      
        "subjects": subjects,      
        "class_options": class_options,
        "staff": staff,
    })

@login_required    
def staff_take_class_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)   
    current_class = staff.current_class
    class_options = ["Form One", "Form Two", "Form Three", "Form Four"] 
    return render(request, "staff_template/staff_take_class_attendance.html", {           
        "current_class": current_class,
        "class_options": class_options,
        "staff": staff,
    })



@csrf_exempt
def get_students(request):
    if request.method == "POST":
        try:
            subject_id = request.POST.get("subject")
            year = request.POST.get("year")
            current_class = request.POST.get("current_class")
            # Check if all required parameters are provided
            if not (year and current_class):
                raise ValueError("Missing required parameters")
            subject = get_object_or_404(Subject, id=subject_id)
            # Get all students associated with the subject, session year, and current class
            students = Students.objects.filter(               
                current_class=current_class,
                updated_at__year=year,
            )
            list_data = []
            for student in students:
                data_small = {
                    "id": student.id,
                    "name": student.full_name  # Assuming this method exists in your Students model
                }
                list_data.append(data_small)

            return JsonResponse(list_data, safe=False)

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Http404:
            return JsonResponse({"error": "Subject or session year not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def staff_fetch_students(request):
    if request.method == "POST":
        try:          
            year = request.POST.get("year")
            current_class = request.POST.get("current_class")
            # Check if all required parameters are provided
            if not (year and current_class):
                raise ValueError("Missing required parameters")         
            students = Students.objects.filter(               
                current_class=current_class,
                updated_at__year=year,
            )
            list_data = []
            for student in students:
                data_small = {
                    "id": student.id,
                    "name": student.full_name  # Assuming this method exists in your Students model
                }
                list_data.append(data_small)
            return JsonResponse(list_data, safe=False)

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Http404:
            return JsonResponse({"error": "Subject or session year not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)
    

    
@csrf_exempt
def staff_save_class_attendance_data(request):
    # Retrieve data from the POST request
    student_ids = request.POST.get("student_ids")
    current_class = request.POST.get("current_class")
    attendance_date = request.POST.get("attendance_date")
    json_students=json.loads(student_ids)
    try:       
         # Check if attendance record already exists for the subject and date
        existing_attendance = ClassAttendance.objects.filter(current_class=current_class, attendance_date=attendance_date).first()
        
        if existing_attendance:
            # Iterate over the JSON data to create attendance reports for each student
            for student_data in json_students:
                student_id = student_data['id']
                status = student_data['status']                
                # Retrieve the student object
                student = Students.objects.get(id=student_id)                
                # Check if attendance report already exists for the student and attendance record
                existing_report = StudentClassAttendance.objects.filter(student_id=student, attendance=existing_attendance).exists()
                
                if not existing_report:
                    # Create attendance report for the student
                    attendance_report = StudentClassAttendance(student=student, attendance=existing_attendance, status=status)
                    attendance_report.save()            
            # Return success response
            return HttpResponse("OK")
        else:
            # Create a new attendance instance
            attendance = ClassAttendance(current_class=current_class, attendance_date=attendance_date)
            attendance.save()

            # Iterate over the JSON data to create attendance reports for each student
            for student_data in json_students:
                student_id = student_data['id']
                status = student_data['status']
                # Retrieve the student object
                student = Students.objects.get(id=student_id)
                # Create attendance report for the student
                attendance_report = StudentClassAttendance(student_id=student, attendance_id=attendance, status=status)
                attendance_report.save()
                
            # Return success response
            return HttpResponse("OK")
    except Exception as e:
        # Print error for troubleshooting
        print("Error saving attendance:", e)
        # Return error response
        return HttpResponse("ERR")
    

@login_required    
def staff_update_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)
    class_options = ["Form One", "Form Two", "Form Three", "Form Four"] 
    subjects = staff.subjects.all()  
    current_class = staff.current_class 
    return render(request, "staff_template/staff_update_attendance.html", {
        "current_class": current_class,       
        "subjects": subjects,       
        "class_options": class_options,
        "staff": staff,
    })

@login_required    
def staff_update_class_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)   
    class_options = ["Form One", "Form Two", "Form Three", "Form Four"] 
    current_class = staff.current_class 
    return render(request, "staff_template/staff_update_class_attendance.html", {           
        "current_class": current_class,
        "class_options": class_options,
        "staff": staff,
    })

@login_required    
def staff_view_class_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)
    attendances=ClassAttendance.objects.all()  
    # Assuming that the educational level is a ForeignKey in Staffs model
    class_levels = staff.current_class 
    return render(request, "staff_template/staff_view_class_attendance.html", {           
        "class_levels": class_levels,
        "staff": staff,
        "attendances": attendances,
    })


 
@csrf_exempt
def staff_get_class_attendance_date(request):
     current_class = request.POST.get("current_class")   
     year = request.POST.get("year")        
     attendance = ClassAttendance.objects.filter(current_class=current_class,updated_at__year=year)
     attendance_obj = []
     
     for attendance_single in attendance:
         data = {
             "id":attendance_single.id,
             "attendance_date":str(attendance_single.attendance_date),   
             "year":year,       
             }
         attendance_obj.append(data)         
     return JsonResponse(json.dumps(attendance_obj),content_type="application/json",safe=False)  
 



@csrf_exempt
def get_class_student_attendance_data(request):  
    date_id = request.POST.get("date") 
    current_class = request.POST.get("current_class")    
    students = Students.objects.filter(current_class=current_class) 
    attendance = ClassAttendance.objects.filter(id=date_id)
    # Fetch attendance data for the given date and class
    attendance_data = StudentClassAttendance.objects.filter(
        attendance__in=attendance,
        student__in=students
    )
    
    # Serialize student data
    list_data = []
    for attendance in attendance_data:
        data_small = {"id": attendance.student.id, "name": attendance.student.full_name, "status": attendance.status}
        list_data.append(data_small)        
    # Return the serialized data as JSON response
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def get_class_student_attendance(request):  
    attendance_date=request.POST.get("attendance_date_id") 
    current_class = request.POST.get("current_class")
    students = Students.objects.filter(current_class=current_class)
    attendance_date_id=ClassAttendance.objects.get(id=attendance_date)
    attendance_data = StudentClassAttendance.objects.filter(
            attendance_id=attendance_date_id,
            student_id__in=students
        )        
    
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student.id,"name":student.student.full_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_class_updateattendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")     
    attendance=ClassAttendance.objects.get(id=attendance_date)     
    json_student=json.loads(student_ids)  
    try:
        for stud in json_student:
             student=Students.objects.get(id=stud['id'])
             attendance_report=StudentClassAttendance.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status =stud["status"]
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
    

@login_required
def staff_sendfeedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data,'staff':staff,})

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
    return render(request,"staff_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report, 'staff':staff,})



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
    return render(request, "staff_template/staff_details.html", context) 


def download_student_results_excel(request, student_id, exam_type_id, year):
    # Convert year string to a date or handle as needed
    year = year  # Adjust this as per your data format or handling needs

    # Get the student based on the provided student_id
    student = get_object_or_404(Students, id=student_id)
    exam_type = get_object_or_404(ExamType, id=exam_type_id)

    # Query results
    results = Result.objects.filter(student=student, exam_type=exam_type, date_of_exam=year)
    exam_info = StudentExamInfo.objects.filter(student=student, exam_type=exam_type, selected_class=student.current_class).first()
    position_info = StudentPositionInfo.objects.filter(student=student, exam_type=exam_type, current_class=student.current_class).first()
    exam_metrics, created = ExamMetrics.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    selected_class=student.current_class,
                )
    total_marks = exam_metrics.total_marks
    average = exam_metrics.average
    grademetrics = exam_metrics.grade
    remark = exam_metrics.remark    

    if exam_info:
        division = exam_info.division
        total_grade_points = exam_info.total_grade_points
    else:
        division = "Division Not Available"
        total_grade_points = "Total Grade Points Not Available"

    if position_info:
        position = position_info.position
    else:
        position = "Position Not Available"

    # Create Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = f"{student.full_name} Results"

    # Headers
    ws.append(['Subject', 'Marks', 'Grade', 'Pass/Fail'])

    # Data rows
    for result in results:
        ws.append([
            result.subject.subject_name,
            result.marks,
            result.determine_grade(),  # Call the method to get the value
            result.determine_pass_fail()
        ])

    # Additional information
    ws.append(['Position', position])
    ws.append(['Total Grade Points', total_grade_points])
    ws.append(['Division', division])
    ws.append(['Total Marks', total_marks])
    ws.append(['Average', average])
    ws.append(['Grade', grademetrics])
    ws.append(['Remark', remark])

    # Adjust column widths and alignment
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
        ws.column_dimensions[column].alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
        ws.cell(row=1, column=col[0].column).font = Font(bold=True)

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={student.full_name}_results.xlsx'
    wb.save(response)
    return response


@login_required
def student_subject_wise_result(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Get the student based on the provided student_id
        student_id = request.POST.get('student_id')
        exam_type_id = request.POST.get('exam_type_id')
        year = request.POST.get('year')
        staff = request.user.staffs
        student = Students.objects.get(id=student_id)
        # Replace 'Students' with your actual student model
        
        form_i_students = Students.objects.filter(current_class=student.current_class)
        total_students = form_i_students.count()
        # Query the results for the specific student
        exam_type = get_object_or_404(ExamType, id=exam_type_id)

        results = Result.objects.filter(student=student, exam_type_id=exam_type,date_of_exam=year)
        exam_info = StudentExamInfo.objects.filter(
            student=student,
            exam_type=exam_type,
            selected_class=student.current_class
        ).first()

        # Retrieve the StudentPositionInfo for the specified student, exam type, and current class
        position_info = StudentPositionInfo.objects.filter(
            student=student,
            exam_type=exam_type,
            current_class=student.current_class
        ).first()

        exam_metrics, created = ExamMetrics.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    selected_class=student.current_class,
                )
        total_marks = exam_metrics.total_marks
        average = exam_metrics.average
        grademetrics = exam_metrics.grade
        remark = exam_metrics.remark
        if exam_info:
            division = exam_info.division
            total_grade_points = exam_info.total_grade_points
        else:
            division = "Division Not Available"
            total_grade_points = "Total Grade Points Not Available"

        if position_info:
            position = position_info.position
        else:
            position = "Position Not Available"

        context = {
            'year': year,
            'staff': staff,
            'remark': remark,
            'grademetrics': grademetrics,
            'average': average,
            'total_marks': total_marks,
            'student': student,
            'results': results,
            "students": student,
            'exam_type': exam_type,
            'position': position,  # Add position to the context
            'division': division,  # Add position to the context
            'total_students': total_students,  # Add position to the context
            'total_grade_points': total_grade_points,  # Add total_grade_points to the context
        }
        html_result = render_to_string('staff_template/result_table.html', context)
        return JsonResponse({'html_result': html_result})
    
    

@csrf_exempt 
def save_marks_view(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            result_id = request.POST.get('resultId')
            marks = request.POST.get('marks')

            # Update the marks for the corresponding result
            result = Result.objects.get(id=result_id)
            result.marks = marks
            result.save()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Marks updated successfully.'})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        # Return error response for unsupported request method
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for this endpoint.'})
    
    
@csrf_exempt  # Use this decorator if CSRF protection is not needed
def delete_result_endpoint(request):
    if request.method == 'POST':
        try:
            # Extract the result ID from the request
            result_id = request.POST.get('resultId')

            # Perform the deletion operation, assuming Result is the model name
            result = Result.objects.get(id=result_id)
            result.delete()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Result deleted successfully.'})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'message': str(e)})

    else:
        # Return error response for non-POST requests
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for this endpoint.'})
        

def student_results_view(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Extract form data
        selected_class = request.POST.get('selected_class')
        exam_type_id = request.POST.get('exam_type_id')
        date_of_exam = request.POST.get('date_of_exam')
        
        # Fetch all students
        students = Students.objects.filter(current_class=selected_class)
        
        # Fetch all subjects
        subjects = Subject.objects.all()
        
        # Create a list to store each student's results and metrics
        student_results = []
        
        # Iterate over each student
        for student in students:
            # Fetch results for the current student filtered by exam type and date
            results = Result.objects.filter(
                student=student,
                exam_type_id=exam_type_id,
                date_of_exam=date_of_exam,
                selected_class=selected_class,
            )
            
            # Initialize variables for position, division, total grade points, total marks, average, grade, and remark
            position = None
            division = None
            total_grade_points = None
            total_marks = None
            average = None
            grademetrics = None
            remark = None
            
            # Iterate over each result for the current student
            for result in results:
                # Fetch or calculate position
                position_info, created = StudentPositionInfo.objects.get_or_create(
                    student=student,
                    exam_type=result.exam_type,
                    current_class=result.selected_class,
                )
                position = position_info.position
                
                # Fetch or calculate division
                student_exam_info, created = StudentExamInfo.objects.get_or_create(
                    student=student,
                    exam_type=result.exam_type,
                    selected_class=result.selected_class,
                )
                division = student_exam_info.division
                total_grade_points = student_exam_info.total_grade_points
                
                # Fetch or calculate ExamMetrics
                exam_metrics, created = ExamMetrics.objects.get_or_create(
                    student=student,
                    exam_type=result.exam_type,
                    selected_class=result.selected_class,
                )
                total_marks = exam_metrics.total_marks
                average = exam_metrics.average
                grademetrics = exam_metrics.grade
                remark = exam_metrics.remark
                exam_type = result.exam_type
            
            # Create a dictionary to store subject-wise results for the current student
            student_subject_results = {}
            
            # Iterate over each subject
            for subject in subjects:
                # Check if there is a result for the current subject and student
                result = results.filter(subject=subject).first()
                if result:
                    # If result exists, store the grade
                    grade = result.determine_grade()
                else:
                    # If result does not exist, mark as 'Not Assigned'
                    grade = ''
                
                # Store subject-wise grades in the dictionary
                student_subject_results[subject.subject_name] = grade
            
            # Append student results and metrics to the list
            student_results.append({
                'student': student,
                'total_marks': total_marks,
                'average': average,
                'grademetrics': grademetrics,
                'position': position,
                'division': division,
                'total_grade_points': total_grade_points,
                'remark': remark,
                'student_subject_results': student_subject_results,
            })
        
        # Render the HTML template with the fetched data
        html_result = render_to_string('staff_template/student_results_table.html', {'student_results': student_results})
        
        # Return the HTML result as JSON response
        return JsonResponse({'html_result': html_result})

@login_required
def exam_type_list(request):
    exam_types = ExamType.objects.all()
    staff = request.user.staffs
    return render(request, 'staff_template/exam_type_list.html', {'exam_types': exam_types,'staff':staff})

@login_required
def exam_type_to_view_class(request, exam_type_id):
    try:
        # Retrieve the exam type object
        staff = request.user.staffs
        exam_type = ExamType.objects.get(pk=exam_type_id)
        
        # Pass the exam type object to the template
        return render(request, 'staff_template/class_wise_results.html', 
                      {
                          'exam_type':exam_type,
                         'staff':staff
                    }
                      )        
    except ExamType.DoesNotExist:
        # Handle the case where the exam type does not exist
        return redirect('exam_type_list') 



@login_required
def view_student_to_add_result(request, exam_type_id, class_name): 
    staff = request.user.staffs   
    className = class_name   
    class_name = class_name.replace('-', ' ')  
    # Fetch all students for the specified class
    students = Students.objects.filter(current_class=class_name)
    exam_type = ExamType.objects.get(pk=exam_type_id)  
    # Fetch all subjects
    subjects = Subject.objects.all()
    staff_subjects = staff.subjects.all()
    # Create a list to store each student's results and metrics
    student_results = []
    
    # Iterate over each student
    for student in students:
        # Fetch results for the current student filtered by exam type and class
        results = Result.objects.filter(
            student=student,
            exam_type_id=exam_type_id,               
            selected_class=class_name,
        )
        
        # Initialize variables for position, division, total grade points, total marks, average, grade, and remark
        position = None
        division = None
        total_grade_points = None
        total_marks = None
        average = None
        grademetrics = None
        remark = None
        
        # Iterate over each result for the current student
        for result in results:
            # Fetch or calculate position
            position_info, created = StudentPositionInfo.objects.get_or_create(
                student=student,
                exam_type=result.exam_type,
                current_class=result.selected_class,
            )
            position = position_info.position
            
            # Fetch or calculate division
            student_exam_info, created = StudentExamInfo.objects.get_or_create(
                student=student,
                exam_type=result.exam_type,
                selected_class=result.selected_class,
            )
            division = student_exam_info.division
            total_grade_points = student_exam_info.total_grade_points
            
            # Fetch or calculate ExamMetrics
            exam_metrics, created = ExamMetrics.objects.get_or_create(
                student=student,
                exam_type=result.exam_type,
                selected_class=result.selected_class,
            )
            total_marks = exam_metrics.total_marks
            average = exam_metrics.average
            grademetrics = exam_metrics.grade
            remark = exam_metrics.remark
            exam_type = result.exam_type
        
        # Create a dictionary to store subject-wise results for the current student
        student_subject_results = {}
        
        # Iterate over each subject
        for subject in subjects:
            # Check if there is a result for the current subject and student
            result = results.filter(subject=subject).first()
            if result:
                # If result exists, store the grade
                grade = result.determine_grade()
            else:
                # If result does not exist, mark as 'Not Assigned'
                grade = ''
            
            # Store subject-wise grades in the dictionary
            student_subject_results[subject.subject_name] = grade
        
        # Append student results and metrics to the list
        
        student_results.append({
            'student': student,
            'total_marks': total_marks,
            'average': average,
            'staff': staff,
            'grademetrics': grademetrics,
            'position': position,
            'division': division,
            'total_grade_points': total_grade_points,
            'remark': remark,
            'student_subject_results': student_subject_results,
        })
    
    # Render the HTML template with the fetched data
    return render(request, 'staff_template/class_wise_students_list.html', {
        'student_results': student_results, 
        'class_name': class_name,
        'className': className,
        'staff_subjects': staff_subjects,
        'subjects':subjects,
        'exam_type':exam_type,
        'staff':staff,
        })


@csrf_exempt
def add_student_result(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            data = request.POST

            # List to store subject IDs for checking uniqueness
            subject_ids = []

            # Iterate over the data to process each row of results
            for i in range(len(data.getlist('subjects[]'))):
                subject_id = int(data.getlist('subjects[]')[i])
                marks = float(data.getlist('marks[]')[i])

                # Validate marks range
                if marks < 0 or marks > 100:
                    return JsonResponse({'success': False, 'message': 'Marks should be between 0 and 100.'})

                # Validate subject uniqueness
                if subject_id in subject_ids:
                    return JsonResponse({'success': False, 'message': 'Each subject should be selected only once for each row.'})
                subject_ids.append(subject_id)

                # Check if a result already exists for the student, exam type, class, and subject
                existing_result = Result.objects.filter(
                    student_id=data.get('student_id'),
                    subject_id=subject_id,
                    exam_type_id=data.get('exam_type'),
                    selected_class=data.get('class_name')
                ).first()
                student = Students.objects.get(id=data.get('student_id'))
                if existing_result:
                    return JsonResponse({'success': False, 'message': f'Result already exists for {student} in {existing_result.subject} for this exam type and class.'})

                # Create a Result object and save it to the database
                Result.objects.create(
                    student_id=data.get('student_id'),
                    subject_id=subject_id,
                    exam_type_id=data.get('exam_type'),
                    marks=marks,
                    date_of_exam=data.get('date_of_exam'),
                    selected_class=data.get('class_name'),
                    total_marks=100
                )

            return JsonResponse({'success': True, 'message': 'Results added successfully.'})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for this endpoint.'})
  
@csrf_exempt   
def save_student_result(request):
    if request.method == 'POST':
        try:
            # Parse form data
            student_id = request.POST.get('student_id')
            exam_type_id = request.POST.get('exam_type_id')
            date_of_exam = request.POST.get('date_of_exam')
            student = Students.objects.get(id=student_id)
            selected_class = student.current_class

            # Check if required fields are missing
            if not all([student_id, exam_type_id, date_of_exam]):
                return JsonResponse({'success': False, 'message': 'Required field(s) missing'})

            # Assign default values if fields are empty or null
            history_score = request.POST.get('history_score', 0)
            english_score = request.POST.get('english_score', 0)
            biology_score = request.POST.get('biology_score', 0)
            arabic_score = request.POST.get('arabic_score', 0)
            physics_score = request.POST.get('physics_score', 0)
            mathematics_score = request.POST.get('mathematics_score', 0)
            chemistry_score = request.POST.get('chemistry_score', 0)
            civics_score = request.POST.get('civics_score', 0)
            geography_score = request.POST.get('geography_score', 0)
            kiswahili_score = request.POST.get('kiswahili_score', 0)
            edk_score = request.POST.get('edk_score', 0)
            computer_application_score = request.POST.get('computer_application_score', 0)
            commerce_score = request.POST.get('commerce_score', 0)
            book_keeping_score = request.POST.get('book_keeping_score', 0)

            # Create Results instance
            result = SujbectWiseResults(
                student_id=student_id,
                exam_type_id=exam_type_id,
                selected_class=selected_class,
                history_score=history_score,
                english_score=english_score,
                biology_score=biology_score,
                arabic_score=arabic_score,
                physics_score=physics_score,
                mathematics_score=mathematics_score,
                chemistry_score=chemistry_score,
                civics_score=civics_score,
                geography_score=geography_score,
                kiswahili_score=kiswahili_score,
                edk_score=edk_score,
                computer_application_score=computer_application_score,
                commerce_score=commerce_score,
                book_keeping_score=book_keeping_score,
                date_of_exam=date_of_exam
            )

            # Save the result
            result.save()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Student result added successfully'})

        except Students.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student does not exist'})

        except Exception as e:
            # Return failure response with error message
            return JsonResponse({'success': False, 'message': str(e)})

    # If request method is not POST, return failure response
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def display_results(request):
    results = SujbectWiseResults.objects.all()
    students = Students.objects.all()
    exam_types = ExamType.objects.all()
    return render(request, 'staff_template/exam_results.html', {
        'results': results,
        'students': students,
        'exam_types': exam_types,
        })

@login_required
def manage_result(request):
    # Fetch all students
    staff = request.user.staffs
    students = Students.objects.all()
    # Fetch all subjects
    subjects = Subject.objects.all()
    exam_types = ExamType.objects.all()
    # Create a dictionary to store each student's results
    student_results = {}
    # Iterate over each student
    for student in students:
        # Fetch results for the current student
        results = Result.objects.filter(student=student)

        # Create a dictionary to store subject-wise results for the current student
        student_subject_results = {}

        # Iterate over each subject
        for subject in subjects:
            # Check if there is a result for the current subject and student
            result = results.filter(subject=subject).first()
            if result:
                # If result exists, store the grade
                grade = result.determine_grade()
            else:
                # If result does not exist, mark as 'Not Assigned'
                grade = ''

            # Store subject-wise grades in the dictionary
            student_subject_results[subject.subject_name] = grade

        # Add the dictionary of subject-wise grades to the main dictionary
        student_results[student] = student_subject_results

    return render(request, 'staff_template/manage_results.html', {'student_results': student_results,
                                                                  'students':students,
                                                                  'subjects':subjects,
                                                                  'exam_types':exam_types,
                                                                  'staff':staff
                                                                  })           

@login_required
def students_wise_result_page(request):
    exam_types = ExamType.objects.all()
    staff = request.user.staffs
    distinct_dates= Result.objects.order_by('date_of_exam').values_list('date_of_exam', flat=True).distinct()   
    return render(request, 'staff_template/student_results.html',
                  {                   
                      'exam_types': exam_types,
                      'distinct_dates': distinct_dates,
                      'staff': staff,
                   })

@login_required
def student_subject_wise_result_page(request,student_id): 
    student = Students.objects.get(id=student_id)
    exam_types = ExamType.objects.all()
    staff = request.user.staffs
    distinct_dates= Result.objects.order_by('date_of_exam').values_list('date_of_exam', flat=True).distinct()
    
    return render(request, 'staff_template/subject_wise_results.html',
                  {
                      'student': student,
                      'exam_types': exam_types,
                      'distinct_dates': distinct_dates,
                      'staff': staff,
                   })


@csrf_exempt
@require_POST
def add_results(request):
    try:
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        exam_type_id = request.POST.get('exam_type')        
        marks = request.POST.get('marks')
        date_of_exam = request.POST.get('date_of_exam')
        selected_class = request.POST.get('selected_class')
        total_marks = request.POST.get('total_marks')
        exam_id = request.POST.get('exam_id')  # For editing existing result
        
        # Retrieve the student, subject, and exam type objects
        student = Students.objects.get(pk=student_id)
        subject = Subject.objects.get(pk=subject_id)
        exam_type = ExamType.objects.get(pk=exam_type_id)
        
        # Check if the result already exists
        result_exists = Result.objects.filter(
            student_id=student_id,
            subject_id=subject_id,
            exam_type_id=exam_type_id,
            selected_class=selected_class
        ).exists()
        
        if result_exists:
            return JsonResponse({'status': 'error', 'message': f'The result for {subject} in {exam_type} for {student} already exists'})
        
        # If not, proceed with adding or editing the result
        if exam_id:
            # Editing existing result
            result = Result.objects.get(pk=exam_id)
            result.student = student
            result.subject = subject
            result.exam_type = exam_type
            result.marks = marks
            result.date_of_exam = date_of_exam          
            result.selected_class = selected_class
            result.total_marks = total_marks
            result.save()
        else:
            # Adding new result
            result = Result(
                student=student,
                subject=subject,
                exam_type=exam_type,
                marks=marks,
                date_of_exam=date_of_exam,
                selected_class=selected_class,
                total_marks=total_marks,
            )
            result.save()

        return JsonResponse({'status': 'success','message':'student result successfully added '})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    
@csrf_exempt
def add_student_result(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            data = request.POST

            # List to store subject IDs for checking uniqueness
            subject_ids = []

            # Iterate over the data to process each row of results
            for i in range(len(data.getlist('subjects[]'))):
                subject_id = int(data.getlist('subjects[]')[i])
                marks = float(data.getlist('marks[]')[i])

                # Validate marks range
                if marks < 0 or marks > 100:
                    return JsonResponse({'success': False, 'message': 'Marks should be between 0 and 100.'})

                # Validate subject uniqueness
                if subject_id in subject_ids:
                    return JsonResponse({'success': False, 'message': 'Each subject should be selected only once for each row.'})
                subject_ids.append(subject_id)

                # Check if a result already exists for the student, exam type, class, and subject
                existing_result = Result.objects.filter(
                    student_id=data.get('student_id'),
                    subject_id=subject_id,
                    exam_type_id=data.get('exam_type'),
                    selected_class=data.get('class_name')
                ).first()
                student = Students.objects.get(id=data.get('student_id'))
                if existing_result:
                    return JsonResponse({'success': False, 'message': f'Result already exists for {student} in {existing_result.subject} for this exam type and class.'})

                # Create a Result object and save it to the database
                Result.objects.create(
                    student_id=data.get('student_id'),
                    subject_id=subject_id,
                    exam_type_id=data.get('exam_type'),
                    marks=marks,
                    date_of_exam=data.get('date_of_exam'),
                    selected_class=data.get('class_name'),
                    total_marks=100
                )

            return JsonResponse({'success': True, 'message': 'Results added successfully.'})

        except Exception as e:
            # Return error response
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed for this endpoint.'})
    
    
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
                    return render(request, 'staff_template/update_profile_picture.html')
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
            
    return render(request, 'staff_template/update_profile_picture.html')    