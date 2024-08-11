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
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.utils.dateparse import parse_date
from datetime import date
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
from result_module.forms import ResultForm, StudentResultForm
from result_module.models import (

    ClassAttendance,
    ClassLevel,   
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
        # Fetch the student object from the same branch
        student = Students.objects.get(id=student_id)
        # Retrieve attendance data for the student within the same branch
        class_attendance_present = StudentClassAttendance.objects.filter(student=student, status=True).count()
        class_attendance_absent = StudentClassAttendance.objects.filter(student=student, status=False).count()
        class_attendance_total = StudentClassAttendance.objects.filter(student=student).count()
        # Fetch the number of students in the same branch
   

        # Pass data to the template for rendering
        return render(
            request,
            "academic_template/student_general_attendance.html",
            {
                "class_attendance_present": class_attendance_present,
                "class_attendance_absent": class_attendance_absent,
                "class_attendance_total": class_attendance_total,                    
                "student": student,                    
              
            },
        )

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist or does not belong to your branch.")
        return render(request, "academic_template/student_general_attendance.html")

    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return render(request, "academic_template/student_general_attendance.html")
    
@login_required
def manage_student(request):
    # Get the branch of the logged-in staff member
    staff_branch = request.user.staffs.branch

    # Fetch students that belong to the same branch
    students = Students.objects.filter(branch=staff_branch)

    # Fetch exam types (this query is not branch-dependent)
    exam_types = ExamType.objects.all()

    return render(request, 'academic_template/manage_student.html', {
        'students': students,
        'exam_types': exam_types,
    })  

@login_required
def academic_home(request):
    if request.user.is_authenticated:
        try:
            # Fetch the staff object for the logged-in user
            staff = Staffs.objects.get(admin=request.user)

            # Fetch the branch of the logged-in staff
            staff_branch = staff.branch           
            # Fetch students that belong to the same branch as the logged-in staff
            students_count = Students.objects.filter(branch=staff_branch).count()


            # Render the academic home page with the relevant data
            return render(request, "academic_template/staff_home.html", {
                "student_count": students_count,              
                "staff": staff,
            })

        except Staffs.DoesNotExist:
            # Handle the case when the staff doesn't exist for the logged-in user
            return render(request, "academic_template/error.html")

    else:
        # Redirect the user to the login page if not authenticated
        return redirect("login")  # Replace "login" with the actual URL name of your login page
    

@login_required    
def staff_take_attendance(request):
    class_levels = ClassLevel.objects.all()
  
    return render(request, "academic_template/staff_take_attendance.html", {
        "class_levels": class_levels      
  
    })

@login_required    
def staff_take_class_attendance(request): 
    class_levels = ClassLevel.objects.all()    
    return render(request, "academic_template/staff_take_class_attendance.html", {           
        "class_levels": class_levels,      
    
    })



@csrf_exempt
@login_required
def get_students(request):
    if request.method == "POST":
        try:
            # Retrieve POST parameters
            subject_id = request.POST.get("subject")
            year = request.POST.get("year")
            class_level_id = request.POST.get("class_level")

            # Validate required parameters
            if not (year and class_level_id):
                raise ValueError("Missing required parameters: 'year' and 'class_level' are required.")

            # Retrieve the subject and class level objects
            subject = get_object_or_404(Subject, id=subject_id)
            class_level = get_object_or_404(ClassLevel, id=class_level_id)

            # Get the branch of the logged-in staff
            staff_branch = request.user.staffs.branch

            # Filter students based on class level, year, and branch
            students = Students.objects.filter(
                class_level=class_level,
                updated_at__year=year,
                branch=staff_branch
            )

            # Prepare the response data
            list_data = [
                {
                    "id": student.id,
                    "name": student.full_name  # Assumes a full_name method exists in the Students model
                }
                for student in students
            ]

            return JsonResponse(list_data, safe=False)

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Http404:
            return JsonResponse({"error": "Subject or class level not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
@login_required
def staff_fetch_students(request):
    if request.method == "POST":
        try:
            year = request.POST.get("year")
            class_level_id = request.POST.get("class_level")

            # Check if all required parameters are provided
            if not year or not class_level_id:
                raise ValueError("Year and Class Level are required parameters.")

            # Get the currently logged-in staff member
            current_staff = Staffs.objects.get(admin=request.user)
            staff_branch = current_staff.branch

            # Fetch the class level object
            class_level = ClassLevel.objects.get(id=class_level_id)
            
            # Filter students based on class level, year, and branch
            students = Students.objects.filter(
                class_level=class_level,
                updated_at__year=year,
                is_active=True,
                branch=staff_branch  # Ensure students are in the same branch as the staff
            )

            # Prepare the list of students to be returned as JSON
            list_data = []
            for student in students:
                data_small = {
                    "id": student.id,
                    "name": f"{student.first_name} {student.middle_name} {student.last_name}"
                    # Adjust above if you have a `full_name` method or field
                }
                list_data.append(data_small)

            return JsonResponse(list_data, safe=False)

        except ClassLevel.DoesNotExist:
            return JsonResponse({"error": "Class Level not found."}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Staff member not found."}, status=404)
        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
    

    
@csrf_exempt
def staff_save_class_attendance_data(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        student_ids = request.POST.get("student_ids")
        class_level_id = request.POST.get("class_level")
        attendance_date = request.POST.get("attendance_date")
        
        # Parse JSON data
        json_students = json.loads(student_ids)
        
        try:
            # Retrieve the ClassLevel instance
            class_level = ClassLevel.objects.get(id=class_level_id)
            
            # Check if attendance record already exists for the class_level and date
            existing_attendance = ClassAttendance.objects.filter(class_level=class_level, attendance_date=attendance_date).first()
            
            if existing_attendance:
                # Iterate over the JSON data to create attendance reports for each student
                for student_data in json_students:
                    student_id = student_data['id']
                    status = student_data['status']
                    
                    # Retrieve the student object
                    student = Students.objects.get(id=student_id)
                    
                    # Check if attendance report already exists for the student and attendance record
                    existing_report = StudentClassAttendance.objects.filter(student=student, attendance=existing_attendance).exists()
                    
                    if not existing_report:
                        # Create attendance report for the student
                        attendance_report = StudentClassAttendance(student=student, attendance=existing_attendance, status=status)
                        attendance_report.save()
                
                # Return success response
                return HttpResponse("OK")
            else:
                # Create a new attendance instance
                attendance = ClassAttendance(class_level=class_level, attendance_date=attendance_date)
                attendance.save()

                # Iterate over the JSON data to create attendance reports for each student
                for student_data in json_students:
                    student_id = student_data['id']
                    status = student_data['status']
                    
                    # Retrieve the student object
                    student = Students.objects.get(id=student_id)
                    
                    # Create attendance report for the student
                    attendance_report = StudentClassAttendance(student=student, attendance=attendance, status=status)
                    attendance_report.save()
                
                # Return success response
                return HttpResponse("OK")
        except ObjectDoesNotExist as e:
            # Handle specific object not found error
            print("Error saving attendance:", e)
            return HttpResponse("ERR: Object not found", status=404)
        except Exception as e:
            # Print error for troubleshooting
            print("Error saving attendance:", e)
            # Return error response
            return HttpResponse("ERR: Unable to save attendance", status=500)
    return HttpResponse("ERR: Invalid request method", status=405)
    


@login_required    
def staff_update_class_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)  
    class_levels = ClassLevel.objects.all()
    return render(request, "academic_template/staff_update_class_attendance.html", {           
        "class_levels": class_levels,       
        "staff": staff,
    })

@login_required    
def staff_view_class_attendance(request):
    staff = Staffs.objects.get(admin=request.user.id)
    attendances=ClassAttendance.objects.all()  
    # Assuming that the educational level is a ForeignKey in Staffs model
    class_levels = ClassLevel.objects.all()
    return render(request, "academic_template/staff_view_class_attendance.html", {           
        "class_levels": class_levels,
        "staff": staff,
        "attendances": attendances,
    })


 
@csrf_exempt
def staff_get_class_attendance_date(request):
     class_level = request.POST.get("class_level")   
     year = request.POST.get("year")        
     attendance = ClassAttendance.objects.filter(class_level=class_level,updated_at__year=year)
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
@login_required
def get_class_student_attendance_data(request):  
    if request.method == "POST":
        date_id = request.POST.get("date")
        class_level_id = request.POST.get("class_level")

        if not date_id or not class_level_id:
            return JsonResponse({"error": "Missing 'date' or 'class_level' parameter."}, status=400)

        try:           

            # Retrieve ClassLevel instance
            class_level = ClassLevel.objects.get(id=class_level_id)

            # Retrieve the currently logged-in staff member
            current_user = request.user
            staff = Staffs.objects.get(admin=current_user)
            
            # Ensure the current staff's branch is used for filtering
            branch = staff.branch

            # Retrieve ClassAttendance instance for the given date and class level
            attendance = ClassAttendance.objects.filter(            
                id=date_id
            ).first()      
            if not attendance:
                return JsonResponse({"error": "Attendance record not found."}, status=404)

            # Filter students by the branch of the currently logged-in staff
            students = Students.objects.filter(
                class_level=class_level,
                branch=branch,
                is_active=True
            )
            
            # Fetch attendance data for the given date and class level
            attendance_data = StudentClassAttendance.objects.filter(
                attendance=attendance,
                student__in=students
            )
            
            # Serialize student data
            list_data = []
            for record in attendance_data:
                data_small = {
                    "id": record.student.id,
                    "name": record.student.full_name,
                    "status": record.status
                }
                list_data.append(data_small)
            
            # Return the serialized data as JSON response
            return JsonResponse(list_data, safe=False)
        
        except ClassLevel.DoesNotExist:
            return JsonResponse({"error": "Class Level not found."}, status=404)
        except Staffs.DoesNotExist:
            return JsonResponse({"error": "Staff member not found."}, status=404)
        except Exception as e:
            # Print error for troubleshooting
            print("Error fetching class student attendance data:", e)
            # Return error response
            return JsonResponse({"error": "Unable to fetch attendance data."}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
@login_required
def get_class_student_attendance(request):  
    if request.method == "POST":
        try:
            # Retrieve data from POST request
            attendance_date_id = request.POST.get("attendance_date_id")
            class_level_id = request.POST.get("class_level")

            # Get the current logged-in staff
            current_staff = Staffs.objects.get(admin=request.user)

            # Retrieve ClassLevel instance
            class_level = ClassLevel.objects.get(id=class_level_id)

            # Filter students based on class level and staff's branch
            students = Students.objects.filter(
                class_level=class_level,
                branch=current_staff.branch,  # Ensure students belong to the same branch as the staff
                is_active=True
            )

            # Retrieve ClassAttendance instance for the given attendance_date_id
            attendance_date = ClassAttendance.objects.get(id=attendance_date_id)

            # Fetch attendance data for the given class level and date
            attendance_data = StudentClassAttendance.objects.filter(
                attendance=attendance_date,
                student__in=students
            )
            
            # Prepare the response data
            list_data = []
            for record in attendance_data:
                data_small = {
                    "id": record.student.id,
                    "name": record.student.full_name,
                    "status": record.status
                }
                list_data.append(data_small)
            
            # Return the data as JSON response
            return JsonResponse(list_data, safe=False)

        except ClassLevel.DoesNotExist:
            return JsonResponse({"error": "Class Level not found."}, status=404)
        except ClassAttendance.DoesNotExist:
            return JsonResponse({"error": "Class Attendance record not found."}, status=404)
        except Staffs.DoesNotExist:
            return JsonResponse({"error": "Current staff not found."}, status=404)
        except Exception as e:
            # Print error for debugging
            print("Error fetching class student attendance:", e)
            return JsonResponse({"error": "Unable to fetch attendance data."}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)


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
    return render(request,"academic_template/staff_feedback.html",{"feedback_data":feedback_data,'staff':staff,})

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
    return render(request,"academic_template/staff_leave_template.html",{"staff_leave_report":staff_leave_report, 'staff':staff,})



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
    return render(request, "academic_template/staff_details.html", context) 


def download_student_results_excel(request, student_id, exam_type_id, year):
    # Convert year string to a date or handle as needed
    year = year  # Adjust this as per your data format or handling needs

    # Get the student based on the provided student_id
    student = get_object_or_404(Students, id=student_id)
    exam_type = get_object_or_404(ExamType, id=exam_type_id)

    # Query results
    results = Result.objects.filter(student=student, exam_type=exam_type, date_of_exam=year)
    exam_info = StudentExamInfo.objects.filter(student=student, exam_type=exam_type, class_level=student.class_level).first()
    position_info = StudentPositionInfo.objects.filter(student=student, exam_type=exam_type, class_level=student.class_level).first()
    exam_metrics, created = ExamMetrics.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    class_level=student.class_level,
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
        try:
            # Retrieve data from POST request
            student_id = request.POST.get('student_id')
            exam_type_id = request.POST.get('exam_type_id')
            year = request.POST.get('year')
            staff = request.user.staffs
            
            # Retrieve the branch of the current staff
            staff_branch = staff.branch
            
            # Get the student
            student = Students.objects.get(id=student_id)
            
            # Ensure the student's branch matches the staff's branch
            if student.branch != staff_branch:
                return JsonResponse({"error": "Student's branch does not match the staff's branch."}, status=403)
            
            # Filter students based on class level and branch
            form_i_students = Students.objects.filter(
                class_level=student.class_level,
                branch=staff_branch
            )
            total_students = form_i_students.count()

            # Retrieve the exam type
            exam_type = get_object_or_404(ExamType, id=exam_type_id)

            # Query the results for the specific student
            results = Result.objects.filter(
                student=student,
                exam_type=exam_type,
                date_of_exam=year
            )
            exam_info = StudentExamInfo.objects.filter(
                student=student,
                exam_type=exam_type,
                class_level=student.class_level
            ).first()

            # Retrieve the StudentPositionInfo for the specified student, exam type, and current class
            position_info = StudentPositionInfo.objects.filter(
                student=student,
                exam_type=exam_type,
                class_level=student.class_level
            ).first()

            exam_metrics, created = ExamMetrics.objects.get_or_create(
                student=student,
                exam_type=exam_type,
                class_level=student.class_level,
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
                'exam_type': exam_type,
                'position': position,
                'division': division,
                'total_students': total_students,
                'total_grade_points': total_grade_points,
            }
            html_result = render_to_string('academic_template/result_table.html', context)
            return JsonResponse({'html_result': html_result})

        except Students.DoesNotExist:
            return JsonResponse({"error": "Student not found."}, status=404)
        except ExamType.DoesNotExist:
            return JsonResponse({"error": "Exam Type not found."}, status=404)
        except Exception as e:
            print("Error fetching student subject-wise result:", e)
            return JsonResponse({"error": "Unable to fetch result data."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
    
    

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
        

@login_required
def student_results_view(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            # Extract form data from POST request
            class_level_id = request.POST.get('class_level')
            exam_type_id = request.POST.get('exam_type_id')
            date_of_exam = request.POST.get('date_of_exam')

            # Retrieve the branch of the current logged-in staff
            staff = request.user.staffs
            staff_branch = staff.branch
            
            # Fetch the class level
            class_level = get_object_or_404(ClassLevel, id=class_level_id)
            
            # Fetch all students for the given class level and branch
            students = Students.objects.filter(class_level=class_level, branch=staff_branch)
            
            # Fetch all subjects for the given class level
            subjects = Subject.objects.filter(class_level=class_level)
            
            # List to store each student's results and metrics
            student_results = []
            
            # Iterate over each student
            for student in students:
                # Fetch results for the current student filtered by exam type, date, and class level
                results = Result.objects.filter(
                    student=student,
                    exam_type_id=exam_type_id,
                    date_of_exam=date_of_exam,
                    class_level=class_level,
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
                        class_level=result.class_level,
                    )
                    position = position_info.position
                    
                    # Fetch or calculate division
                    student_exam_info, created = StudentExamInfo.objects.get_or_create(
                        student=student,
                        exam_type=result.exam_type,
                        class_level=result.class_level,
                    )
                    division = student_exam_info.division
                    total_grade_points = student_exam_info.total_grade_points
                    
                    # Fetch or calculate ExamMetrics
                    exam_metrics, created = ExamMetrics.objects.get_or_create(
                        student=student,
                        exam_type=result.exam_type,
                        class_level=result.class_level,
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
                    'subjects': subjects,
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
            html_result = render_to_string('academic_template/student_results_table.html', {'student_results': student_results, 'subjects': subjects})
            
            # Return the HTML result as JSON response
            return JsonResponse({'html_result': html_result})

        except ClassLevel.DoesNotExist:
            return JsonResponse({"error": "Class Level not found."}, status=404)
        except Exception as e:
            print("Error fetching student results:", e)
            return JsonResponse({"error": "Unable to fetch student results."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def exam_type_list(request):
    exam_types = ExamType.objects.all()
    staff = request.user.staffs
    return render(request, 'academic_template/exam_type_list.html', {'exam_types': exam_types,'staff':staff})

@login_required
def exam_type_to_view_class(request, exam_type_id):
    try:
        # Retrieve the exam type object        
        exam_type = ExamType.objects.get(pk=exam_type_id)
        class_levels = ClassLevel.objects.all()
        
        # Pass the exam type object to the template
        return render(request, 'academic_template/class_wise_results.html', 
                      {
                          'exam_type':exam_type,
                         'class_levels':class_levels
                    }
                      )        
    except ExamType.DoesNotExist:
        # Handle the case where the exam type does not exist
        return redirect('exam_type_list') 



@login_required
def view_student_to_add_result(request, exam_type_id, class_level_id):
    try:
        # Get the current logged-in staff's branch
        staff = request.user.staffs
        staff_branch = staff.branch
        
        # Fetch the class level
        class_level = get_object_or_404(ClassLevel, id=class_level_id)
        
        # Fetch students for the given class level and staff's branch
        students = Students.objects.filter(class_level=class_level, branch=staff_branch)
        
        # Fetch the exam type
        exam_type = get_object_or_404(ExamType, pk=exam_type_id)
        
        # Fetch subjects for the given class level
        subjects = Subject.objects.filter(class_level=class_level)
        
        student_results = []

        # Iterate over each student
        for student in students:
            results = Result.objects.filter(
                student=student,
                exam_type_id=exam_type_id,
                class_level=class_level,
            )
            
            position, division, total_grade_points = None, None, None
            total_marks, average, grademetrics, remark = None, None, None, None

            # Fetch or calculate metrics
            if results.exists():
                position_info, _ = StudentPositionInfo.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    class_level=class_level,
                )
                position = position_info.position

                student_exam_info, _ = StudentExamInfo.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    class_level=class_level,
                )
                division = student_exam_info.division
                total_grade_points = student_exam_info.total_grade_points

                exam_metrics, _ = ExamMetrics.objects.get_or_create(
                    student=student,
                    exam_type=exam_type,
                    class_level=class_level,
                )
                total_marks = exam_metrics.total_marks
                average = exam_metrics.average
                grademetrics = exam_metrics.grade
                remark = exam_metrics.remark

            # Prepare subject results
            student_subject_results = {}
            for subject in subjects:
                result = results.filter(subject=subject).first()
                if result:
                    grade = result.determine_grade()
                else:
                    grade = ''
                
                student_subject_results[subject.subject_name] = grade

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

        return render(request, 'academic_template/class_wise_students_list.html', {
            'student_results': student_results,
            'class_name': class_level.class_name,
            'className': class_level.class_name,
            'class_level': class_level,
            'subjects': subjects,
            'exam_type': exam_type,
        })
    
    except ClassLevel.DoesNotExist:
        return render(request, 'error.html', {'message': 'Class Level not found.'})
    except ExamType.DoesNotExist:
        return render(request, 'error.html', {'message': 'Exam Type not found.'})
    except Exception as e:
        # Log error or handle accordingly
        return render(request, 'error.html', {'message': 'An error occurred: {}'.format(e)})
    




@login_required
def display_results(request):
    try:
        # Get the current logged-in staff's branch
        staff = request.user.staffs
        staff_branch = staff.branch
        
        # Filter students based on the branch of the logged-in staff
        students = Students.objects.filter(branch=staff_branch)
        
        # Fetch results and exam types
        results = SujbectWiseResults.objects.filter(student__in=students)
        exam_types = ExamType.objects.all()
        
        return render(request, 'academic_template/exam_results.html', {
            'results': results,
            'students': students,
            'exam_types': exam_types,
        })
    
    except Exception as e:
        # Log error or handle accordingly
        return render(request, 'error.html', {'message': 'An error occurred: {}'.format(e)})

@login_required
def manage_result(request):
    try:
        # Get the current logged-in staff's branch
        staff = request.user.staffs
        staff_branch = staff.branch
        
        # Filter students based on the branch of the logged-in staff
        students = Students.objects.filter(branch=staff_branch)
        
        # Fetch all subjects and exam types
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

        return render(request, 'academic_template/manage_results.html', {
            'student_results': student_results,
            'students': students,
            'subjects': subjects,
            'exam_types': exam_types,
            'staff': staff
        })

    except Exception as e:
        # Log error or handle accordingly
        return render(request, 'error.html', {'message': 'An error occurred: {}'.format(e)}) 
       

@login_required    
def students_wise_result_page(request):
    exam_types = ExamType.objects.all()
    class_levels = ClassLevel.objects.all()
    distinct_dates= Result.objects.order_by('date_of_exam').values_list('date_of_exam', flat=True).distinct()   
    return render(request, 'academic_template/student_results.html',
                  {                   
                      'class_levels': class_levels,
                      'exam_types': exam_types,
                      'distinct_dates': distinct_dates,
                   })

@login_required
def student_subject_wise_result_page(request,student_id): 
    student = Students.objects.get(id=student_id)
    exam_types = ExamType.objects.all()
    staff = request.user.staffs
    distinct_dates= Result.objects.order_by('date_of_exam').values_list('date_of_exam', flat=True).distinct()
    
    return render(request, 'academic_template/subject_wise_results.html',
                  {
                      'student': student,
                      'exam_types': exam_types,
                      'distinct_dates': distinct_dates,
                      'staff': staff,
                   })



    
    
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
                    return render(request, 'academic_template/update_profile_picture.html')
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
            
    return render(request, 'academic_template/update_profile_picture.html')    


class ResultCreateUpdateView(LoginRequiredMixin, View):
    def get(self, request, exam_type_id, class_level_id, pk=None, *args, **kwargs):
        exam_type = get_object_or_404(ExamType, pk=exam_type_id)
        class_level = get_object_or_404(ClassLevel, pk=class_level_id)
        
        # Get the branch of the currently logged-in staff
        branch = request.user.staffs.branch if request.user.staffs else None

        # Filter subjects based on the class level
        subjects = Subject.objects.filter(class_level=class_level)

        if pk:
            result = get_object_or_404(Result, pk=pk)
            form = ResultForm(instance=result, exam_type=exam_type, class_level=class_level, branch=branch)
            context = {'form': form, 'is_edit': True}
        else:
            form = ResultForm(exam_type=exam_type, class_level=class_level, branch=branch)
            context = {'form': form, 'is_edit': False}
        
        context['subjects'] = subjects
        return render(request, 'academic_template/add_manage_result.html', context)

    def post(self, request, exam_type_id, class_level_id, pk=None, *args, **kwargs):
        exam_type = get_object_or_404(ExamType, pk=exam_type_id)
        class_level = get_object_or_404(ClassLevel, pk=class_level_id)

        # Get the branch of the currently logged-in staff
        branch = request.user.staffs.branch if request.user.staffs else None

        if pk:
            result = get_object_or_404(Result, pk=pk)
            form = ResultForm(request.POST, instance=result, exam_type=exam_type, class_level=class_level, branch=branch)
        else:
            form = ResultForm(request.POST, exam_type=exam_type, class_level=class_level, branch=branch)

        if form.is_valid():
            result = form.save(commit=False)
            result.exam_type = exam_type
            result.class_level = class_level
            result.save()
            action = request.POST.get('action')
            if action == 'save':
                messages.success(request, 'Result saved successfully!')
                return redirect('academic_view_student_to_add_result', exam_type_id=exam_type_id, class_level_id=class_level_id)  # Replace with your URL name for the result list view
            elif action == 'save_and_continue':
                messages.success(request, 'Result saved! You can add another one.')
                return redirect('academic_add_result', exam_type_id=exam_type_id, class_level_id=class_level_id)

        context = {'form': form, 'is_edit': pk is not None}
        return render(request, 'academic_template/add_manage_result.html', context)
    
    
class StudentResultCreateUpdateView(CreateView, UpdateView):
    model = Result
    form_class = StudentResultForm
    template_name = 'academic_template/add_student_result.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        student = get_object_or_404(Students, id=self.kwargs['student_id'])
        exam_type = get_object_or_404(ExamType, id=self.kwargs['exam_type_id'])
        kwargs.update({
            'student': student,
            'exam_type': exam_type
        })
        return kwargs

    def form_valid(self, form):
        # Set the `student`, `exam_type`, and `class_level` fields
        form.instance.student = get_object_or_404(Students, id=self.kwargs['student_id'])
        form.instance.exam_type = get_object_or_404(ExamType, id=self.kwargs['exam_type_id'])
        form.instance.class_level = form.instance.student.class_level  # Set class_level from student

        return super().form_valid(form)

    def get_object(self, queryset=None):
        # Return the existing Result object if in update mode
        if self.kwargs.get('pk'):
            return super().get_object(queryset)
        return None

    def get_success_url(self):
        action = self.request.POST.get('action')
        
        if action == 'save_and_continue':
            return reverse('academic_student_result_create_update', kwargs={
                'student_id': self.kwargs['student_id'],
                'exam_type_id': self.kwargs['exam_type_id'],
                'class_level_id': self.kwargs['class_level_id']
            })
        
        elif action == 'save' :
             return reverse('academic_view_student_to_add_result', kwargs={
            'exam_type_id': self.kwargs['exam_type_id'],
            'class_level_id': self.kwargs['class_level_id']
        })   
       

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Students, id=self.kwargs['student_id'])
        context['exam_type'] = get_object_or_404(ExamType, id=self.kwargs['exam_type_id'])
        context['is_edit'] = self.object is not None
        return context
    
    
def get_subject_count_per_class_level(request):
    data = Subject.objects.values('class_level__class_name').annotate(subject_count=models.Count('id'))
    return JsonResponse(list(data), safe=False)       