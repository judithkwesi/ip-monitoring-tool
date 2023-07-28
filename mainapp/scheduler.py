from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import ipaddress

def updater():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_sites_file, 'interval', hours=12)
    scheduler.start()

def download_sites_file():
    print("running")
    # Sites url
    block_url = "https://lists.blocklist.de/lists/all.txt"
    cins_url = "http://cinsscore.com/list/ci-badguys.txt"
    spam_url = "https://www.spamhaus.org/drop/drop.txt"
    
		# Output path
    block_output_file = "./mainapp/sites/blocklist.txt"
    cins_output_file = "./mainapp/sites/cins.txt"
    spam_output_file = "./mainapp/sites/spamhaus.txt"
    spam_temp = "./mainapp/sites/spamhaus_temp.txt"

    # Use wget to download the file
    download_block = f"wget -O {block_output_file} {block_url}"
    download_cins_url = f"wget -O {cins_output_file} {cins_url}"
    download_spamhaus = f"wget -O {spam_temp} {spam_url}"

    subprocess.call(download_block, shell=True)
    subprocess.call(download_cins_url, shell=True)
    subprocess.call(download_spamhaus, shell=True)

    # Extract IP addresses from the spam_temp file
    # extract_ip_addresses(spam_temp, spam_output_file)

    return "Done"


# def extract_ip_addresses(input_file, output_file):
#     with open(input_file, 'r') as file:
#         lines = file.readlines()

#     ip_addresses = []
#     for line in lines:
#         line = line.strip()
#         if line and not line.startswith(';'):
#             ip_address = line.split(';')[0].strip()
#             network = ipaddress.IPv4Network(ip_address)
#             # ip_addresses.append(list(network.hosts()))

#             # Convert the iterator to a list of strings (IP addresses)
#             host_ips = [str(ip) for ip in network.hosts()]
#             ip_addresses.extend(host_ips)

            

#     with open(output_file, 'w') as file:
#         file.write('\n'.join(ip_addresses))

def extract_ip_addresses(input_file, output_file):
    def generate_ip_addresses():
        with open(input_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith(';'):
                ip_address = line.split(';')[0].strip()
                network = ipaddress.IPv4Network(ip_address)
                for ip in network.hosts():
                    yield str(ip)

    with open(output_file, 'w') as file:
        for ip_address in generate_ip_addresses():
            file.write(ip_address + '\n')

# extract_ip_addresses("./sites/spamhaus_temp.txt", "./sites/spamhaus.txt")

# ip_addresses.append(ip_address)
            # print(list(network.hosts()))