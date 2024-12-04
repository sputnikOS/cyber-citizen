import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class Server {

    public static void main(String[] args) throws IOException {
        // Create an HTTP server that listens on port 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // Create a context for handling requests and set the handler
        server.createContext("/", new MyHandler());

        // Start the server
        server.start();

        System.out.println("Server started on port 8080");
    }

    // Define a custom request handler
    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // Define the response content and status code
            String response = "Hello, World!";
            int statusCode = 200;

            // Send the response headers
            exchange.sendResponseHeaders(statusCode, response.length());

            // Get the response output stream and write the response
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
