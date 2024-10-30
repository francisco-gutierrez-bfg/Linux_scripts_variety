import subprocess
import argparse
import humanfriendly
from cron_descriptor import get_description  # pip install cron-descriptor

def convert_to_cron(schedule):
    try:
        cron_expression = humanfriendly.cron.convert(schedule)
        description = get_description(cron_expression)
        return cron_expression, description
    except ValueError as e:
        print(f"Error converting schedule to cron expression: {e}")
        exit(1)

def setup_cron_job(cron_expression, command):
    try:
        cron_job = f'{cron_expression} {command}'
        subprocess.run(['sudo', 'bash', '-c', f'(crontab -l; echo "{cron_job}") | crontab -'], check=True)
        print("Cron job added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up cron job: {e}")

def main():
    parser = argparse.ArgumentParser(description='Setup a cron job.')
    parser.add_argument('--schedule', required=True, help='Human-friendly schedule (e.g., "every day at 2am")')
    parser.add_argument('--command', required=True, help='Command to execute')

    args = parser.parse_args()
    
    cron_expression, description = convert_to_cron(args.schedule)
    print(f"Schedule interpreted as: {description}")
    
    setup_cron_job(cron_expression, args.command)

if __name__ == "__main__":
    main()


## How to run
## python3 setup_cron_job.py --schedule "every day at 2am" --command "/usr/bin/python3 /path/to/your/script.py"