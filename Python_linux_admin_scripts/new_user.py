import argparse
import subprocess
import getpass

# Run this script as follows:
# python create_user.py --username myuser --groupname mygroup
# Password will be prompted but it won´t show anything while you are typing

def create_group(group_name):
    subprocess.run(['sudo', 'groupadd', group_name])

def create_user(username, password, group_name):
    subprocess.run(['sudo', 'useradd', '-m', username])
    subprocess.run(['sudo', 'usermod', '-a', '-G', group_name, username])
    subprocess.run(['sudo', 'chpasswd'], input=f"{username}:{password}", universal_newlines=True)

if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Create user and group in Linux.')
    parser.add_argument('--username', required=True, help='Username of the new user')
    parser.add_argument('--groupname', required=True, help='Name of the group to add the user to')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Prompt for the password (will be hidden as you type)
    password = getpass.getpass(prompt="Enter password for the new user: ")

    # Call functions to create group and user
    create_group(args.groupname)
    create_user(args.username, password, args.groupname)

    # Confirmation message
    print("User and group created successfully.")
