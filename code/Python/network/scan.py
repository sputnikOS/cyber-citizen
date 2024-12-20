import argparse
import shodan
import sys
import json

# Replace with your actual Shodan API key
API_KEY = '5DjnnKaMwglBCIYf0MgXrM1NoLhYpPc5'

def get_ip_details(ip_address):
    """Retrieve detailed information for the given IP address using Shodan."""
    try:
        # Initialize Shodan API
        api = shodan.Shodan(API_KEY)
        
        # Perform the search query for the given IP
        result = api.host(ip_address)
        
        # Display basic information
        print(f"IP Information for {ip_address}:")
        print(f"Organization: {result.get('org', 'n/a')}")
        print(f"Location: {result.get('city', 'n/a')}, {result.get('country_name', 'n/a')}")
        print(f"ASN: {result.get('asn', 'n/a')}")
        print(f"OS: {result.get('os', 'n/a')}")
        print(f"Last Update: {result.get('last_update', 'n/a')}")
        
        # Detailed services info
        print("\nServices:")
        for service in result.get('data', []):
            print(f"Port: {service['port']} - {service.get('product', 'n/a')} "
                  f"({service.get('info', 'n/a')})")
            print(f"Banner: {service.get('data', 'n/a')}")
            print("=============================================")
        
        # Get the vulnerabilities if available
        if result.get('vulns'):
            print("\nVulnerabilities:")
            for vuln, details in result['vulns'].items():
                print(f"{vuln}: {details['description']}")
                print("=============================================")
        else:
            print("\nNo vulnerabilities found.")

        # Display Shodan raw data (optional for in-depth analysis)
        print("\nRaw Data:")
        print(json.dumps(result, indent=4))
        
    except shodan.APIError as e:
        print(f"Error: {e}")

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Shodan IP In-Depth Scan")
    parser.add_argument("ip", help="IP address to scan")
    args = parser.parse_args()

    # Validate the IP address argument
    ip_address = args.ip
    if not ip_address:
        print("Please provide a valid IP address to scan.")
        sys.exit(1)

    # Perform the scan
    get_ip_details(ip_address)

if __name__ == "__main__":
    main()
