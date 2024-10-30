import subprocess
import os
import argparse

def install_mysql():
    try:
        print("Updating package index...")
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        
        print("Installing MySQL server...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mysql-server'], check=True)
        print("MySQL server installed successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during MySQL installation: {e}")
        exit(1)

def configure_mysql(root_password, db_name, db_user, db_password):
    try:
        print("Securing MySQL installation...")
        subprocess.run(['sudo', 'mysql_secure_installation'], input=f'y\n{root_password}\n{root_password}\nY\nY\nY\nY\n', text=True, check=True)
        
        print("Configuring MySQL with initial settings...")
        mysql_commands = f"""
        ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '{root_password}';
        CREATE DATABASE {db_name};
        CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';
        GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost';
        FLUSH PRIVILEGES;
        EXIT;
        """
        with open('/tmp/mysql_setup.sql', 'w') as f:
            f.write(mysql_commands)
        
        subprocess.run(['sudo', 'mysql', '-u', 'root', '-p' + root_password, '-e', f"source /tmp/mysql_setup.sql"], check=True)
        os.remove('/tmp/mysql_setup.sql')
        
        print("MySQL configuration completed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during MySQL configuration: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description='Install and configure MySQL server.')
    parser.add_argument('--root-password', required=True, help='Root password for MySQL')
    parser.add_argument('--db-name', required=True, help='Name of the database to create')
    parser.add_argument('--db-user', required=True, help='Name of the user to create')
    parser.add_argument('--db-password', required=True, help='Password for the new user')
    
    args = parser.parse_args()
    
    install_mysql()
    configure_mysql(args.root_password, args.db_name, args.db_user, args.db_password)

if __name__ == "__main__":
    main()

## Usage:
## python3 install_configure_mysql.py --root-password your_root_password --db-name your_database --db-user your_user --db-password your_password