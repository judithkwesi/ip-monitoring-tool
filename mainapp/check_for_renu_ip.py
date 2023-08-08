import ipaddress

# *********************************************IPv4*****************************************************
def expand_ipv4_to_bits(ipv4_address):
    try:
        # Convert IPv4 address to an IPv4Address object
        ipv4_addr = ipaddress.IPv4Address(ipv4_address)

        # Get the full binary representation of the IPv4 address
        ipv4_binary = bin(int(ipv4_addr))[2:].zfill(32)

        return ipv4_binary
    except ipaddress.AddressValueError:
        return None
    
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

        ipv4_prefix1_in_bits1 = expand_ipv4_to_bits(ipv4_prefix1)
        ipv4_prefix1_in_bits2 = expand_ipv4_to_bits(ipv4_prefix2)

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
# function to expand IPv6 address into binary(bits)
def expand_ipv6_to_bits(ipv6_address):
    try:
        # Convert IPv6 address to an IPv6Address object
        ipv6_addr = ipaddress.IPv6Address(ipv6_address)

        # Get the full binary representation of the IPv6 address
        ipv6_binary = "".join(format(int(x, 16), '04b') for x in ipv6_addr.exploded.replace(':', ''))

        return ipv6_binary
    except ipaddress.AddressValueError:
        return None
    

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
        ipv6_prefix1_in_bits1 = expand_ipv6_to_bits(ipv6_prefix1)
        ipv6_prefix1_in_bits2 = expand_ipv6_to_bits(ipv6_prefix2)

        # Check if the first bits equal in quantity to the prefix_length2 of both addresses are similar
        return ipv6_prefix1_in_bits1[:int(prefix_length2)] == ipv6_prefix1_in_bits2[:int(prefix_length2)]

    except (ValueError, ipaddress.AddressValueError):
        return False
# ********************************************************************************************************

# Identify whether ip is IPv4 or IPv6 
def identify_ip_addresses_type(input_file, reference_ip_address):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith(';'):
            ip_full_address = line.split(';')[0].strip()
            try:
                ip = ipaddress.ip_network(ip_str, strict=False)
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
            