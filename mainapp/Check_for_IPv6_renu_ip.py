import ipaddress

# Allow user to input ipv6 address full address
ipv6_full_address = input("Enter the full IPv6 address with prefix length (e.g., 2c0f:f6d0::abcd:1234/32): ")

def check_ipv6_subnet_length(ipv6_address):
    try:
        # Split the IPv6 address and prefix length
        address, prefix_length = ipv6_address.split('/')

        # Convert the IPv6 address to an IPv6Address object
        ipv6_addr = ipaddress.IPv6Address(address)

        # Convert the prefix length to an integer
        prefix_length = int(prefix_length)

        # Check if the prefix length is less than to 32
        return prefix_length < 32
        
    except ValueError:
        return False
    
def check_ipv6_prefix(ipv6_address):
    try:
        # Split the IPv6 address and prefix length
        address, prefix_length = ipv6_address.split('/')

        # Convert IPv6 address to an IPv6Address object
        ipv6_addr = ipaddress.IPv6Address(address)

        # Convert subnet address to an IPv6Address object
        subnet_address = ipaddress.IPv6Address("2c0f:f6d0::")

        # Get the first 32 bits (first 4 blocks) of the IPv6 address and the subnet address
        ipv6_prefix = ipv6_addr.exploded[:19]  # 19 characters represent the first 32 bits (4 blocks)
        subnet_prefix = subnet_address.exploded[:19]

        # Check if the first 32 bits are similar to "2c0f:f6d0"
        return ipv6_prefix == subnet_prefix
    except (ValueError, ipaddress.AddressValueError):
        return False

if __name__ == "__main__":
    
    if check_ipv6_subnet_length(ipv6_full_address):
        exit()

    else:
        if check_ipv6_prefix(ipv6_full_address):
            print(f"The ip address {ipv6_full_address} is a subnet.")
        else:
            print(f"The ip address {ipv6_full_address} is not a subnet.")
            exit()
        
    



    
    


