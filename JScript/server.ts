import * as http from 'http';
import * as scan from './alert'

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end('Hello, World!');
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
    setInterval(scan.scanNetwork, 6000);
    debugger;
});