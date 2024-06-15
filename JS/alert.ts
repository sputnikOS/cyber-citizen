import { spawn } from 'child_process';
import { createTransport } from 'nodemailer';

// Configuration
const network = "192.168.1.64/24";
const knownDevices = ["11:22:33:44:55:66", "aa:bb:cc:dd:ee:ff"];
const emailFrom = "your-email@example.com";
const emailTo = "alert-email@example.com";
const smtpHost = "smtp.gmail.com";
const smtpPort = 465;
const smtpUser = "your-email@example.com";
const smtpPass = "your-email-password";

// Function to scan the network and check for new devices
export function scanNetwork() {
  const command = 'nmap';
  const args = ['-sn', network];
  const nmap = spawn(command, args);

  nmap.stdout.on('data', (data) => {
    const output = data.toString();
    const devices = output.match(/([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}/g);
    
    if (devices) {
      devices.forEach((device) => {
        if (!knownDevices.includes(device)) {
          debugger;
          // sendEmail(`New device detected: ${device}`);
          console.log('device: ', devices);
        }
      });
    }
  });
  
  nmap.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  nmap.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
}

// Function to send an email alert
function sendEmail(message: string) {
  const transporter = createTransport({
    host: smtpHost,
    port: smtpPort,
    secure: true,
    auth: {
      user: smtpUser,
      pass: smtpPass,
    },
  });

  const mailOptions = {
    from: emailFrom,
    to: emailTo,
    subject: 'New device detected on network',
    text: message,
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error(error);
    } else {
      console.log(`Email sent: ${info.response}`);
    }
  });
}

// Scan the network every minute
setInterval(scanNetwork, 60000);
