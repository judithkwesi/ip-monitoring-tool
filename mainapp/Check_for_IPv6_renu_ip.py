import ipaddress

def check_ipv6_prefix(ipv6_address):
    # Convert IPv6 address to an IPv6Address object
    ipv6_addr = ipaddress.IPv6Address(ipv6_address)

    # Convert subnet address to an IPv6Address object
    subnet_address = ipaddress.IPv6Address("2c0f:f6d0::")

    # Get the first 32 bits (first 4 blocks) of the IPv6 address and the subnet address
    ipv6_prefix = ipv6_addr.exploded[:19]  # 19 characters represent the first 32 bits (4 blocks)
    subnet_prefix = subnet_address.exploded[:19]

    # Check if the first 32 bits are similar to "2c0f:f6d0"
    return ipv6_prefix == subnet_prefix

if __name__ == "__main__":
    ipv6_address_to_check = input("Enter the IPv6 address to check (e.g., 2c0f:f6d0::abcd:1234): ")

    if check_ipv6_prefix(ipv6_address_to_check):
        print(f"The first 32 bits of the IPv6 address {ipv6_address_to_check} are similar to 2c0f:f6d0.")
    else:
        print(f"The first 32 bits of the IPv6 address {ipv6_address_to_check} are different from 2c0f:f6d0.")
