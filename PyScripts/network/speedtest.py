import subprocess

def test_internet_speed():
    try:
        result = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True)
        output = result.stdout.strip()
        download, upload, ping = output.split("\n")
        print(f"Download Speed: {download}")
        print(f"Upload Speed: {upload}")
        print(f"Ping: {ping}")
    except Exception as e:
        print(f"An error occurred: {e}")

test_internet_speed()
