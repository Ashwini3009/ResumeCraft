from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedFile
from .forms import UploadFileForm
from .functions import load_job_criteria, analyze_resume, calculate_score, generate_feedback, generate_appreciation
import os
from django.conf import settings
from django.templatetags.static import static 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .forms import SignupForm
from django.contrib import messages
from datetime import datetime
from .models import User
import json

# Create your views here.
def check_login(request):
    # Check if the user is logged in by looking for a session value
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not logged in
    return True


def login_required_custom(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('upload_file')
#     else:
#         form = UploadFileForm()
#     files = UploadedFile.objects.all()
#     return render(request, 'upload_file.html', {'form': form, 'files': files})

def landing(request):
    return render(request, "LandingPage.html")


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user session data
    return redirect('login')  # Redirect to the login page after logout




#Login view
# def login(request):
#     return render(request,"login.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get user by email
            user = User.objects.get(email=email)

            # Check if the password matches the hashed password
            if check_password(password, user.password):
                # Login successful, store user session
                request.session['user_id'] = user.email
                return redirect('landing')  # Redirect to the home page or dashboard
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist")
        
        return redirect('login')  # Stay on the login page if login failed

    return render(request, 'login.html')


#Login View Code ends here




# Signup view
# def signup(request):
#     return render(request, 'signup.html') 

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(user.password)  # Hash the password before saving
#             user.save()
#             messages.success(request, "Your account has been created successfully.")
#             return redirect('login')  # Redirect to login page after successful signup
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = SignupForm()

#     return render(request, 'signup.html', {'form': form})


def signup(request):
    if request.method == "POST":
        # Initialize the form with POST data
        form = SignupForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Clean the data from the form
            cleaned_data = form.cleaned_data
            first_name = cleaned_data['first_name']
            last_name = cleaned_data['last_name']
            contact_number = cleaned_data['contact_number']
            email = cleaned_data['email']
            dob = cleaned_data['dob']
            password = cleaned_data['password']

            # Hash the password before saving
            hashed_password = make_password(password)

            # Calculate the age based on the date of birth
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Create a new user object
            user = User(
                first_name=first_name,
                last_name=last_name,
                contact_number=contact_number,
                email=email,
                dob=dob,
                age=age,  # Age is calculated manually here
                password=hashed_password  # Store the hashed password
            )

            # Save the new user to the database
            user.save()

            # Redirect to the login page after successful signup
            return redirect('login')

        else:
            # If the form is not valid, render the page again with form errors
            return render(request, 'signup.html', {'form': form})

    else:
        # If GET request, initialize an empty form
        form = SignupForm()

    # Render the signup page with the form
    return render(request, 'signup.html', {'form': form})


# Here the Signup View Ends




# Templates view starting here
@login_required_custom
def resume_templates(request):
    # Define the path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'ATS_Project_Mini','static', 'data', 'templates.json')
    
    # Read the JSON file and load the data
    with open(json_file_path, 'r') as file:
        templates = json.load(file)
    # templates = [
    #     {
    #     "name": "Modern Resume",
    #     "image": "img/template1.png",  # Adjusted image path
    #     "file": "files/template1.docx",  # Adjusted file path
    #     "description": "A sleek and professional resume template suitable for all industries.",
    # },
    # {
    #     "name": "Creative Resume",
    #     "image": "img/template2.png",  # Adjusted image path
    #     "file": "files/template2.docx",  # Adjusted file path
    #     "description": "Perfect for creatives, this resume showcases design and innovation.",
    # },
    # {
    #     "name": "Minimalist Resume",
    #     "image": "img/template3.png",  # Adjusted image path
    #     "file": "files/template3.docx",  # Adjusted file path
    #     "description": "A clean and simple layout ideal for professionals with less experience.",
    # },
    #     # Add more templates as needed
    # ]
    return render(request, "templates.html", {"templates": templates})

@login_required_custom
def editableTemplates(request):
    # Define the path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'ATS_Project_Mini','static', 'data', 'editableTemplates.json')
    
    # Read the JSON file and load the data
    with open(json_file_path, 'r') as file:
        templates = json.load(file)
    
    return render(request, "editTemplates.html", {"templates": templates})


# About us views
# @login_required
@login_required_custom
def about_us(request):
    print(request.user.is_authenticated)
    if check_login(request):  # Make sure user is logged in
        return render(request, 'aboutUs.html')
    return redirect('login')
    


# templates view ends here
@login_required_custom
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            uploaded_file = form.save()

            # Get the file path of the uploaded file
            file_path = uploaded_file.file.path  # Django automatically saves files in MEDIA_ROOT
            print(f"File path after upload: {file_path}")
            try:
                # Process the uploaded resume using ATS algorithm
                print("***********************--------------------************************")
                print(f"File path passed to ats_algorithm: {file_path}")  # Debug print

                score, feedback_path = ats_algorithm(file_path)
                feedback_url = settings.MEDIA_URL + feedback_path
                print("***********************--------------------************************")

                # Display the score and feedback path to the user
                return render(request, 'upload_file.html', {
                    'form': form,
                    'score': score,
                    'feedback_path': feedback_url,
                    'files': UploadedFile.objects.all()
                })
            except FileNotFoundError as e:
                # Handle file not found errors
                return render(request, 'upload_file.html', {
                    'form': form,
                    'error': f"File not found: {str(e)}",
                    'files': UploadedFile.objects.all()
                })

            except Exception as e:
                # Handle any errors in processing the file
                return render(request, 'upload_file.html', {
                    'form': form,
                    'error': f"Error processing the file: {str(e)}",
                    'files': UploadedFile.objects.all()
                })
    else:
        form = UploadFileForm()

    # Initial render with no score
    return render(request, 'upload_file.html', {
        'form': form,
        'files': UploadedFile.objects.all()
    })



@login_required_custom
def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response



# View to pass resume to Analyzer Framework

def ats_algorithm(filepath):
    # Ensure the path to job_criteria.json is correct
    job_criteria_path = os.path.join(settings.BASE_DIR, 'ATS_Project_Mini', 'static', 'job_criteria.json')
    print("---------------------------------*************************---------------------------")

    print(f"Job criteria path: {job_criteria_path}")
    print("---------------------------------*************************---------------------------")
     # Ensure the file exists before loading it
    if not os.path.exists(job_criteria_path):
        raise FileNotFoundError(f"The job_criteria.json file was not found at {job_criteria_path}")
    
    job_criteria = load_job_criteria(job_criteria_path)
    print('Job Criters is executed',job_criteria)
    print("-------------------------------------------------------------------------------")
    results, text = analyze_resume(filepath, job_criteria)
    print('Result is executed',results)
    print("-------------------------------------------------------------------------------")
    score = calculate_score(results, job_criteria)
    feedback_file = generate_feedback(results)
    appreciation_file = generate_appreciation(results)
    return score, feedback_file






# Views for the Editable Resume templates

@login_required_custom
def beginResume(request):
    return render(request,'beginResume.html')

@login_required_custom
def beginResume1(request):
    return render(request,'beginResume1.html')

@login_required_custom
def beginResume2(request):
    return render(request,'beginResume2.html')

@login_required_custom
def editTemplates(request):
    return render(request,'editTemplates.html')