import subprocess
import argparse

def install_software(package_name):
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', package_name], check=True)
        print(f"Software {package_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing software {package_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Install software package.')
    parser.add_argument('--package-name', required=True, help='Name of the package to install')

    args = parser.parse_args()

    install_software(args.package_name)

if __name__ == "__main__":
    main()

## how to run
## python3 install_software.py --package-name nginx