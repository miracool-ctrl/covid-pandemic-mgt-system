from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Bed, Doctor, Patient
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Login view
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        messages.error(request, 'Invalid username or password')
    return render(request, 'main/login.html')

# Logout view
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

# Dashboard view
@login_required(login_url='login')
def dashboard(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    patients_recovered = Patient.objects.filter(status="Recovered")
    patients_deceased = Patient.objects.filter(status="Deceased")
    deceased_count = patients_deceased.count()
    recovered_count = patients_recovered.count()
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    context = {
        'patient_count': patient_count,
        'recovered_count': recovered_count,
        'beds_available': beds_available,
        'deceased_count': deceased_count,
        'beds': beds
    }
    return render(request, 'main/dashboard.html', context)

# Add patient view
@login_required(login_url='login')
def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    
    if request.method == "POST":
        try:
            name = request.POST['name']
            phone_num = request.POST['phone_num']
            patient_relative_name = request.POST['patient_relative_name']
            patient_relative_contact = request.POST['patient_relative_contact']
            address = request.POST['address']
            symptoms = request.POST.getlist('symptoms')  # Handle as a list
            prior_ailments = request.POST['prior_ailments']
            bed_num_sent = request.POST['bed_num']
            bed = Bed.objects.get(bed_number=bed_num_sent)
            dob = request.POST['dob']
            status = request.POST['status']
            doctor_id = request.POST['doctor']
            doctor = Doctor.objects.get(id=doctor_id)
            
            # Create Patient
            patient = Patient.objects.create(
                name=name,
                phone_num=phone_num,
                patient_relative_name=patient_relative_name,
                patient_relative_contact=patient_relative_contact,
                address=address,
                symptoms=symptoms,
                prior_ailments=prior_ailments,
                bed_num=bed,
                dob=dob,
                doctor=doctor,
                status=status
            )
            bed.occupied = True
            bed.save()
            return redirect(f"/patient/{patient.id}")

        except KeyError as e:
            return HttpResponse(f"Error: Missing field {e.args[0]}", status=400)
        except Bed.DoesNotExist:
            return HttpResponse("Error: Bed not found", status=404)
        except Doctor.DoesNotExist:
            return HttpResponse("Error: Doctor not found", status=404)
    
    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)

# Patient detail view
@login_required(login_url='login')
def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        try:
            doctor_name = request.POST['doctor']
            doctor_time = request.POST['doctor_time']
            doctor_notes = request.POST['doctor_notes']
            mobile = request.POST['mobile']
            mobile2 = request.POST['mobile2']
            relative_name = request.POST['relativeName']
            address = request.POST['location']
            status = request.POST['status']
            doctor = Doctor.objects.get(name=doctor_name)

            patient.phone_num = mobile
            patient.patient_relative_contact = mobile2
            patient.patient_relative_name = relative_name
            patient.address = address
            patient.doctor = doctor
            patient.doctors_visiting_time = doctor_time
            patient.doctors_notes = doctor_notes
            patient.status = status
            patient.save()
        except Doctor.DoesNotExist:
            return HttpResponse("Error: Doctor not found", status=404)

    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)

# Patient list view with filtering
@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()
    myFilter = PatientFilter(request.GET, queryset=patients)
    patients = myFilter.qs
    context = {
        'patients': patients,
        'myFilter': myFilter
    }
    return render(request, 'main/patient_list.html', context)

# Autosuggest for patients
def autosuggest(request):
    query = request.GET.get('term', '')
    queryset = Patient.objects.filter(name__icontains=query)
    names = [x.name for x in queryset]
    return JsonResponse(names, safe=False)

# Autosuggest for doctors
def autodoctor(request):
    query = request.GET.get('term', '')
    queryset = Doctor.objects.filter(name__icontains=query)
    names = [x.name for x in queryset]
    return JsonResponse(names, safe=False)

# Info page view
def info(request):
    return render(request, "main/info.html")
