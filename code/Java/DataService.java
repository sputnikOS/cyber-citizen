// package com.example.myapp.service;

// import org.springframework.stereotype.Service;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

@Service
public class DataService {

    private static final String FILE_PATH = "path/to/your/local/storage/data.json";

    public String getDataFromLocalStorage() {
        try {
            return new String(Files.readAllBytes(Paths.get(FILE_PATH)));
        } catch (IOException e) {
            e.printStackTrace();
            return "{\"error\":\"Unable to read data\"}";
        }
    }
}
