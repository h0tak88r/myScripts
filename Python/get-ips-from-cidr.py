import ipaddress

# Input file with CIDR ranges
input_file = 'cidr.txt'

# Output file for expanded IP ranges
output_file = 'ip-ranges.txt'

# Function to expand CIDR ranges and save to a file
def expand_cidr_ranges(input_file, output_file):
    with open(input_file, 'r') as cidr_file, open(output_file, 'w') as ip_file:
        for line in cidr_file:
            cidr = line.strip()
            try:
                network = ipaddress.IPv4Network(cidr, strict=False)
                for ip in network.hosts():
                    ip_file.write(str(ip) + '\n')
            except ipaddress.AddressValueError as e:
                print(f"Error parsing CIDR {cidr}: {e}")

if __name__ == '__main__':
    expand_cidr_ranges(input_file, output_file)
