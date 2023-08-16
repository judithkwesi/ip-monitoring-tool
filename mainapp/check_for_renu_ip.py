import ipaddress
from multiprocessing import Pool
from functools import partial

# function that expands ip address to bits
def expand_ip_to_bits(ip_address):
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            ip_bits = bin(int(ip_obj))[2:].zfill(32)  # IPv4 has 32 bits
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            ip_bits = bin(int(ip_obj))[2:].zfill(128)  # IPv6 has 128 bits
        else:
            return None

        return ip_bits
    except ipaddress.AddressValueError:
        return None

#Function that checks whether an ip has a subnet '/' or not
def has_subnet(ip_address):
    try:
        ip_obj = ipaddress.ip_interface(ip_address)
        return ip_obj.network.prefixlen < ip_obj.network.max_prefixlen
    except ValueError:
        return False
        
#Split function for subnet_length function        
def split_for_subnet_length(test_ip_address, reference_ip_address):
    if has_subnet(test_ip_address) and has_subnet(reference_ip_address):
        _, prefix_length1 = test_ip_address.split('/')
        _, prefix_length2 = reference_ip_address.split('/')
        return prefix_length1, prefix_length2
    elif not has_subnet(test_ip_address) and has_subnet(reference_ip_address):
        _, prefix_length2 = reference_ip_address.split('/')
        return None, prefix_length2
    else:
        return None, None
    

#Split function for check_prefix function
def split_for_check_prefix(test_ip_address, reference_ip_address):
    if has_subnet(test_ip_address) and has_subnet(reference_ip_address):
        address1, _ = test_ip_address.split('/')
        address2, prefix_length2 = reference_ip_address.split('/')
        return address1, address2, prefix_length2
    elif not has_subnet(test_ip_address) and has_subnet(reference_ip_address):
        address1 = test_ip_address
        address2, prefix_length2 = reference_ip_address.split('/')
        return address1, address2, prefix_length2
    else:
        return None, None, None


#function to check subnet length and comapre them
def check_subnet_length(test_ip_address, reference_ip_address):
    try:
        # Split the IP address and prefix length
        prefix_length1, prefix_length2 = split_for_subnet_length(test_ip_address, reference_ip_address)

        if prefix_length1 == None or prefix_length2 == None:
            return False
           
        # Convert the prefix length to an integer
        prefix_length1 = int(prefix_length1)
        prefix_length2 = int(prefix_length2)

        # Check if the test prefix length is less than the reference prefix length
        return prefix_length1 < prefix_length2

    except ValueError:
        return False

#Function to check the prefix length
def check_prefix(test_ip_address, reference_ip_address, ip_type):
    try:
        address1, address2, prefix_length2 = split_for_check_prefix(test_ip_address, reference_ip_address)

        if ip_type == "IPv4":
            # Convert IPv4 addresses to IPv4Address objects
            ipv_addr1 = ipaddress.IPv4Address(address1)
            ipv_addr2 = ipaddress.IPv4Address(address2)
        elif ip_type == "IPv6":
            # Convert IPv6 addresses to IPv6Address objects
            ipv_addr1 = ipaddress.IPv6Address(address1)
            ipv_addr2 = ipaddress.IPv6Address(address2)
        else:
            return False

        # Expands IP addresses into full form
        prefix1 = ipv_addr1.exploded[:]
        prefix2 = ipv_addr2.exploded[:]

        # Expands IP address into bits
        prefix1_in_bits1 = expand_ip_to_bits(prefix1)
        prefix1_in_bits2 = expand_ip_to_bits(prefix2)

        # Check if the first bits equal in quantity to the prefix_length2 of both addresses are similar
        return prefix1_in_bits1[:int(prefix_length2)] == prefix1_in_bits2[:int(prefix_length2)]

    except (ValueError, ipaddress.AddressValueError):
        return False

#Main functon of identify_blacklisted_ip_addresses
def main(ip_full_address, reference_ip_address, blocklist, site):
    ip = ipaddress.ip_network(ip_full_address, strict=False)
    
    if ip.version == 4:
        if check_subnet_length(ip_full_address, reference_ip_address):
            pass
        else:
            if check_prefix(ip_full_address, reference_ip_address, "IPv4"):
                blocklist.append({"ip": str(ip_full_address), "source": site})
            else:
                pass
    elif ip.version == 6:
        if check_subnet_length(ip_full_address, reference_ip_address):
            pass
        else:
            if check_prefix(ip_full_address, reference_ip_address, "IPv6"):
                blocklist.append({"ip": str(ip_full_address), "source": site})
            else:
                pass
    
    else:
        return "Invalid IP"


def process_chunk(chunk, reference_ip_address, site):
    result = []
    for line in chunk:
        line = line.strip()
        if line and not line.startswith(';'):
            # ip_full_address = line.strip().split(';', 1)[0]
            ip_full_address = line.split(';')[0].strip()
            try:
                main(ip_full_address, reference_ip_address, result, site)
            except ValueError:
                pass
    return result

def identify_blacklisted_ip_addresses(input_file, reference_ip_address, blocklist, site):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    num_processes = 4  # Number of processes (cores) to use
    chunk_size = len(lines) // num_processes
    remaining_lines = len(lines) % num_processes

    chunks = [lines[i:i+chunk_size] for i in range(0, len(lines) - remaining_lines, chunk_size)]

    # Add a separate chunk for the remaining lines
    if remaining_lines > 0:
        chunks.append(lines[-remaining_lines:])

    process_chunk_partial = partial(process_chunk, reference_ip_address=reference_ip_address, site=site)

    with Pool(num_processes) as pool:
        results = pool.map(process_chunk_partial, chunks)

    for result in results:
        blocklist.extend(result)
