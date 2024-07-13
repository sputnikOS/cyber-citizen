require 'win32ole'
require 'colorize'
# Method to list all audio devices (both input and output)
def list_audio_devices
  wmi = WIN32OLE.connect("winmgmts://")

  # Query for all audio devices
  query = "SELECT * FROM Win32_SoundDevice"
  audio_devices = wmi.ExecQuery(query)

  puts "All Audio Devices:"
  audio_devices.each do |device|
    puts "Name: #{device.Name}"
    puts "Description: #{device.Description}"
    puts "Manufacturer: #{device.Manufacturer}"
    puts "Device ID: #{device.DeviceID}"
    puts "Status: #{device.Status}"
    puts "Availability: #{device.Availability}"
    puts "------------------------------------"
  end
end

# Call the method to list all audio devices
list_audio_devices
