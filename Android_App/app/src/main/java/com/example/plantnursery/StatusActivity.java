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


/**
 * this class requests the information needed to retrieve
 * the most recent pot data and displays it
 *
 * @author Ruqaya Almalki
 */
public class StatusActivity extends AppCompatActivity {

    private String ipAddress = "192.168.137.101"; //globalServer IP
    private static final int PORT = 8008;
    private int count;

    private Button sendPotID;
    private EditText potID;
    private UDPSender udpSender;
    private String sensors;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_potid); //reference layout

        sendPotID = findViewById(R.id.button4); //button to trigger sending message
        potID = findViewById(R.id.editText4);

        sendPotID.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //notify user button is clicked by a toast
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
                //send data
                udpSender = new UDPSender();
                udpSender.run(ipAddress, sendPot.toString(), PORT);

                //directs to the next view where info will show up
                startActivity(new Intent(StatusActivity.this, ViewStatusActivity.class));
            }
        });
    }
}
