from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from result_module.models import ClassFee, ClassLevel, CustomUser, Expenditure, FeePayment, FeeStructure, MadrasatulFee, MadrasatulFeePayment, Result, SchoolFeesInstallment,  Staffs, Students, Subject, TransportFee, TransportFeePayment
from django.db.models import Q
from django.utils.timezone import now
import pandas as pd

class ImportStudentForm(forms.Form):
    student_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportSubjectForm(forms.Form):
    subject_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportExamTypeForm(forms.Form):
    exam_type_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportSujbectWiseResultsForm(forms.Form):
    new_record = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    date_of_exam = forms.DateField(
        initial=pd.to_datetime('today').date(),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_of_exam = cleaned_data.get('date_of_exam')

        # Ensure the date_of_exam is provided
        if not date_of_exam:
            raise forms.ValidationError("Date of exam is required.")

        return cleaned_data
class ImportStudentsForm(forms.Form):
    file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )


# Define choices for gender and current_class fields
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

BRANCH_CHOICES = [
    ('Uwanja wa Ndege', 'Uwanja wa Ndege'),
    ('Chukwani', 'Chukwani'),
]

STAFF_ROLE_CHOICES = [
    ('Academic', 'Academic'),
    ('Headmaster', 'Headmaster'),
    ('Admin', 'Admin'),
    ('Class Teacher', 'Class Teacher'),
    ('Accountant', 'Accountant'),

]

class AddStaffForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name', required=True, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter First Name"})
    )
    middle_name = forms.CharField(
        label='Middle Name', required=False, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Middle Name"})
    )
    last_name = forms.CharField(
        label='Last Name', required=True, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Last Name"})
    )
    gender = forms.ChoiceField(
        label='Gender', required=True, choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )
    email = forms.CharField(
        label='Email', required=True, max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email"})
    )
    username = forms.CharField(
        label='Username', required=True, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Username"})
    )
    password = forms.CharField(
        label='Password', required=True, max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"})
    )
    phone_number = forms.CharField(
        label='Phone Number', required=True, max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Phone Number"})
    )
    address = forms.CharField(
        label='Address', required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Address", "rows": 3})
    )
    date_of_birth = forms.DateField(
        label='Date of Birth', required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    date_of_employment = forms.DateField(
        label='Date of Employment', required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    staff_role = forms.ChoiceField(
        label='Staff Role', required=True, choices=[
            ('Admin', 'Admin'),
            ('Staff', 'Staff'),
            ('Accountant', 'Accountant'),
            ('Headmaster', 'Headmaster'),
            ('Academic', 'Academic')
        ],
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )
    branch = forms.ChoiceField(
        label='Branch', required=True, choices=BRANCH_CHOICES,  # Assuming you have a BRANCH_CHOICES
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )
    profile_pic = forms.ImageField(
        label='Profile Picture', required=False,       
         widget=forms.FileInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = Staffs
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'email', 'username', 'password',
            'phone_number', 'address', 'date_of_birth', 'date_of_employment', 'staff_role', 'branch', 'profile_pic'
        ]
        widgets = {
            'address': forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Address", "rows": 3}),
            'date_of_birth': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            'date_of_employment': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('0') or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Phone number must start with '0' and have exactly ten digits.")
        return phone_number

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type=2  # Assuming user_type 2 corresponds to staff
        )
        user.save()

        staff = super(AddStaffForm, self).save(commit=False)
        staff.admin = user
        if commit:
            staff.save()
            self.save_m2m()
        return staff
# forms.py

class EditStaffForm(forms.ModelForm):
    email = forms.CharField(
        label='Email', required=True, max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email"})
    )
    first_name = forms.CharField(
        label='First Name', required=True, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter First Name"})
    )
    last_name = forms.CharField(
        label='Last Name', required=True, max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Last Name"})
    )
    phone_number = forms.CharField(
        label='Phone Number', required=True, max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Phone Number"})
    )
    address = forms.CharField(
        label='Address', required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Address", "rows": 3})
    )
    gender = forms.ChoiceField(
        label='Gender', required=True, choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )
    date_of_birth = forms.DateField(
        label='Date of Birth', required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    date_of_employment = forms.DateField(
        label='Date of Employment', required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    branch = forms.ChoiceField(
        label='Branch', required=True, choices=BRANCH_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )
    staff_role = forms.ChoiceField(
        label='Staff Role', required=True, choices=STAFF_ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control select2bs4"})
    )

    class Meta:
        model = Staffs
        fields = [
            'middle_name', 'address', 'gender', 'date_of_birth', 'date_of_employment',
            'phone_number', 'branch', 'staff_role', 'profile_pic'
        ]
        widgets = {
            'middle_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Middle Name"}),
            'profile_pic': forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(EditStaffForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.admin.email
        self.fields['first_name'].initial = self.instance.admin.first_name
        self.fields['last_name'].initial = self.instance.admin.last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        instance = getattr(self, 'instance', None)
        if CustomUser.objects.filter(email=email).exists() and (not instance or instance.admin.email != email):
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('0') or not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Phone number must start with '0' and have exactly ten digits.")
        return phone_number

    def save(self, commit=True):
        staff = super(EditStaffForm, self).save(commit=False)
        # Update the CustomUser part
        user = staff.admin
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        if commit:
            staff.save()
        return staff
    
class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_level', 'school_fee_amount']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'school_fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_school_fee_amount(self):
        amount = self.cleaned_data.get('school_fee_amount')
        if amount is not None and amount < 0:
            raise forms.ValidationError('School fee amount cannot be negative')
        return amount


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'class_level', 'is_active']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject name'}),
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SchoolFeesInstallmentForm(forms.ModelForm):
    class Meta:
        model = SchoolFeesInstallment
        fields = ['installment_name', 'amount_required', 'start_date', 'end_date', 'class_level']
        widgets = {
            'installment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter installment name'}),
            'amount_required': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter required amount'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        class_level = cleaned_data.get('class_level')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Validate the number of installments for the class level
        if class_level:
            # Count existing installments for the selected class level
            existing_installments = SchoolFeesInstallment.objects.filter(class_level=class_level).count()

            # When editing an existing record, exclude the current instance from the count
            if self.instance.pk:
                existing_installments = SchoolFeesInstallment.objects.filter(class_level=class_level).exclude(pk=self.instance.pk).count()

            # Check if adding the new installment would exceed the limit
            if existing_installments >= 3:
                raise ValidationError(f'The selected class level already has three installments.')

        # Validate that start_date is less than end_date
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError({'start_date': 'Start date must be before the end date.'})

        return cleaned_data
        
class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_level', 'school_fee_amount']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'school_fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the school fee amount'}),
        }        
        
class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['class_name']
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    
class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['description', 'amount', 'date', 'category','branch']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),           
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control select2bs4'}),
             'branch': forms.Select(attrs={'class': 'form-control select2bs4'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom button choices or any other modifications here if needed    
        
class ClassFeeForm(forms.ModelForm):
    class Meta:
        model = ClassFee
        fields = ['class_level', 'fee_type', 'fee_amount']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'fee_type': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }        
    
class MadrasatulFeeForm(forms.ModelForm):
    class Meta:
        model = MadrasatulFee
        fields = ['class_level', 'fee_amount']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter fee amount'}),
        }    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'first_name', 'middle_name', 'last_name', 'class_level', 'date_of_birth',
            'gender', 'first_phone_number', 'second_phone_number', 'fee_payer_number',
            'address', 'profile_pic', 'examination_number', 'previously_examination_number',
            'physical_disabilities_condition', 'branch', 'services'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_level': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'first_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'second_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'fee_payer_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'examination_number': forms.TextInput(attrs={'class': 'form-control'}),
            'previously_examination_number': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_disabilities_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control select2bs4'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        optional_fields = [
            'examination_number', 'previously_examination_number', 'profile_pic', 
            'second_phone_number', 'physical_disabilities_condition', 'fee_payer_number'
        ]
        for field in self.fields:
            self.fields[field].required = field not in optional_fields

    def clean_first_phone_number(self):
        first_phone_number = self.cleaned_data.get('first_phone_number')
        if not first_phone_number.startswith('0') or len(first_phone_number) != 10:
            raise ValidationError('Phone number must start with 0 and be 10 digits long.')
        return first_phone_number

    def clean_second_phone_number(self):
        second_phone_number = self.cleaned_data.get('second_phone_number')
        if second_phone_number and (not second_phone_number.startswith('0') or len(second_phone_number) != 10):
            raise ValidationError('Phone number must start with 0 and be 10 digits long.')
        return second_phone_number

    def clean_fee_payer_number(self):
        fee_payer_number = self.cleaned_data.get('fee_payer_number')
        if fee_payer_number and (not fee_payer_number.startswith('0') or len(fee_payer_number) != 10):
            raise ValidationError('Fee payer number must start with 0 and be 10 digits long.')
        return fee_payer_number


class TransportFeeForm(forms.ModelForm):
    class Meta:
        model = TransportFee
        fields = ['location', 'fee_amount']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter fee amount'}),
        }
        
class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'class_fee', 'amount_paid', 'payment_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'class_fee': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount paid'}),
            'payment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        branch_students = kwargs.pop('branch_students', None)
        super().__init__(*args, **kwargs)
        
        if branch_students is not None:
            self.fields['student'].queryset = branch_students

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        class_fee = cleaned_data.get('class_fee')
        amount_paid = cleaned_data.get('amount_paid')

        # Validate that the class_fee corresponds to the student's class level
        if student and class_fee:
            student_class_level = student.class_level
            fee_class_level = class_fee.class_level

            if student_class_level != fee_class_level:
                self.add_error('class_fee', f'The selected fee does not correspond with the student\'s class level ({student_class_level}).')

        # Validate that the amount paid does not exceed the required amount
        if class_fee and amount_paid:
            total_required = class_fee.fee_amount
            if amount_paid > total_required:
                self.add_error('amount_paid', f'The amount paid ({amount_paid}) exceeds the required fee ({total_required}). Please adjust the amount.')

        return cleaned_data
    
class MadrasatulFeePaymentForm(forms.ModelForm):
    class Meta:
        model = MadrasatulFeePayment
        fields = ['student', 'matrasatul_fee', 'amount_paid', 'payment_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'matrasatul_fee': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount paid'}),
            'payment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        branch_students = kwargs.pop('branch_students', None)
        super().__init__(*args, **kwargs)
        
        if branch_students is not None:
            self.fields['student'].queryset = branch_students

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        matrasatul_fee = cleaned_data.get('matrasatul_fee')
        amount_paid = cleaned_data.get('amount_paid')

        if student and matrasatul_fee:
            student_class_level = student.class_level
            fee_class_level = matrasatul_fee.class_level

            if student_class_level != fee_class_level:
                self.add_error('matrasatul_fee', f'The selected fee does not correspond with the student\'s class level ({student_class_level}).')

        if matrasatul_fee and amount_paid:
            total_required = matrasatul_fee.fee_amount
            if amount_paid > total_required:
                self.add_error('amount_paid', f'The amount paid ({amount_paid}) exceeds the required fee ({total_required}). Please adjust the amount.')

        return cleaned_data
    
class TransportFeePaymentForm(forms.ModelForm):
    class Meta:
        model = TransportFeePayment
        fields = ['student', 'transport_fee', 'amount_paid', 'payment_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'transport_fee': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount paid'}),
            'payment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        branch_students = kwargs.pop('branch_students', None)
        super().__init__(*args, **kwargs)
        
        if branch_students is not None:
            self.fields['student'].queryset = branch_students

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        transport_fee = cleaned_data.get('transport_fee')
        amount_paid = cleaned_data.get('amount_paid')

        # Validate that the amount paid does not exceed the transport fee
        if transport_fee and amount_paid:
            total_required = transport_fee.fee_amount
            if amount_paid > total_required:
                self.add_error('amount_paid', f'The amount paid ({amount_paid}) exceeds the required transport fee ({total_required}). Please adjust the amount.')

        return cleaned_data
     

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks', 'date_of_exam']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'subject': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'date_of_exam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        exam_type = kwargs.pop('exam_type', None)
        class_level = kwargs.pop('class_level', None)
        branch = kwargs.pop('branch', None)  # Extract branch from kwargs
        super(ResultForm, self).__init__(*args, **kwargs)

        if class_level:
            # Filter students based on class level and branch
            self.fields['student'].queryset = Students.objects.filter(class_level=class_level, branch=branch)
            # Filter subjects based on class level
            self.fields['subject'].queryset = Subject.objects.filter(class_level=class_level)

        # Store exam_type as an instance variable
        self.exam_type = exam_type

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        subject = cleaned_data.get("subject")
        marks = cleaned_data.get("marks")
        date_of_exam = cleaned_data.get("date_of_exam")

        # Fetch class level from student
        class_level = student.class_level if student else None

        # Ensure uniqueness of the result for the same student, subject, exam_type, date_of_exam, and class_level
        if Result.objects.filter(
                student=student, subject=subject, exam_type=self.exam_type,
                date_of_exam=date_of_exam, class_level=class_level
        ).exists():
            raise forms.ValidationError("This student already has a result for this subject, exam type, date of exam, and class level.")

        # Ensure marks are between 0 and 100
        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("Marks must be between 0 and 100.")
        
        return cleaned_data


class StudentResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['subject', 'marks', 'date_of_exam']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'date_of_exam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        exam_type = kwargs.pop('exam_type', None)
        super().__init__(*args, **kwargs)

        if student:
            class_level = student.class_level
            self.fields['subject'].queryset = Subject.objects.filter(class_level=class_level)

        self.student = student
        self.exam_type = exam_type

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")
        marks = cleaned_data.get("marks")
        date_of_exam = cleaned_data.get("date_of_exam")

        if Result.objects.filter(
                student=self.student, subject=subject, exam_type=self.exam_type,
                date_of_exam=date_of_exam
        ).exists():
            raise forms.ValidationError("This student already has a result for this subject, exam type, and date of exam.")

        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("Marks must be between 0 and 100.")
        
        return cleaned_data