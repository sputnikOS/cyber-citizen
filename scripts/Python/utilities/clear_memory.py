import subprocess

def clear_memory():
    try:
        # PowerShell command to clear standby memory
        command = r'powershell.exe -Command "& {Clear-Host; $mem = Get-WmiObject Win32_OperatingSystem; $mem.FreePhysicalMemory}"'
        
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Display the result
        print(result.stdout)
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Clearing standby memory...")
    clear_memory()

if __name__ == "__main__":
    main()
