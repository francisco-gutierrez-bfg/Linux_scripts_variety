import subprocess
import argparse

def configure_network(interface, ip_address, netmask, gateway, dns_servers):
    try:
        # Configure network interface
        subprocess.run(['sudo', 'ifconfig', interface, ip_address, 'netmask', netmask], check=True)
        subprocess.run(['sudo', 'route', 'add', 'default', 'gw', gateway, interface], check=True)
        print(f"Network interface {interface} configured successfully.")

        # Configure DNS servers
        for dns_server in dns_servers:
            subprocess.run(['sudo', 'bash', '-c', f'echo "nameserver {dns_server}" >> /etc/resolv.conf'], check=True)
        print(f"DNS servers configured: {dns_servers}")

    except subprocess.CalledProcessError as e:
        print(f"Error configuring network: {e}")

def main():
    parser = argparse.ArgumentParser(description='Configure network settings.')
    parser.add_argument('--interface', required=True, help='Network interface to configure')
    parser.add_argument('--ip-address', required=True, help='IP address to assign')
    parser.add_argument('--netmask', required=True, help='Netmask to assign')
    parser.add_argument('--gateway', required=True, help='Default gateway to assign')
    parser.add_argument('--dns-servers', nargs='+', required=True, help='DNS servers to configure')

    args = parser.parse_args()

    configure_network(args.interface, args.ip_address, args.netmask, args.gateway, args.dns_servers)

if __name__ == "__main__":
    main()


## How to run
## python3 configure_network.py --interface eth0 --ip-address 192.168.1.100 --netmask 255.255.255.0 --gateway 192.168.1.1 --dns-servers 8.8.8.8 8.8.4.4