from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from result_module.models import Staffs


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user       
       

        if (request.path == reverse("login") or
            request.path == reverse("DoLogin") or         
            request.path == reverse("logout_user") or
            modulename.startswith("django.contrib.auth.views")):           
            return None

        if user.is_authenticated:            
            
            if user.user_type == "1":                
                if modulename in ["result_module.HodViews", "result_module.views", "django.views.static", "result_module.Delete"]:                    
                    return None
                else:                    
                    return HttpResponseRedirect(reverse("admin_home"))
            
            elif user.user_type == "2":                
                staff = Staffs.objects.filter(admin=user).first()
                
                if staff:                   
                    
                    if staff.staff_role == "Accountant":
                        allowed_modules = ["result_module.AccountantViews", "django.views.static"]
                        if modulename in allowed_modules:                            
                            return None
                        else:                            
                            return HttpResponseRedirect(reverse("accountant_home"))
                        
                    elif staff.staff_role == "Academic":
                        allowed_modules = ["result_module.AcademicViews", "django.views.static"]
                        if modulename in allowed_modules:                            
                            return None
                        else:                            
                            return HttpResponseRedirect(reverse("academic_home"))
                    
                    elif staff.staff_role == "Admin":
                        allowed_modules = [
                            "result_module.HodViews",
                            "result_module.Delete",                        
                            "result_module.imports",                        
                            "result_module.ExcelTemplate",                        
                            "result_module.views",                        
                            "django.views.static",
                        ]
                        if modulename in allowed_modules:                            
                            return None
                        else:                           
                            return HttpResponseRedirect(reverse("admin_home"))
                        
                    elif staff.staff_role == "Headmaster":
                        allowed_modules = [
                            "result_module.HeadmasterViews",
                            "result_module.Delete",                        
                            "result_module.imports",                        
                            "result_module.ExcelTemplate",                        
                            "result_module.views",                        
                            "django.views.static",
                        ]
                        if modulename in allowed_modules:                            
                            return None
                        else:                           
                            return HttpResponseRedirect(reverse("headmaster_home"))
                    
                    else:
                        allowed_modules = [
                            "result_module.StaffImports",
                            "result_module.StaffView",
                            "result_module.ExcelTemplate",
                            "result_module.views",
                            "django.views.static",
                        ]
                        if modulename in allowed_modules:                          
                            return None
                        else:                            
                            return HttpResponseRedirect(reverse("staff_home"))

        elif modulename == "result_module.views":            
            return None
        
        # Redirect unauthenticated users to the login page
        
        return HttpResponseRedirect(reverse("login"))
