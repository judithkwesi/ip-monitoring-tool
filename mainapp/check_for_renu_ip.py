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
          
# **************************************IPv6*****************************************************

def check_subnet_length(test_ip_address, reference_ip_address):
    try:
        # Split the IP address and prefix length
        _, prefix_length1 = test_ip_address.split('/')
        _, prefix_length2 = reference_ip_address.split('/')

        # Convert the prefix length to an integer
        prefix_length1 = int(prefix_length1)
        prefix_length2 = int(prefix_length2)

        # Check if the test prefix length is less than the reference prefix length
        return prefix_length1 < prefix_length2

    except ValueError:
        return False


def check_prefix(test_ip_address, reference_ip_address, ip_type):
    try:
        # Split the IP address and prefix length
        address1, _ = test_ip_address.split('/')
        address2, prefix_length2 = reference_ip_address.split('/')

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
                
                        if check_subnet_length(ip_full_address, reference_ip_address):
                    
                            pass
                        else:
                    
                            if check_prefix(ip_full_address, reference_ip_address, "IPv4"):
                                print(f"The ip address {ip_full_address} is a subnet.")
                        
                            else:
                                pass
                                
                elif ip.version == 6:
                    if __name__ == "__main__":
                
                        if check_subnet_length(ip_full_address, reference_ip_address):
                    
                            pass
                        else:
                    
                            if check_prefix(ip_full_address, reference_ip_address, "IPv6"):
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

