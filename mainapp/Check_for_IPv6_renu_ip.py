import ipaddress

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

if __name__ == "__main__":
    ipv6_full_address = input("Enter the full IPv6 address with prefix length (e.g., 2c0f:f6d0::abcd:1234/32): ")

    if check_ipv6_subnet_length(ipv6_full_address):
        print(f"The subnet prefix length in {ipv6_full_address} is less than 32.")
        exit()
    else:
        print(f"The subnet prefix length in {ipv6_full_address} is greater than or equal to 32")


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
    ipv6_address_to_check = input("Enter the IPv6 address to check for similarity (e.g., 2c0f:f6d0::abcd:1234): ")

    if check_ipv6_prefix(ipv6_address_to_check):
        print(f"The first 32 bits of the IPv6 address {ipv6_address_to_check} are similar to 2c0f:f6d0.")
    else:
        print(f"The first 32 bits of the IPv6 address {ipv6_address_to_check} are different from 2c0f:f6d0.")

