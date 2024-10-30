import subprocess

def update_system():
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'upgrade', '-y'], check=True)
        subprocess.run(['sudo', 'apt-get', 'dist-upgrade', '-y'], check=True)
        subprocess.run(['sudo', 'apt-get', 'autoremove', '-y'], check=True)
        subprocess.run(['sudo', 'apt-get', 'clean'], check=True)
        print("System updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating system: {e}")

def main():
    update_system()

if __name__ == "__main__":
    main()

## How to run
## python3 update_system.py