#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <linux/if.h>

// Function to disable a network interface
void disable_network_interface(const char* interface) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        return;
    }

    struct ifreq ifr;
    strncpy(ifr.ifr_name, interface, IFNAMSIZ - 1);

    // Bring the interface down
    ifr.ifr_flags = 0;
    if (ioctl(sock, SIOCSIFFLAGS, &ifr) < 0) {
        perror("Failed to disable network interface");
    } else {
        printf("Network interface %s disabled successfully.\n", interface);
    }

    close(sock);
}

// Function to monitor for external device connections (example: USB)
void monitor_usb_connections() {
    printf("Monitoring USB connections...\n");
    system("lsusb"); // Example to list USB devices (requires lsusb installed)
    printf("Consider implementing stricter USB management policies.\n");
}

int main() {
    // Example: Disable a network interface (e.g., "eth0")
    const char* network_interface = "eth0";
    disable_network_interface(network_interface);

    // Monitor USB devices
    monitor_usb_connections();

    printf("System is now enforcing an air-gapped environment.\n");

    // Infinite loop to maintain air gap; replace with appropriate logic for your use case
    while (1) {
        sleep(10);
    }

    return 0;
}
