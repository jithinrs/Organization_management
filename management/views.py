from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm
from .models import MyUser, Organization


@login_required(login_url='signup')
def home_page(request):
    if request.method == 'GET':
        print(request.user)
        is_admin = False
        if request.user.is_org_admin:
            is_admin = True
        organization_name = 'Global'
        if request.user.organization:
            organization_name = request.user.organization.name
        context = {
            'is_admin' : is_admin,
            'organization' : organization_name

        }
        return render(request, 'main.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('valid form')
            user = form.save(commit=False)
            email_domain = (user.email.split('@')[1])
            organization = Organization.objects.filter(email_domain=email_domain).first()
            if organization:
                user.organization = organization
                if user.email == organization.organization_email:
                    user.is_org_admin = True
                MyUser.objects.filter(email_domain=email_domain, organization=Organization.objects.filter(name='Global').\
                                                       first()).update(organization=organization)
            else:
                user.organization = Organization.objects.filter(name='Global').first()
            user.email_domain = email_domain
            user.set_password(request.POST['password'])
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'log_sign.html', {'form' : form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(email = request.POST['email'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('homepage')
    return redirect('signup')



def log_out(request):
    if request.method == 'POST':
        logout(request)
        print('user logged out')
    return redirect('signup')


def create_user(request):
    if request.user.is_org_admin == True:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                org_id = Organization.objects.filter(organization_email=request.user.email).first()
                print(org_id , type(org_id))
                user.organization = org_id
                user.set_password(request.POST['password'])
                user.save()
                messages.success(request,'user_created')
                return redirect('homepage')

            else:
                print(form.errors)
                messages.error(request,'something went wrong. try again after some time')
    return redirect('homepage')