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
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketException;
import java.net.SocketTimeoutException;

public class StatusActivity extends AppCompatActivity {

    private String ipAddress = "192.168.137.101";
    private static final int PORT = 8008;
    private int count;

    private Button sendPotID;
    private EditText potID;
    private  UDPSender udpSender;
    private UDPReceiver udpReceiver;
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
                udpSender = new UDPSender();

                udpSender.run(ipAddress, sendPot.toString(), PORT);

                startActivity(new Intent(StatusActivity.this, ViewStatusActivity.class));
            }
        });
    }
}
