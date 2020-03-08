import com.fasterxml.jackson.databind.ObjectMapper;
import entities.GameData;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Main {
    public static void main(final String[] args) {

        try {
            URL url = new URL("http://localhost:8082");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            GameData gameData = new ObjectMapper()
                    .readerFor(GameData.class)
                    .readValue(new InputStreamReader(connection.getInputStream()));

            System.out.println(gameData.getGameOn());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
