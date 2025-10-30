use std::process::Command;
use std::time::Duration;
use std::thread;

// Function to disable a network interface
fn disable_network_interface(interface: &str) {
    println!("Disabling network interface: {}", interface);
    let output = Command::new("sudo")
        .arg("ifconfig")
        .arg(interface)
        .arg("down")
        .output();

    match output {
        Ok(result) if result.status.success() => {
            println!("Network interface {} disabled successfully.", interface);
        }
        Ok(result) => {
            eprintln!(
                "Failed to disable network interface: {}",
                String::from_utf8_lossy(&result.stderr)
            );
        }
        Err(e) => {
            eprintln!("Error executing command: {}", e);
        }
    }
}

// Function to monitor connected USB devices
fn monitor_usb_devices() {
    println!("Monitoring USB devices...");
    loop {
        let output = Command::new("lsusb").output();

        match output {
            Ok(result) if result.status.success() => {
                println!("Connected USB devices:\n{}", String::from_utf8_lossy(&result.stdout));
            }
            Ok(result) => {
                eprintln!(
                    "Error listing USB devices: {}",
                    String::from_utf8_lossy(&result.stderr)
                );
            }
            Err(e) => {
                eprintln!("Error executing lsusb: {}", e);
            }
        }

        // Pause before checking again
        thread::sleep(Duration::from_secs(10));
    }
}

fn main() {
    // Disable a specific network interface (e.g., "eth0" or "wlan0")
    disable_network_interface("eth0");

    // Monitor USB devices in a separate thread
    thread::spawn(|| {
        monitor_usb_devices();
    });

    println!("Air-gapped environment enforcement active.");
    loop {
        // Keep the main thread running
        thread::sleep(Duration::from_secs(60));
    }
}
