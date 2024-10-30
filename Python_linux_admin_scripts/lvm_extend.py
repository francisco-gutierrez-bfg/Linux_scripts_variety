import argparse
import subprocess

# Run this scripts as follows:
# python extend_lvm.py --lvm_name <mylvm> --size <size in MB (M), GB (G), TB (T)>
# Ex: python extend_lvm.py --lvm_name mylvm --size 1000M
# Ex: python extend_lvm.py --lvm_name mylvm --size 1G
# Ex: python extend_lvm.py --lvm_name mylvm --size 1T


import argparse
import subprocess

def extend_lvm(lvm_name, size):
    # Convert size to megabytes
    if size.endswith('G'):
        size_in_mb = int(size[:-1]) * 1024
    elif size.endswith('T'):
        size_in_mb = int(size[:-1]) * 1024 * 1024
    else:
        size_in_mb = int(size)
    
    # Check existing size of the LVM
    lvdisplay_output = subprocess.check_output(['sudo', 'lvdisplay', '--units', 'm', '--noheading', '-c', f'/dev/mapper/{lvm_name}']).decode().strip()
    current_size = int(lvdisplay_output.split(':')[6].split('M')[0])
    
    # Extend the LVM
    subprocess.run(['sudo', 'lvextend', '--size', f'+{size_in_mb}M', f'/dev/mapper/{lvm_name}'])
    
    # Resize the file system
    subprocess.run(['sudo', 'resize2fs', f'/dev/mapper/{lvm_name}'])

if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Extend LVM in Linux.')
    parser.add_argument('--lvm_name', required=True, help='Name of the LVM to extend')
    parser.add_argument('--size', required=True, help='Size to extend the LVM (e.g., 1000M, 10G, 1T)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call function to extend LVM
    extend_lvm(args.lvm_name, args.size)

    print("LVM extended successfully.")