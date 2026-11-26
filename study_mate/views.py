from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import StudyMaterialForm, SubjectForm
from .models import Subject
from django.db.models import Q

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


@login_required(login_url='login')
def subjects_view(request):
    subjects = Subject.objects.filter(user=request.user)
    search_query = request.GET.get("q", "").strip()
    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    semester = request.GET.get("semester", "")
    if semester in ["winter", "summer"]:
        subjects = subjects.filter(semester__iexact=semester)
        
    sort = request.GET.get("sort", "recent")
    if sort == "name":
        subjects = subjects.order_by("name")
    else:
        subjects = subjects.order_by("-created_at")

    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject_name = form.cleaned_data["name"]
            
            if Subject.objects.filter(user=request.user, name__iexact=subject_name).exists():
                messages.error(request, "You already have a subject with this name.")
            else:
                subject = form.save(commit=False)
                subject.user = request.user
                subject.save()

                messages.success(request, "Subject added successfully.")
                return redirect("subjects")
    else:
        form = SubjectForm()

    context = {
            "subjects": subjects,
            "form": form,
            "search_query": search_query,
            "selected_semester": semester,
            "sort": sort,
                    }
    return render(request, "study_mate/subjects.html", context)


@login_required(login_url='login')
def subject_detail_view(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user)
    return render(request,
                  "study_mate/subject_detail.html",
                  {"subject": subject}
                  )

@login_required(login_url='login')
def upload_study_material_view(request):
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            allowed_extensions = ['.pdf', '.docx']
            file_name = material.file.name.lower()
           
            if material.file.size > 10 * 1024 * 1024:  # 10 MB limit
               form.add_error('file', "File size exceeds the 10MB limit.")
            elif not file_name.endswith(allowed_extensions):
                form.add_error('file', "Only PDF files and DOCX files are allowed.")
            else:
                material.save()
                messages.success(request, "Study material uploaded successfully.")
                return redirect("subject_detail", subject_id=material.subject.id)    
    else:
        form = StudyMaterialForm(user=request.user)
    return render(request, "study_mate/upload_study_material.html", {"form": form})