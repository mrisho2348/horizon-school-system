import openpyxl
from django.http import HttpResponse
from .models import Students

def download_students_excel_template(request):
    # Create a new Workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Students Template"

    # Define column headers from model fields
    excluded_fields = ['id', 'created_at', 'updated_at','registration_number','examination_number','previously_examination_number','profile_pic','is_active']
    model_fields = [field.name for field in Students._meta.get_fields() 
                    if not field.auto_created and not field.is_relation and field.name not in excluded_fields]

    # Add headers to the first row
    for col_num, column_title in enumerate(model_fields, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = column_title

    # Save the workbook to a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students_template.xlsx'
    workbook.save(response)

    return response
