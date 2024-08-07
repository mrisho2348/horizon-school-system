# views.py
from decimal import Decimal, InvalidOperation
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
import openpyxl
from result_module.models import ExamType, Students, Subject, SujbectWiseResults
from .resources import ExamTypeResources, SubjectResources, SujbectWiseResultsResources
from .forms import ImportExamTypeForm, ImportStudentsForm, ImportSubjectForm, ImportSujbectWiseResultsForm
from tablib import Dataset
logger = logging.getLogger(__name__)



def import_student_records(request):
    if request.method == 'POST':
        form = ImportStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                workbook = openpyxl.load_workbook(file)
                sheet = workbook.active

                # Read headers
                headers = [cell.value.strip() for cell in sheet[1]]  # Trim headers
                required_headers = [
                    'registration_number', 'full_name', 'current_class', 
                    'date_of_birth', 'gender', 'phone_number', 'address', 'profile_pic', 'is_active'
                ]

                # Validate headers
                if headers[:len(required_headers)] != required_headers:
                    messages.error(request, 'Invalid file format')
                    return render(request, 'hod_template/import_students.html', {'form': form})

                # Read data from rows
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    data = dict(zip(headers, (cell.strip() if isinstance(cell, str) else cell for cell in row)))  # Trim data
                    try:
                        Students.objects.create(
                            registration_number=data['registration_number'],
                            full_name=data['full_name'],
                            current_class=data['current_class'],
                            date_of_birth=data['date_of_birth'],
                            gender=data['gender'],
                            phone_number=data['phone_number'],
                            address=data['address'],
                            profile_pic=data['profile_pic'],
                            is_active=data['is_active']
                        )
                    except IntegrityError:
                        # Skip duplicate entries and continue
                        continue

                return HttpResponseRedirect(reverse('manage_student'))

            except Exception as e:
                messages.error(request, f"Failed to import data: {str(e)}")
                return render(request, 'hod_template/import_students.html', {'form': form})
    else:
        form = ImportStudentsForm()

    return render(request, 'hod_template/import_students.html', {'form': form})


def import_subject_wise_result(request, exam_type_id):
    if request.method == 'POST':
        form = ImportSujbectWiseResultsForm(request.POST, request.FILES)
        exam_type = ExamType.objects.get(pk=exam_type_id)  # Get the exam type
                
        if form.is_valid():
            try:
                resource = SujbectWiseResultsResources()
                new_records = request.FILES['new_record']
                
                # Load the imported data using tablib
                dataset = Dataset()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Adjust format accordingly

                for data in imported_data:
                    # Check if the row has the expected number of elements
                    if len(data) != 15:  # Assuming there are 15 columns of scores in each row
                        # Log the error and skip this row
                        messages.error(request, f'Invalid data format in row: {data}')
                        continue

                    # Extract student's name and scores
                    student_name = data[0]
                    scores = data[1:]

                    try:
                        # Get the student object using the provided name
                        student = Students.objects.get(full_name=student_name)
                    except Students.DoesNotExist:
                        # If the student does not exist, log the error and continue to the next record
                        messages.error(request, f'Student "{student_name}" does not exist.')
                        continue

                    # Validate and convert score values to decimal numbers
                    converted_scores = []
                    for i, score in enumerate(scores):
                        try:
                            converted_score = Decimal(score)
                            if not 0 <= converted_score <= 100:  # Check if the score is between 0 and 100
                                raise InvalidOperation("Score must be between 0 and 100")
                            converted_scores.append(converted_score)
                        except InvalidOperation as e:
                            # Log the error and skip this row
                            messages.error(request, f'Invalid score format for student "{student.full_name}" at index {i+1}: {e}')
                            break  # Skip the entire row if any score value is invalid

                    else:
                        # Check if a record already exists for this student, exam type, and class
                        existing_record = SujbectWiseResults.objects.filter(student=student, exam_type=exam_type, selected_class=student.current_class).exists()
                        if existing_record:
                            # Skip this record if a record already exists for this student, exam type, and class
                            continue

                        # Create a new SujbectWiseResults record
                        new_record = SujbectWiseResults(                       
                            student=student,
                            history_score=converted_scores[0],
                            english_score=converted_scores[1],
                            kiswahili_score=converted_scores[2],
                            geography_score=converted_scores[3],
                            mathematics_score=converted_scores[4],
                            physics_score=converted_scores[5],
                            arabic_score=converted_scores[6],
                            biology_score=converted_scores[7],
                            chemistry_score=converted_scores[8],
                            edk_score=converted_scores[9],
                            civics_score=converted_scores[10],
                            computer_application_score=converted_scores[11],
                            commerce_score=converted_scores[12],
                            book_keeping_score=converted_scores[13],
                            selected_class=student.current_class,
                            exam_type=exam_type,
                        )
                        new_record.save()
                
                # Redirect to the manage_sujbectWiseResults page after successful import
                return redirect(reverse('view_student_to_add_result', args=[exam_type_id, student.current_class]))
            except Exception as e:
                # Handle any exceptions and display an error message
                messages.error(request, f'An error occurred: {e}')
    else:
        # If the request method is not POST, render the import form
        form = ImportSujbectWiseResultsForm()

    return render(request, 'hod_template/import_subject_wise_result.html', {
        'form': form,
        'exam_type_id': exam_type_id,  
    })
    

def import_subject_records(request):
    if request.method == 'POST':
        form = ImportSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = SubjectResources()
                new_records = request.FILES['student_file']
                
                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     subject_recode = Subject(
                        subject_name=data[0],
                                      
                    )
                     subject_recode.save()

                return redirect('manage_subject') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportSubjectForm()

    return render(request, 'hod_template/import_subject.html', {'form': form})

def import_exam_type_records(request):
    if request.method == 'POST':
        form = ImportExamTypeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = ExamTypeResources()
                new_records = request.FILES['student_file']
                
                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly

                for data in imported_data:
                     subject_recode = ExamType(
                        name=data[0],
                        description=data[0],
                                      
                    )
                     subject_recode.save()

                return redirect('manage_exam_type') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportExamTypeForm()

    return render(request, 'hod_template/import_exam_type.html', {'form': form})


