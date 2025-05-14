from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender, Users
from django.contrib.auth.hashers import make_password

# Create your views here.

def gender_list(request):
    try:
        genders = Gender.objects.all()
        
        data = {
            'genders': genders
        }
        
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

def add_gender(request):  
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Gender.objects.create(gender=gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add gender: {e}')
    
def edit_gender(request, genderId):
    try:
        genderObj = Gender.objects.get(pk=genderId)
        
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            genderObj.gender = gender
            genderObj.save()
            
            messages.success(request, 'Gender updated successfully!')
            
            
            data = {
            'gender': genderObj
        }
            
            return redirect('gender_list')
            
        data = {
            'gender': genderObj
        }
        
        return render(request, 'gender/EditGender.html', data)
    
    except Exception as e:
        return HttpResponse(f'Error occurred during edit: {e}')
    
def delete_gender(request, genderId):
   try:
    if request.method == 'POST':
        genderObj = Gender.objects.get(pk=genderId)
        genderObj.delete()
        
        messages.success(request, 'Gender deleted successfully!')
        return redirect('/gender/list')
    else:
        genderObj = Gender.objects.get(pk=genderId)
        
        data = {
            'gender': genderObj
        }
        
        return render(request, 'gender/DeleteGender.html', data)
   except Exception as e:
       return HttpResponse(f"Error occurred during delete: {e}")
   
   
def user_list(request):
    try:
        users = Users.objects.all()
        return render(request, 'user/UsersList.html', {'users': users})
    except Exception as e:
        messages.error(request, f'Error occurred during load users: {e}')
        return redirect('/user/list/')
    
def add_user(request):
    try:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if not all([full_name, gender, birth_date, address, contact_number, username, password, confirm_password]):
                messages.error(request, 'All fields are required!')
                return redirect('/user/add/')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect('/user/add/')
            
            if Users.objects.filter(full_name=full_name).exists():
                messages.error(request, f'A user with the name "{full_name}" already exists!')
                return redirect('/user/add/')
        
            Users.objects.create(
                full_name=full_name,
                gender=Gender.objects.get(pk=gender),
                birth_date=birth_date,
                address=address,
                contact_number=contact_number,
                email=email,
                username=username,
                password=make_password(password),
            ).save()
            
            messages.success(request, 'User added successfully!')
            return redirect('/user/add/')
        else:        
            genderObj = Gender.objects.all()
        
            data = {
                'genders': genderObj
            }
        
            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        messages.error(request, f'Error occurred during add user: {e}')
        return redirect('/user/add/')
def delete_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()
            
            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list/')
        else:
            userObj = Users.objects.get(pk=userId)
            
            data = {
                'user': userObj
            }
            
            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        messages.error(request, f'Error occurred during delete: {e}')
        return redirect('/user/list/')
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if not all([full_name, gender, birth_date, address, contact_number, username]):
                messages.error(request, 'All fields are required!')
                return redirect(f'/user/edit/{userId}/')
            
            if password and confirm_password:
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match!')
                    return redirect(f'/user/edit/{userId}/')
                userObj.password = make_password(password)
            
            # Check for duplicate full name (excluding the current user)
            if Users.objects.filter(full_name=full_name).exclude(pk=userId).exists():
                messages.error(request, f'A user with the name "{full_name}" already exists!')
                return redirect(f'/user/edit/{userId}/')
            
            userObj.full_name = full_name
            userObj.gender = Gender.objects.get(pk=gender)
            userObj.birth_date = birth_date
            userObj.address = address
            userObj.contact_number = contact_number
            userObj.email = email
            userObj.username = username
            userObj.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list/')
            
        data = {
            'user': userObj,
            'genders': Gender.objects.all()
        }
        
        return render(request, 'user/EditUser.html', data)
    
    except Exception as e:
        messages.error(request, f'Error occurred during edit: {e}')
        return redirect('/user/list/')