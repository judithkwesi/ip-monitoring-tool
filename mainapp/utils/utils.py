import json
import ssl
from django.contrib import messages
from django.shortcuts import render
from django.core.cache import cache
import ipaddress
import logging

import requests
from mainapp.utils.constants import OutputFile
from user_agents import parse
from mainapp.models import IPSpace
from mainapp.check_for_renu_ip import identify_blacklisted_ip_addresses
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings


auth_logger = logging.getLogger('auth')

def get_device_info(request):
    """
        This returns information about the users device in logs,
        params(object): request
        return(string): device: Device name, Browser name and version
    """
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    return f'(device: {user_agent})'


def generateContext(request, selected_option, blocklist, form):
     selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)
     blocklist_json = json.dumps(blocklist)
     my_ip = get_user_ip(request)
     context = {
               "blocklist": blocklist_json,
               'section': 'dashboard',
               'form': form,
               'selected_option': selected_option,
               'selected_label': selected_option_label,
               'my_ip': my_ip
          }
     return context


def handle_invalid_login_attempt(request, attempts, MAX_LOGIN_ATTEMPTS_PER_HOUR, username):
    device_info = get_device_info(request)
    user_ip = user_ip = get_user_ip(request)

    if attempts == MAX_LOGIN_ATTEMPTS_PER_HOUR - 1:
        messages.info(request, "You are left with 1 attempt!.")
    else:
        messages.error(request, "Invalid username or password.")
    auth_logger.error(f"401 Unauthorised {user_ip} {username} {request.path} {device_info}")


def check_file(file, renu_ips, blocklist, site):
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file, 'r') as file:
               for line in file.readlines():
                    ip_address = ipaddress.ip_address(line.strip())
                    for entry in renu_ips:
                         if ip_address in ipaddress.ip_network(entry):
                              blocklist.append({"ip": str(ip_address), "timestamp": f"{ current_timestamp }", "source": site})
                              send_response_email(ip_address)


def send_response_email(ip):
    subject = "RENU IP Found in List"
    message = f"The IP {ip} was found in the list."
    from_email = 'renutest100@gmail.com'
    recipient_list = ["charleskasasira01@gmail.com"]
    send_mail(subject, message, from_email, recipient_list)



def get_user_ip(request):
    """
        Get the users id address
        params: request
        return(string): ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_my_ip():
    try:
        response = requests.get("https://ipinfo.io/ip")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return ""
    except Exception as e:
        return ""



def process_and_store_blacklist():
    all_ips = IPSpace.objects.all()
    renu_ips = [ip_obj.ip_space for ip_obj in all_ips]
    blocklist = []

    check_file(OutputFile.CINS, renu_ips, blocklist, "CINS")
    check_file(OutputFile.BLOCKLIST, renu_ips, blocklist, "Blocklist.de")
    check_file(OutputFile.ABUSEIPDB, renu_ips, blocklist, "AbuseIPDB")

    try:
        for ip_space in renu_ips:
            if ":" in ip_space:
                identify_blacklisted_ip_addresses(OutputFile.SPAMHAUSV6, ip_space, blocklist, "Spamhaus")
            else:
                identify_blacklisted_ip_addresses(OutputFile.SPAMHAUS, ip_space, blocklist, "Spamhaus")
    except Exception as e:
         print("Error just")

    # Write blocklist data to a JSON file
    with open(OutputFile.BLACKLIST, 'w') as blacklist_file:
        json.dump(blocklist, blacklist_file)



def get_blacklist_from_file():
    blocklist = []
    with open(OutputFile.BLACKLIST, 'r') as blacklist_file:
        blocklist = json.load(blacklist_file)
    return blocklist


