import json
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from django.core.cache import cache
import ipaddress
import logging
from user_agents import parse


logger = logging.getLogger('ip-monitoring-tool')

def get_device_info(request):
     user_agent_string = request.META.get('HTTP_USER_AGENT', '')
     user_agent = parse(user_agent_string)
     return f'(device: {user_agent})'


def generateContext(selected_option, blocklist, form):
     selected_option_label = dict(form.fields['select_choice'].choices).get(selected_option)
     blocklist_json = json.dumps(blocklist)
     context = {
               "blocklist": blocklist_json,
               'section': 'dashboard',
               'form': form,
               'selected_option': selected_option,
               'selected_label': selected_option_label,
          }
     return context


def handle_invalid_login_attempt(request):
    device_info = get_device_info(request)
    username = request.POST.get('username', 'Anonymous')
    user_ip = user_ip = get_user_ip(request)
    key = f'login_attempts:{user_ip}'
    attempts = cache.get(key, 0)
    MAX_LOGIN_ATTEMPTS_PER_HOUR = 5

    if attempts >= MAX_LOGIN_ATTEMPTS_PER_HOUR:
     #    messages.error(request, "Too many failed login attempts. Try again later.")
     
        return render(request, 'registration/too_many_attempts.html', status=403)
    else:
        cache.set(key, attempts + 1, 3600)
        messages.error(request, "Invalid username or password.")
        logger.error(f"401 Unauthorised {user_ip} {username} {request.path} {device_info}")


def check_file(file, renu_ips, blocklist, site):
    with open(file, 'r') as file:
               for line in file.readlines():
                    ip_address = ipaddress.ip_address(line.strip())
                    for entry in renu_ips:
                         if ip_address in ipaddress.ip_network(entry):
                              blocklist.append({"ip": str(ip_address), "source": site})


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
