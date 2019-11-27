package com.example.plantnursery;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

public class StatusActivity extends AppCompatActivity {

    private String ipAddress = "192.168.137.101";
    private static final int PORT = 1003;

    private Button sendPotID;
    private EditText potID;
    private  UDPSender udpSender;
    private String sensors;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_potid);

        sendPotID = findViewById(R.id.button4);
        potID = findViewById(R.id.editText4);

        sendPotID.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(StatusActivity.this, "send potID", Toast.LENGTH_SHORT).show();
                JSONObject sendPot = new JSONObject();
                try {
                    sendPot.put("opcode", "5");
                    //opcode for this view is row == 0 when in fact its the last row entered
                    sendPot.put("rowNumbers", 0);
                    sendPot.put("potID", potID.getText().toString());
                    sensors = "light, temperature, humidity, waterDistance, soilMoisture";
                    sendPot.put("sensorType", sensors);

                } catch (JSONException e) {
                    e.printStackTrace();
                }
                try {
                    udpSender = new UDPSender();
                    udpSender.run(ipAddress, sendPot.toString() , PORT);
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //goes to viewStatusActivity nect
                startActivity(new Intent(StatusActivity.this, ViewStatusActivity.class));


            }

        });
    }
}
