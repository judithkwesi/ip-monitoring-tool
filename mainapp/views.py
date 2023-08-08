import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.cache import cache
from .forms import MySelectForm, AddUserForm, AddIPForm, SyncIntervalForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from .models import IPSpace, SyncInterval
from mainapp.utils.utils import generateContext, handle_invalid_login_attempt, check_file
from mainapp.utils.custom_decorators import custom_admin_only, custom_authorised_user


@never_cache
def login_view(request):
     if request.user.is_authenticated:
          return HttpResponseRedirect('/')
     if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in")
            cache.delete(f'login_attempts:{request.META.get("REMOTE_ADDR")}')
            return redirect('dashboard')
        else:
            handle_invalid_login_attempt(request)

     return render(request, 'registration/login.html', {})


@custom_authorised_user
def dashboard(request):
     all_ips = IPSpace.objects.all()
     renu_ips = [ip_obj.ip_space for ip_obj in all_ips]
     blocklist = []

     check_file('./mainapp/sites/cins.txt', renu_ips, blocklist, "CINS")
     check_file('./mainapp/sites/blocklist.txt', renu_ips, blocklist, "Blocklist")

     sorted_data = sorted(blocklist, key=lambda x: x['ip'])

     if request.method == 'POST':
          form = MySelectForm(request.POST)
          if form.is_valid():
               selected_option = form.cleaned_data['select_choice']
               context = generateContext(selected_option, sorted_data, form)

               return render(request, 'registration/dashboard.html', context)
     else:
          form = MySelectForm(initial={'select_choice': 'option1'})
          selected_option = form.initial['select_choice']
          context = generateContext(selected_option, sorted_data, form)

          return render(request, 'registration/dashboard.html', context)
     

@login_required(login_url='login')
def add_ip_space(request):
     if request.method == 'POST':
          form = AddIPForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, f"Successfully added IP space")
               return HttpResponseRedirect('/')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")

            return HttpResponseRedirect('/')
     form = AddIPForm() 

@custom_admin_only
def add_user(request):
     if request.method == 'POST':
          form = AddUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request, "Successfully added user")
               return HttpResponseRedirect('/users')
          else:
            for field, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")

            return HttpResponseRedirect('/users')
     form = AddUserForm()


@custom_admin_only
def update_sync_interval(request):
     if request.method == 'POST':
          form = SyncIntervalForm(request.POST)

          if form.is_valid():
               form.save()
               messages.success(request, "Successfully updated Sync Interval")
               return HttpResponseRedirect('/settings')
          else:
            for _, errors in form.errors.items():
                for error in errors:
                     messages.error(request, f"{error}")

            return HttpResponseRedirect('/settings')

     return HttpResponseRedirect('/settings')


@custom_admin_only
def users(request):
    users = User.objects.all()
    usernames_list = [{"username": user.username, "access_level": user.is_superuser} for user in users]
    data = {"users": usernames_list}
    context = {
         "users": json.dumps(data),
         "section": "users"
    }
    return render(request, 'registration/users.html', context)


@custom_admin_only
def settings(request):
     sync = SyncInterval.objects.all()
     sync_intervals = [ip_obj.sync_interval for ip_obj in sync]

     if sync_intervals:
          sync_interval = int(sync_intervals[-1])
     else:
          sync_interval = 12

     context = {
          "section": "settings",
          "sync_interval": sync_interval
     }
     return render(request, 'registration/settings.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/')


# for testing purposes only


# from django.conf import settings
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import BadHeaderError, send_mail
# from django.db.models import Q
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# # def password_reset_request(request):
# #     if request.method == "POST":
# #         domain = request.headers['Host']
# #         password_reset_form = PasswordResetForm(request.POST)
# #         if password_reset_form.is_valid():
# #             data = password_reset_form.cleaned_data['email']
# #             associated_users = User.objects.filter(Q(email=data))
# #             # You can use more than one way like this for resetting the password.
# #             # ...filter(Q(email=data) | Q(username=data))
# #             # but with this you may need to change the password_reset form as well.
# #             if associated_users.exists():
# #                 for user in associated_users:
# #                     subject = "Password Reset Requested"
# #                     email_template_name = "admin/accounts/password/password_reset_email.txt"
# #                     c = {
# #                         "email": user.email,
# #                         'domain': domain,
# #                         'site_name': 'Interface',
# #                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
# #                         "user": user,
# #                         'token': default_token_generator.make_token(user),
# #                         'protocol': 'http',
# #                     }
# #                     email = render_to_string(email_template_name, c)
# #                     try:
# #                         send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
# #                     except BadHeaderError:
# #                         return HttpResponse('Invalid header found.')
# #                     return redirect("/core/password_reset/done/")
# #     password_reset_form = PasswordResetForm()
# #     return render(request=request, template_name="admin/accounts/password/password_reset.html",
# #                   context={"password_reset_form": password_reset_form})

from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache

# Password Reset View
@never_cache
def password_reset(request):
    return auth_views.PasswordResetView.as_view()(request)

# Password Reset Done View
@never_cache
def password_reset_done(request):
    return auth_views.PasswordResetDoneView.as_view()(request)

# Password Reset Confirm View
@never_cache
def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)

# Password Reset Complete View
@never_cache
def password_reset_complete(request):
    return auth_views.PasswordResetCompleteView.as_view()(request)
