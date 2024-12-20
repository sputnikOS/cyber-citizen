import sounddevice as sd

# Function to list audio devices
def list_audio_devices():
    devices = sd.query_devices()  # Get list of all audio devices
    print("Available audio devices:\n")
    
    for idx, device in enumerate(devices):
        print(f"Device #{idx}: {device['name']}")
        print(f"  - Default sample rate: {device['default_samplerate']} Hz")
        print(f"  - Input channels: {device['max_input_channels']}")
        print(f"  - Output channels: {device['max_output_channels']}")
        print(f"  - Host API: {device['hostapi']}\n")

# Call the function to list audio devices
list_audio_devices()
