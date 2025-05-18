from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender, Users
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.auth import logout
from django.urls import reverse
from .forms import ChangePasswordForm
from django.core.paginator import Paginator


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
                    return redirect('/user/list/')  # Redirect to the next page after login
                else:
                    return render(request, 'layout/Login.html', {'error': 'Invalid email or password'})
            except Users.DoesNotExist:
                return render(request, 'layout/Login.html', {'error': 'Invalid email or password'})

        return render(request, 'layout/Login.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during login: {e}')
<<<<<<< HEAD
    
=======

>>>>>>> 389dfe354bc0279e8c07cab4f474dfffb164fd72
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

<<<<<<< HEAD
=======
@login_required_custom
>>>>>>> 389dfe354bc0279e8c07cab4f474dfffb164fd72
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

<<<<<<< HEAD
=======
@login_required_custom    
>>>>>>> 389dfe354bc0279e8c07cab4f474dfffb164fd72
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
    
<<<<<<< HEAD
=======
@login_required_custom    
>>>>>>> 389dfe354bc0279e8c07cab4f474dfffb164fd72
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
        query = request.GET.get('q', '')
        user_list = Users.objects.select_related('gender')
        if query:
            user_list = user_list.filter(full_name__icontains=query)
        paginator = Paginator(user_list, 10)  # 10 users per page
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)
        return render(request, 'user/UsersList.html', {'users': users, 'query': query})
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

            # ...existing field checks...

            # Check for duplicate username
            if Users.objects.filter(username=username).exists():
                errors['username'] = 'A user with this username already exists.'
            # Check for duplicate email (optional)
            if Users.objects.filter(email=email).exists():
                errors['email'] = 'A user with this email already exists.'

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
        userObj = Users.objects.get(pk=user_id)
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            # ...other fields...

            errors = {}

            # Check for duplicate username (exclude current user)
            if Users.objects.filter(username=username).exclude(pk=user_id).exists():
                errors['username'] = 'A user with this username already exists.'
            # Check for duplicate email (exclude current user)
            if Users.objects.filter(email=email).exclude(pk=user_id).exists():
                errors['email'] = 'A user with this email already exists.'

            # ...other validation...

            if errors:
                return render(request, 'user/EditUser.html', {
                    'errors': errors,
                    'user': userObj,
                    'genders': Gender.objects.all(),
                    # ...other fields...
                })

            # Update user fields
            userObj.full_name = fullName
            userObj.gender = Gender.objects.get(pk=gender)
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username
            userObj.save()

            messages.success(request, 'User updated successfully!')
            return redirect('/user/list')
        else:
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
    return redirect('login')

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