from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.


def signup_view(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        terms = request.POST.get("terms")

    # Validation for empty fields
        if not full_name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "study_mate/signup.html")

        if not terms:
            messages.error(request, "Please accept the Terms & Conditions.")
            return render(request, "study_mate/signup.html")

    # Check duplicate email
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, "study_mate/signup.html")

    # Check Password matching
        if password != confirm_password:
            messages.error(request, "Password do not match.")
            return render(request, "study_mate/signup.html")

        try:
            validate_password(password)
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)
            return render(request, "study_mate/signup.html")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
        )

        messages.success(request, "Account created sucessfully.Please log in.")
        return redirect("signup")

    return render(request, "study_mate/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        remember = request.POST.get("remember")

        if not email or not password:
            messages.error(request, "Please enter email and password.")
            return render(request, "study_mate/login.html")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
                
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "study_mate/login.html")

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, "study_mate/dashboard.html")

@login_required(login_url='login')
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
