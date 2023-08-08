import ipaddress

# ****************Expand to bits*************************************************************
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

# *********************************************IPv4*****************************************************
    
def check_ipv4_subnet_length(test_ip_address, reference_ip_address):
    try:

        # Split the IPv4 address and prefix length

        _, prefix_length1 = test_ip_address.split('/')
        _, prefix_length2= reference_ip_address.split('/')

        # Convert the prefix length to an integer
        prefix_length1 = int(prefix_length1)
        prefix_length2 = int(prefix_length2)
        
        # Check if the test prefix length  is less than to reference prefix length
        return prefix_length1 < prefix_length2
        
    except ValueError:
        return False
            

def check_ipv4_prefix(test_ip_address, reference_ip_address):
    try:

        # Split the IPv4 address and prefix length
        address1, _ = test_ip_address.split('/')
        address2, prefix_length2 = reference_ip_address.split('/')

        # Convert IPv4 addresses to IPv4 Address objects
        ipv4_addr1 = ipaddress.IPv4Address(address1)
        ipv4_addr2 = ipaddress.IPv4Address(address2)

        # Expands IPv4 addresses into full form
        ipv4_prefix1 = ipv4_addr1.exploded[:]  
        ipv4_prefix2 = ipv4_addr2.exploded[:]

        #Expands ipv4 address into bits

        ipv4_prefix1_in_bits1 = expand_ip_to_bits(ipv4_prefix1)
        ipv4_prefix1_in_bits2 = expand_ip_to_bits(ipv4_prefix2)

        # Check if the first bits equal in quantity to the prefix_length2 of both addresses are similar
        return ipv4_prefix1_in_bits1[:int(prefix_length2)] == ipv4_prefix1_in_bits2[:int(prefix_length2)]

    except (ValueError, ipaddress.AddressValueError):
        return False
    

    
def identify_ipv4_addresses(input_file, reference_ipv4_address):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith(';'):
            ipv4_full_address = line.split(';')[0].strip()
        
            if __name__ == "__main__":
                
                if check_ipv4_subnet_length(ipv4_full_address, reference_ipv4_address):
                    
                    pass
                else:
                    
                    if check_ipv4_prefix(ipv4_full_address, reference_ipv4_address):
                        print(f"The ip address {ipv4_full_address} is a subnet.")
                        
                    else:
                        pass

# **************************************IPv6*****************************************************

def check_ipv6_subnet_length(test_ip_address, reference_ip_address):
    try:
        # Split the IPv6 address and prefix length
        _, prefix_length1 = test_ip_address.split('/')
        _, prefix_length2= reference_ip_address.split('/')

        # Convert the prefix length to an integer
        prefix_length1 = int(prefix_length1)
        prefix_length2 = int(prefix_length2)
        
        # Check if the test prefix length  is less than to reference prefix length
        return prefix_length1 < prefix_length2
        
    except ValueError:
        return False
            

def check_ipv6_prefix(test_ip_address, reference_ip_address):
    try:
        # Split the IPv6 address and prefix length
        address1, _ = test_ip_address.split('/')
        address2, prefix_length2 = reference_ip_address.split('/')

        # Convert IPv6 addresses to IPv6Address objects
        ipv6_addr1 = ipaddress.IPv6Address(address1)
        ipv6_addr2 = ipaddress.IPv6Address(address2)

        # Expands IPv6 addresses into full form
        ipv6_prefix1 = ipv6_addr1.exploded[:]  
        ipv6_prefix2 = ipv6_addr2.exploded[:]

        #Expands ipv6 address into bits
        ipv6_prefix1_in_bits1 = expand_ip_to_bits(ipv6_prefix1)
        ipv6_prefix1_in_bits2 = expand_ip_to_bits(ipv6_prefix2)

        # Check if the first bits equal in quantity to the prefix_length2 of both addresses are similar
        return ipv6_prefix1_in_bits1[:int(prefix_length2)] == ipv6_prefix1_in_bits2[:int(prefix_length2)]

    except (ValueError, ipaddress.AddressValueError):
        return False
# ********************************************************************************************************

# Identify whether ip is IPv4 or IPv6 
def identify_blacklisted_ip_addresses(input_file, reference_ip_address):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith(';'):
            ip_full_address = line.split(';')[0].strip()
            try:
                ip = ipaddress.ip_network(ip_full_address, strict=False)
                if ip.version == 4:
                    
                    if __name__ == "__main__":
                
                        if check_ipv4_subnet_length(ip_full_address, reference_ip_address):
                    
                            pass
                        else:
                    
                            if check_ipv4_prefix(ip_full_address, reference_ip_address):
                                print(f"The ip address {ip_full_address} is a subnet.")
                        
                            else:
                                pass
                                
                elif ip.version == 6:
                    if __name__ == "__main__":
                
                        if check_ipv6_subnet_length(ip_full_address, reference_ip_address):
                    
                            pass
                        else:
                    
                            if check_ipv6_prefix(ip_full_address, reference_ip_address):
                                print(f"The ip address {ip_full_address} is a subnet.")
                        
                            else:
                                pass
                        
                else:
                    return "Invalid IP"
                

            except ValueError:
                return "Invalid IP"
            


Renu_ip_address = ['196.43.128.0/18', '137.63.128.0/17', '102.34.0.0/16', '2.56.192.0/22', '2c0f:f6d0::/32']

for ip in Renu_ip_address:
    identify_blacklisted_ip_addresses('sites/blocklist.txt', ip)

