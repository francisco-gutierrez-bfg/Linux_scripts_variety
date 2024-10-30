import subprocess

# This script will sacn for new LUN's/Disks and show them.
# Run this script as follows:
# python scan_and_show_luns.py

def scan_for_new_luns():
    subprocess.run(['sudo', 'echo', '1', '>', '/sys/class/scsi_host/host*/scan'], shell=True)

def get_detected_luns():
    luns = []
    with open('/proc/partitions', 'r') as f:
        for line in f:
            if 'sd' in line:
                parts = line.split()
                if len(parts) > 3:
                    luns.append(parts[3])
    return luns

if __name__ == "__main__":
    scan_for_new_luns()
    detected_luns = get_detected_luns()
    print("Detected LUNs:")
    for lun in detected_luns:
        print(lun)
