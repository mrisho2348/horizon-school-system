from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from result_module.models import CustomUser, FeeStructure,  Staffs, Students
from django.db.models import Q

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
class ImportStudentsForm(forms.Form):
    file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )


# Define choices for gender and current_class fields
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
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
        fields = ['school_class', 'school_fee_amount']
        widgets = {
            'school_class': forms.Select(attrs={'class': 'form-control select2bs4'}),
            'school_fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
          
        }

    def clean_school_fee_amount(self):
        amount = self.cleaned_data.get('school_fee_amount')
        if amount < 0:
            raise forms.ValidationError('School fee amount cannot be negative')
        return amount

    
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'first_name', 'middle_name', 'last_name', 'current_class', 'date_of_birth',
            'gender', 'first_phone_number', 'second_phone_number', 'fee_payer_number',
            'address', 'profile_pic', 'examination_number', 'previously_examination_number',
            'physical_disabilities_condition', 'branch', 'service'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'current_class': forms.Select(attrs={'class': 'form-control select2bs4'}),
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
            'service': forms.SelectMultiple(attrs={'class': 'form-control select2bs4'}),
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
