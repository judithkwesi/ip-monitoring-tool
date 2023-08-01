import ipaddress

def check_for_renu_ip():
      renu_ips = ['196.43.128.0/18', '137.63.128.0/17', '102.34.0.0/16', '2.56.192.0/22']
      read_normalised_file2("./sites/blocklist.txt", renu_ips)

def read_normalised_file2(input_file, ips):
    with open(input_file, 'r') as file:
        for line in file.readlines():
            is_blacklisted(line.strip(), ips)


def is_blacklisted(ip, renu_ips):
    ip_address = ipaddress.ip_address(ip)
    for entry in renu_ips:
        if ip_address in ipaddress.ip_network(entry):
            # return True
            print(ip_address)
    return False

check_for_renu_ip()