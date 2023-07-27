#Telling django to render the views .html file

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
import subprocess
from django.contrib.auth.models import User


# Create your views here. 

@login_required(login_url='login')
def dashboard(request):   #Main screen
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})

@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    return render(request, 'registration/users.html', {'users': users})

@login_required(login_url='login')
def settings(request):
    return render(request, 'registration/settings.html', {'section': 'settings'})

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	messages.success(request, ('Successful logged out!'))
        
	response = HttpResponse()
	response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response['Pragma'] = 'no-cache'
	response['Expires'] = '0'
	return redirect('login')

def download_sites_file(request):
    # Sites url
    spam_url = "https://www.spamhaus.org/drop/drop.txt"
    block_url = "https://lists.blocklist.de/lists/all.txt"
    cins_url = "http://cinsscore.com/list/ci-badguys.txt"
    
		# Output path
    block_output_file = "./sites/blocklist.txt"
    spam_output_file = "./sites/spamhaus.txt"
    cins_output_file = "./sites/cins.txt"

    # Use wget to download the file
    download_spamhaus = f"wget -O {spam_output_file} {spam_url}"
    download_block = f"wget -O {block_output_file} {block_url}"
    download_cins_url = f"wget -O {cins_output_file} {cins_url}"

    subprocess.call(download_spamhaus, shell=True)
    subprocess.call(download_block, shell=True)
    subprocess.call(download_cins_url, shell=True)

    return "Done"
