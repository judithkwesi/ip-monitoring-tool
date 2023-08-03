import ipaddress


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
            

def check_ipv4_prefix(test_ip_address, reference_ip_address):
    try:
        # Split the IPv6 address and prefix length
        address1, _ = test_ip_address.split('/')
        address2, prefix_length2 = reference_ip_address.split('/')

        # Convert IPv6 addresses to IPv6Address objects
        ipv6_addr1 = ipaddress.IPv4Address(address1)
        ipv6_addr2 = ipaddress.IPv4Address(address2)

        # Expands IPv6 addresses into full form
        ipv6_prefix1 = ipv6_addr1.exploded[:]  
        ipv6_prefix2 = ipv6_addr2.exploded[:]

        #Expands ipv6 address into bits
        ipv6_prefix1_in_bits1 = expand_ipv4_to_bits(ipv6_prefix1)
        ipv6_prefix1_in_bits2 = expand_ipv4_to_bits(ipv6_prefix2)

        # Check if the first bits equal in quantity to the prefix_length2 of both addresses are similar
        return ipv6_prefix1_in_bits1[:int(prefix_length2)] == ipv6_prefix1_in_bits2[:int(prefix_length2)]

    except (ValueError, ipaddress.AddressValueError):
        return False
    

    
def identify_ipv4_addresses(input_file, reference_ipv6_address):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith(';'):
            ipv6_full_address = line.split(';')[0].strip()
        
            if __name__ == "__main__":
                
                if check_ipv4_subnet_length(ipv6_full_address, reference_ipv6_address):
                    
                    pass
                else:
                    
                    if check_ipv4_prefix(ipv6_full_address, reference_ipv6_address):
                        print(f"The ip address {ipv6_full_address} is a subnet.")
                        
                    else:
                        pass
                   

# Calling the identify_ipv4_addresses
Renu_ip_address = ['196.43.128.0/18', '137.63.128.0/17', '102.34.0.0/16', '2.56.192.0/22']

for ip in Renu_ip_address:
    identify_ipv4_addresses("./sites/spamhaus.txt", ip)

