import subprocess
import argparse

def configure_firewall(ports, port_type):
    try:
        for port in ports:
            subprocess.run(['sudo', 'ufw', 'allow', f'{port}/{port_type}'], check=True)
        subprocess.run(['sudo', 'ufw', 'enable'], check=True)
        print("Firewall configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring firewall: {e}")

def main():
    parser = argparse.ArgumentParser(description='Configure firewall to allow specific ports.')
    parser.add_argument('--ports', required=True, nargs='+', help='List of ports to allow')
    parser.add_argument('--type', choices=['tcp', 'udp'], default='tcp', help='Type of ports (TCP or UDP)')

    args = parser.parse_args()

    configure_firewall(args.ports, args.type)

if __name__ == "__main__":
    main()

## How to run
## TCP rule
## python3 configure_firewall.py --ports 22 80 443 --type tcp

## UDP rule
## python3 configure_firewall.py --ports 53 123 --type udp