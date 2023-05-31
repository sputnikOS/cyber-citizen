# defmodule NetworkScanner do
#   def scan_network(network_address) do
#     # Define the options for the nmap command
#     options = ["-sn", "#{network_address}/24"]

#     # Execute the nmap command and capture the output
#     output = System.cmd("nmap", options)

#     # Parse the output to extract the list of hosts that responded to the ping scan
#     hosts = extract_hosts(output)

#     # Print the list of hosts
#     IO.puts("Hosts on the network:")
#     Enum.each(hosts, fn(host) -> IO.puts(host) end)
#   end

#             defp extract_hosts(output) do
#               # Split the output into lines and filter out any that don't contain a host address
#               # lines = output |> String.split("\n") |> Enum.filter(fn(line) -> String.match?(line, /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/) end)

#               # Extract the host addresses from the lines
#               hosts = lines |> Enum.map(fn(line) -> String.split(line, " ")[4] end)

#               # Return the list of hosts
#     hosts
#   end
# end

# # Run the network scan
# NetworkScanner.scan_network("192.168.1.0")
def module NetworkScanner do
  @doc """
  Scans the local network for new devices and sends an email notification.
  """
  def scan_and_notify do
    # Scan the local network for new devices
    nmap_output = :os.cmd("nmap -sn 192.168.1.64/24")
    new_devices = parse_nmap_output(nmap_output)

    # Send an email notification if new devices are found
    if Enum.empty?(new_devices) do
      IO.puts "No new devices found."
    else
      send_notification(new_devices)
    end
  end

  defp parse_nmap_output(nmap_output) do
    # Parse the nmap output to extract the list of new devices
    # You may need to adjust this based on your specific network configuration
    nmap_output
    |> String.split("\n")
    |> Enum.filter(&String.match?(&1, ~r/Nmap scan report for/))
    |> Enum.map(&String.replace(&1, "Nmap scan report for ", ""))
    |> Enum.reject(&String.contains?(&1, "192.168.1."))
  end

  defp send_notification(devices) do
    # Replace these values with your own email address and SMTP server settings
    to = "youremail@example.com"
    from = "networkscanner@example.com"
    smtp_host = "smtp.example.com"
    smtp_port = 587
    smtp_user = "username"
    smtp_password = "password"

    # Compose the email message
    subject = "New device(s) connected to your network"
    body = "The following new device(s) have connected to your network:\n\n#{Enum.join(devices, "\n")}"
    message = Floki.html_to_text("<html><body>#{body}</body></html>")

    # Send the email using the Bamboo library
    email =
      %Bamboo.Email{
        to: to,
        from: from,
        subject: subject,
        text_body: message
      }
    Bamboo.Email.deliver_later(email, adapter: Bamboo.SMTPAdapter, smtp: [host: smtp_host, port: smtp_port, username: smtp_user, password: smtp_password])
  end
end

# Run the scan every 10 minutes
:timer.apply_interval(10 * 60 * 1000, NetworkScanner, :scan_and_notify, [])
