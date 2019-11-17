package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

public class AddThresholdsActivity extends AppCompatActivity {

    private static final int PORT = 1000;
    private static final String ipAddress = "192.168.1.94";
    private UDPSender udpSender;
    private Button setLightThreshold, setTempThreshold, setHumidityThreshold, setSoilThreshold;
    private EditText tempThreshold, lightThreshold, humidityThreshold, soilThreshold, potID, roomID;
    private CheckBox tLess, tGreater, lLess, lGreater, hLess, hGreater, sLess, sGreater;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addthreshold);

        //needs to be here
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //findViewById
        //pot and room id

        potID = findViewById(R.id.editText11);
        roomID = findViewById(R.id.editText12);

        //buttons
        setLightThreshold = findViewById(R.id.button13);
        setTempThreshold =  findViewById(R.id.button17);
        setHumidityThreshold =  findViewById(R.id.button18);
        setSoilThreshold =  findViewById(R.id.button16);

        //inputted number
        tempThreshold = findViewById(R.id.editText6);
        lightThreshold = findViewById(R.id.editText13);
        humidityThreshold = findViewById(R.id.editText14);
        soilThreshold = findViewById(R.id.editText10);

        //less/greater than
        tLess = findViewById(R.id.checkBox);
        tGreater = findViewById(R.id.checkBox2);
        hLess = findViewById(R.id.checkBox6);
        hGreater = findViewById(R.id.checkBox7);
        lLess = findViewById(R.id.checkBox3);
        lGreater = findViewById(R.id.checkBox4);
        sLess = findViewById(R.id.checkBox5);
        sGreater = findViewById(R.id.checkBox8);

        //if both checkboxes checked, nothing is set
        // press a button to set every one of them

        setTempThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {

                //put it in JSON format
                //JSON[‘opcode’:’3’, ‘lessGreaterThan’:String, ‘thresholdValue’: integer, ‘sensorType’: String, ‘potID’:Integer, ‘roomID’ :Integer]
                JSONObject threshold = new JSONObject();
                try {
                    threshold.put("opcode", "3" );
                    threshold.put("sensorType", "roomTemperature");
                    threshold.put("thresholdValue", tempThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());
                    threshold.put("roomID", roomID.getText().toString());

                    if((tLess.isChecked() && tGreater.isChecked()) | (!tLess.isChecked() && !tGreater.isChecked())){
                        Toast.makeText(AddThresholdsActivity.this, "please only check one box", Toast.LENGTH_SHORT).show();
                    }
                    else if(tLess.isChecked()){
                        threshold.put("lessGreaterThan", "less");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    } else {
                        threshold.put("lessGreaterThan", "greater");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //after receives ACK:
               // Toast.makeText(AddThresholdsActivity.this, " temperature threshold is set", Toast.LENGTH_SHORT).show();
            }
        });

        setLightThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //put it in JSON format
                //JSON[‘opcode’:’3’, ‘lessGreaterThan’:String, ‘thresholdValue’: integer, ‘sensorType’: String, ‘potID’:Integer, ‘roomID’ :Integer]
                JSONObject threshold = new JSONObject();
                try {
                    threshold.put("opcode", "3" );
                    threshold.put("sensorType", "light");
                    threshold.put("thresholdValue", lightThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());
                    threshold.put("roomID", roomID.getText().toString());

                    if(lLess.isChecked() && lGreater.isChecked()){
                        Toast.makeText(AddThresholdsActivity.this, "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    else if(lLess.isChecked()){
                        threshold.put("lessGreaterThan", "less");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    } else {
                        threshold.put("lessGreaterThan", "greater");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //after receives ACK:
                Toast.makeText(AddThresholdsActivity.this, " light threshold is set", Toast.LENGTH_SHORT).show();
            }
        });

        setHumidityThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                JSONObject threshold = new JSONObject();
                try {
                    threshold.put("opcode", "3" );
                    threshold.put("sensorType", "roomHumidity");
                    threshold.put("thresholdValue", humidityThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());
                    threshold.put("roomID", roomID.getText().toString());

                    if(hLess.isChecked() && hGreater.isChecked()){
                        Toast.makeText(AddThresholdsActivity.this, "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    else if(hLess.isChecked()){
                        threshold.put("lessGreaterThan", "less");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    } else {
                        threshold.put("lessGreaterThan", "greater");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //after receives ACK:
                Toast.makeText(AddThresholdsActivity.this, " humidity threshold is set", Toast.LENGTH_SHORT).show();
            }
        });

        setSoilThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                JSONObject threshold = new JSONObject();
                try {
                    threshold.put("opcode", "3" );
                    threshold.put("sensorType", "soilMoisture");
                    threshold.put("thresholdValue", soilThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());
                    threshold.put("roomID", roomID.getText().toString());

                    if(sLess.isChecked() && sGreater.isChecked()){
                        Toast.makeText(AddThresholdsActivity.this, "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    else if(sLess.isChecked()){
                        threshold.put("lessGreaterThan", "less");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    } else {
                        threshold.put("lessGreaterThan", "greater");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }
                //after receives ACK:
                Toast.makeText(AddThresholdsActivity.this, " soil threshold is set", Toast.LENGTH_SHORT).show();
            }
        });

        try {
            udpSender = new UDPSender();
            Log.d("User", "Thread start...");
        } catch (Exception e) {
            String str = e.toString();
            Log.e("Error by User", str);
        }

    }
}
