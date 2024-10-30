import subprocess
import argparse

def create_user(username, password):
    try:
        subprocess.run(['sudo', 'useradd', username], check=True)
        subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}', text=True, check=True)
        print(f"User {username} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}: {e}")

def delete_user(username):
    try:
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"User {username} deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user {username}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create or delete a user.')
    parser.add_argument('action', choices=['create', 'delete'], help='Action to perform (create or delete a user)')
    parser.add_argument('--username', required=True, help='Username of the user')
    parser.add_argument('--password', required=False, help='Password for the user (required for create action)')

    args = parser.parse_args()

    if args.action == 'create' and not args.password:
        parser.error('The --password argument is required for creating a user.')

    if args.action == 'create':
        create_user(args.username, args.password)
    elif args.action == 'delete':
        delete_user(args.username)

if __name__ == "__main__":
    main()

## How to run
## To create users:
## python3 user_management.py create --username testuser --password password123

## To delete users:
## python3 user_management.py delete --username testuser
