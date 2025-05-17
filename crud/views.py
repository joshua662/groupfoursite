from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender, Users
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.auth import logout
from django.urls import reverse
from .forms import ChangePasswordForm
# from django.contrib.auth.models.User import AbstractBaseUser

def login_view(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = Users.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    return redirect('/user/list')
                else:
                    return render(request, 'layout/LogIn.html', {'error': 'Invalid password'})
            except Users.DoesNotExist:
                messages.warning(request, 'User does not exist.')
                return render(request, 'layout/LogIn.html', {'error': 'User not found'})

        return render(request, 'layout/LogIn.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during login: {e}')

@login_required_custom
def gender_list(request):
    try:
        genderObj = Gender.objects.all()

        data = {
            'genders':genderObj
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required_custom
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Gender.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')

@login_required_custom    
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Gender.objects.get(pk=genderId)

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')
            
            data = {
                'gender': genderObj 
            }
            
            return render(request, 'gender/EditGender.html', data)
        else:
            genderObj = Gender.objects.get(pk=genderId)

            data = {
                'gender': genderObj 
            }

            return render(request, 'gender/EditGender.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')
    
@login_required_custom    
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
        return HttpResponse(f'Error occured during delete gender: {e}')

@login_required_custom
def user_list(request):
    try:
        userObj = Users.objects.select_related('gender')

        data = {
            'users':  userObj
        }

        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

def add_user(request):
    try:
        errors = {}
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date', '')
            address = request.POST.get('address', '')
            contact_number = request.POST.get('contact_number', '')
            email = request.POST.get('email', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not full_name:
                errors['full_name'] = 'Full Name is required.'
            if not gender:
                errors['gender'] = 'Gender is required.'
            if not birth_date:
                errors['birth_date'] = 'Birth Date is required.'
            if not address:
                errors['address'] = 'Address is required.'
            if not contact_number:
                errors['contact_number'] = 'Contact Number is required.'
            if not username:
                errors['username'] = 'Username is required.'
            if not password:
                errors['password'] = 'Password is required.'
            if not confirm_password:
                errors['confirm_password'] = 'Confirm Password is required.'
            elif password != confirm_password:
                errors['confirm_password'] = 'Passwords do not match.'

            if not errors:
                Users.objects.create(
                    full_name=full_name,
                    gender=Gender.objects.get(pk=gender),
                    birth_date=birth_date,
                    address=address,
                    contact_number=contact_number,
                    email=email,
                    username=username,
                    password=make_password(password),
                )

                messages.success(request, 'User added successfully!')
                return redirect('/user/list')
            else:
                genderObj = Gender.objects.all()
                return render(request, 'user/AddUser.html', {
                    'errors': errors,
                    'genders': genderObj,
                    'full_name': full_name,
                    'gender': gender,
                    'birth_date': birth_date,
                    'address': address,
                    'contact_number': contact_number,
                    'email': email,
                    'username': username,
                    'password': password,
                    'confirm_password': confirm_password
                })

        else:
            genderObj = Gender.objects.all()
            return render(request, 'user/AddUser.html', {'genders': genderObj})

    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')
 
def edit_user(request, user_id):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=user_id)
            user_id = request.POST.get('user_id')
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')

            userObj.user_id = user_id
            userObj.full_name = fullName
            userObj.gender = Gender.objects.get(pk=gender)
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email

            userObj.save()

            messages.success(request, 'User updated successfully!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=user_id)

            data = {
                'user': userObj,
                'genders': Gender.objects.all()
            }

            return render(request, 'user/EditUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during edit user: {e}')


def delete_user(request, user_id):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=user_id)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')
        else:
            userObj = Users.objects.get(pk=user_id)

            data = {
                'user': userObj
            }

            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during delete user: {e}')

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

def change_password(request, user_id):
    userObj = get_object_or_404(Users, pk=user_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            userObj.password = make_password(new_password)
            userObj.save()
           
            messages.success(request, 'Password changed successfully!')
            return redirect('user/edit')
    else:
        form = ChangePasswordForm()

    context = {
        'user': userObj,
        'form': form,
    }
    return render(request, 'user/ChangePassword.html', context)