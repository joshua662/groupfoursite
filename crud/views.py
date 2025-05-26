from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.auth import logout
from django.urls import reverse
from .forms import ChangePasswordForm
from django.core.paginator import Paginator

def login_view(request):
    try:
        if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.grt('password')
        
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                request.session('userId') = user.user_id
                request.sesion('username') = user.username
                request.sesion('is_auntheticated') = True
                
                messages.success(request, f'Welcome {user.full_name}|')
                return redirect('/gender/list')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('/login/?error=1')
        except user.DoesNotexist:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/?error=1')
        
        else:
            return render(request, 'layout/Login.html')
    except Exception as e:
        messages.error(request, f'An error occured: {str(e)}')
        return redirect('/login/?error=1')

@login_required_custom
def gender_list(request):
    try:
        genderObj = Genders.objects.all()
        data = {'genders': genderObj}
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required_custom
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender', '').strip()
            if not gender:
                messages.error(request, 'Gender field is required.')
                return render(request, 'gender/AddGender.html')
            if Genders.objects.filter(gender__iexact=gender).exists():
                messages.error(request, 'This gender already exists.')
                return render(request, 'gender/AddGender.html')
            Genders.objects.create(gender=gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('gender_list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')

@login_required_custom
def edit_gender(request, genderId):
    gender = get_object_or_404(Genders, pk=genderId)
    if request.method == 'POST':
        new_gender = request.POST.get('gender', '')
        if new_gender:
            gender.gender = new_gender
            gender.save()
            messages.success(request, 'Gender updated successfully!')
            return redirect('gender_list')
        else:
            messages.error(request, 'Gender name cannot be empty.')
    return render(request, 'gender/EditGender.html', {'gender': gender})

@login_required_custom
def edit_user(request, user_id):
    userObj = Users.objects.get(pk=user_id)
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date', '')
        address = request.POST.get('address', '')
        contact_number = request.POST.get('contact_number', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')

        if Users.objects.filter(username=username).exclude(pk=user_id).exists():
            messages.error(request, 'A user with this username already exists.')
            return redirect('edit_user', user_id=user_id)
        if Users.objects.filter(email=email).exclude(pk=user_id).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('edit_user', user_id=user_id)

        if new_password or confirm_new_password:
            if new_password != confirm_new_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('edit_user', user_id=user_id)
            for user in Users.objects.exclude(pk=user_id):
                if check_password(new_password, user.password):
                    messages.error(request, 'This password is already used by another user. Please choose a different password.')
                    return redirect('edit_user', user_id=user_id)
            userObj.password = make_password(new_password)
            messages.success(request, 'Password changed successfully!')

        userObj.full_name = full_name
        userObj.gender = Genders.objects.get(pk=gender)
        userObj.birth_date = birth_date
        userObj.address = address
        userObj.contact_number = contact_number
        userObj.email = email
        userObj.username = username
        userObj.save()

        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
    else:
        genders = Genders.objects.all()
        return render(request, 'user/EditUser.html', {'user': userObj, 'genders': genders})

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

@login_required_custom
def add_user(request):
    try:
        if request.method == 'POST':
            full_name = request.POST.get('full_name', '')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date', '')
            address = request.POST.get('address', '')
            contact_number = request.POST.get('contact_number', '')
            email = request.POST.get('email', '')  # Email is optional
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if Users.objects.filter(username=username).exists():
                messages.error(request, 'A user with this username already exists.')
                return render(request, 'user/AddUser.html', {'genders': Genders.objects.all()})

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'clear_password': True  # Use this in your template to clear fields
                })

            Users.objects.create(
                full_name=full_name,
                gender=Genders.objects.get(pk=gender),
                birth_date=birth_date,
                address=address,
                contact_number=contact_number,
                email=email,
                username=username,
                password=make_password(password),
            )
            messages.success(request, 'User added successfully!')
            return redirect('user_list')
        else:
            genders = Genders.objects.all()
            return render(request, 'user/AddUser.html', {'genders': genders})
    except Exception as e:
        messages.error(request, f'Error occurred: {e}')
        return redirect('add_user')
    
@login_required_custom
def delete_gender(request, gender_id):
    try:
        gender = Genders.objects.get(pk=gender_id)
        if request.method == 'POST':
            gender.delete()
            messages.success(request, 'Gender deleted successfully!')
            return redirect('gender_list')
        return render(request, 'gender/DeleteGender.html', {'gender': gender})
    except Genders.DoesNotExist:
        messages.error(request, 'Gender not found.')
        return redirect('gender_list')

@login_required_custom
def delete_user(request, user_id):
    try:
        userObj = Users.objects.get(pk=user_id)
        if request.method == 'POST':
            userObj.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('user_list')
        return render(request, 'user/DeleteUser.html', {'user': userObj})
    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')

@login_required_custom
def change_password(request, user_id):
    userObj = Users.objects.get(pk=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')
        if not new_password or not confirm_new_password:
            messages.error(request, 'Please fill in all password fields.')
            return redirect('change_password', user_id=user_id)
        if new_password != confirm_new_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('change_password', user_id=user_id)
        for user in Users.objects.exclude(pk=user_id):
            if check_password(new_password, user.password):
                messages.error(request, 'This password is already used by another user. Please choose a different password.')
                return redirect('change_password', user_id=user_id)
        userObj.password = make_password(new_password)
        userObj.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('user_list')
    return render(request, 'user/ChangePassword.html', {'user': userObj})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if Users.objects.filter(username=username).exists():
            messages.error(request, 'A user with this username already exists.')
            return render(request, 'layout/Signup.html')
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'layout/Signup.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'layout/Signup.html')

        Users.objects.create(
            full_name=full_name,
            email=email,
            username=username,
            password=make_password(password),
        )
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    return render(request, 'layout/Signup.html')