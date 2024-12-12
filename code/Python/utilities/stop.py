

import psutil
import time

# Define an array of process IDs you want to disable
process_ids_to_disable = [16284, 2140]  # Add the desired PIDs here

# Function to check if a process is running
def is_process_running(pid):
    return psutil.pid_exists(pid)

# Loop to continuously check and disable the processes
while True:
    for pid_to_disable in process_ids_to_disable:
        if is_process_running(pid_to_disable):
            print(f"Disabling process with PID {pid_to_disable}...")
            try:
                process = psutil.Process(pid_to_disable)
                process.suspend()
            except psutil.NoSuchProcess:
                pass  # Process might have terminated since last check

    # Sleep for a period of time before checking again
    time.sleep(5)
