
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout,login
from result_module.emailBackEnd import EmailBackend
from result_module.forms import AddStaffForm
from result_module.models import CustomUser, Staffs
from django.core.mail import send_mail
from django.core.exceptions import  ValidationError
from django.views.decorators.csrf import csrf_exempt

def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("login"))

def ShowLogin(request):  
  return render(request,'login.html')

def landing_page(request):  
  return render(request,'index.html')

def add_staff(request):  
    form = AddStaffForm() 
    return render(request,"add_staff.html",{"form":form})    
    
def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    form = AddStaffForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            gender = form.cleaned_data["gender"]
            middle_name = form.cleaned_data["middle_name"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            date_of_employment = form.cleaned_data["date_of_employment"]
            address = form.cleaned_data["address"]
            branch = form.cleaned_data["branch"]
            staff_role = form.cleaned_data["staff_role"]
          

            # Check if email or username already exists
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Email already exists. Try another email or contact the administrator for support")

            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError("Username already exists. Try another username or contact the administrator for support")

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2  # Adjust this based on your user model setup
            )
            user.staffs.middle_name = middle_name
            user.staffs.gender = gender
            user.staffs.phone_number = phone_number
            user.staffs.staff_role = staff_role
            user.staffs.branch = branch
            user.staffs.address = address
            user.staffs.date_of_employment = date_of_employment
            user.staffs.date_of_birth = date_of_birth
            user.staffs.profile_pic=form.cleaned_data.get("profile_pic")
            # Add subjects to the staff
      

            user.is_active = False  # Deactivate account until admin activates it
            user.save()

            # Send email to the user
            send_mail(
                'Welcome to HORIZON - Account Creation Successful',
                f'Dear {first_name} {last_name},\n\n'
                'We are excited to inform you that your account has been successfully created on HORIZON. However, before you can log in, your account needs to be activated by the administrator.\n\n'
                'Please note the following:\n'
                '1. Your account will be reviewed and activated by the administrator shortly.\n'
                '2. If the activation takes too long, please feel free to contact the administrator for assistance.\n'
                '3. You will receive an email notification once your account is activated or if any additional information is required.\n\n'
                'Thank you for joining our community!\n\n'
                'Best regards,\n'
                'MRISHO HAMISI\n'
                'HORIZON Academy Team\n\n'
                'Note: This is an automated message. Please do not reply directly to this email.',
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Account created successfully! Please check your email for activation instructions.")
            return HttpResponseRedirect(reverse("success_page"))  # Redirect to a success page

        except ValidationError as ve:
            messages.error(request, str(ve))
            return HttpResponseRedirect(reverse("add_staff"))
        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Failed to save staff {e}")
            return HttpResponseRedirect(reverse("add_staff"))

    else:
        messages.error(request, "Failed to save staff")
        return render(request, "add_staff.html", {"form": form})

def account_creation_success(request):
    return render(request, 'success_page.html')

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_object = CustomUser.objects.filter(email=email).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)
    
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_object = CustomUser.objects.filter(username=username).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)



def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not allowed</h2>")
    else:
        # Authenticate user using EmailBackend
        user = EmailBackend.authenticate(request, request.POST.get("email"), request.POST.get("password"))
        
        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is not active. Please contact the administrator for support.")
                return HttpResponseRedirect(reverse("login"))

            login(request, user)

            # Redirect based on user type
            if user.user_type == "1":  # Admin user
                return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2":  # Staff user
                # Retrieve the staff role
                try:
                    staff = Staffs.objects.get(admin=user)
                    # Redirect based on staff role
                    if staff.staff_role == "Accountant":
                        return HttpResponseRedirect(reverse("accountant_home"))
                    elif staff.staff_role == "Admin":
                        return HttpResponseRedirect(reverse("admin_home"))
                    elif staff.staff_role == "Academic":
                        return HttpResponseRedirect(reverse("academic_home"))
                    elif staff.staff_role == "Headmaster":
                        return HttpResponseRedirect(reverse("headmaster_home"))
                    elif staff.staff_role == "Class Teacher":
                        return HttpResponseRedirect(reverse("class_teacher_home"))
                    else:
                        messages.error(request, "Your role is not recognized. Please contact the administrator.")
                        return HttpResponseRedirect(reverse("login"))
                except Staffs.DoesNotExist:
                    messages.error(request, "Staff profile not found. Please contact the administrator.")
                    return HttpResponseRedirect(reverse("login"))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "wrong email or password")
            return HttpResponseRedirect(reverse("login"))
    


