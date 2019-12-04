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

import java.io.IOException;

/**
 * This class is used to collect threshold values the app user will like to set
 * and send the threshold values to the globalServer which will store it in the
 * database
 */
public class AddThresholdsActivity extends AppCompatActivity {

    private static final String ipAddress = "192.168.137.101";
    private static final int PORT = 8008;

    private UDPSender udpSender;
    private Button setLightThreshold, setTempThreshold, setHumidityThreshold, setSoilThreshold;
    private EditText tempThreshold, lightThreshold, humidityThreshold, soilThreshold, potID;
    private CheckBox tempLess, tempGreater, lightLess, lightGreater, humidityLess,
            humidityGreater, soilLess, soilGreater;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addthreshold);

        //test for compatibility and sets policy
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //allow all widgets in view to be found
        potID = findViewById(R.id.editText11);

        //buttons, send info to globalServer
        setLightThreshold = findViewById(R.id.button13);
        setTempThreshold = findViewById(R.id.button17);
        setHumidityThreshold = findViewById(R.id.button18);
        setSoilThreshold = findViewById(R.id.button16);

        //editText, inputted value for thresholds
        tempThreshold = findViewById(R.id.editText6);
        lightThreshold = findViewById(R.id.editText10);
        humidityThreshold = findViewById(R.id.editText13);
        soilThreshold = findViewById(R.id.editText14);

        //checkboxes, less than /greater than
        tempLess = findViewById(R.id.checkBox);
        tempGreater = findViewById(R.id.checkBox2);
        humidityLess = findViewById(R.id.checkBox6);
        humidityGreater = findViewById(R.id.checkBox7);
        lightLess = findViewById(R.id.checkBox3);
        lightGreater = findViewById(R.id.checkBox4);
        soilLess = findViewById(R.id.checkBox5);
        soilGreater = findViewById(R.id.checkBox8);


        //setTempThreshold button listener
        setTempThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            //when button is pressed
            public void onClick(View v) {
                try {
                    //put it in JSON format
                    JSONObject threshold = new JSONObject();
                    //extract info from layout view and add to JSON object
                    threshold.put("opcode", "3");
                    threshold.put("sensorType", "roomTemperature");
                    threshold.put("thresholdValue", tempThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());


                    //if both checkboxes are pressed, the message is not sent
                    if ((tempLess.isChecked() && tempGreater.isChecked()) |
                            (!tempLess.isChecked() && !tempGreater.isChecked())) {
                        //notify user for invalid input
                        Toast.makeText(AddThresholdsActivity.this,
                                "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    //logic for checkboxes, default is greater
                    else if (tempLess.isChecked()) {
                        threshold.put("lessGreaterThan", "<");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    } else {
                        //x>threshold
                        threshold.put("lessGreaterThan", ">");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        //setLightThreshold is listening
        setLightThreshold.setOnClickListener(new Button.OnClickListener() {
            //if button is clicked
            @Override
            public void onClick(View v) {

                try {
                    //put it in JSON format
                    JSONObject threshold = new JSONObject();
                    //extract info from layout view and add to JSON object
                    threshold.put("opcode", "3");
                    threshold.put("sensorType", "light");
                    threshold.put("thresholdValue", lightThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());


                    //if both checkboxes are pressed, the message is not sent
                    if (lightLess.isChecked() && lightGreater.isChecked()) {
                        //notify user for invalid input
                        Toast.makeText(AddThresholdsActivity.this,
                                "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    //logic for checkboxes, default is greater
                    else if (lightLess.isChecked()) {
                        threshold.put("lessGreaterThan", "<");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    } else {
                        threshold.put("lessGreaterThan", ">");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        setHumidityThreshold.setOnClickListener(new Button.OnClickListener() {
            //if button is clicked
            @Override
            public void onClick(View v) {

                try {
                    //put it in JSON format
                    JSONObject threshold = new JSONObject();
                    //extract info from layout view and add to JSON object
                    threshold.put("opcode", "3");
                    threshold.put("sensorType", "roomHumidity");
                    threshold.put("thresholdValue", humidityThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());


                    //if both checkboxes are pressed, the message is not sent
                    if (humidityLess.isChecked() && humidityGreater.isChecked()) {
                        //notify user for invalid input
                        Toast.makeText(AddThresholdsActivity.this,
                                "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    //logic for checkboxes, default is greater
                    else if (humidityLess.isChecked()) {
                        threshold.put("lessGreaterThan", "<");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    } else {
                        threshold.put("lessGreaterThan", ">");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        setSoilThreshold.setOnClickListener(new Button.OnClickListener() {
            //if button is clicked
            @Override
            public void onClick(View v) {
                try {
                    //put it in JSON format
                    JSONObject threshold = new JSONObject();
                    //extract info from layout view and add to JSON object
                    threshold.put("opcode", "3");
                    threshold.put("sensorType", "soilMoisture");
                    threshold.put("thresholdValue", soilThreshold.getText().toString());
                    threshold.put("potID", potID.getText().toString());

                    //if both checkboxes are pressed, the message is not sent
                    if (soilLess.isChecked() && soilGreater.isChecked()) {
                        //notify user for invalid input
                        Toast.makeText(AddThresholdsActivity.this,
                                "please only check one box", Toast.LENGTH_SHORT).show();
                    }

                    //logic for checkboxes, default is greater
                    else if (soilLess.isChecked()) {
                        threshold.put("lessGreaterThan", "<");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    } else {
                        threshold.put("lessGreaterThan", ">");
                        udpSender.run(ipAddress, threshold.toString(), PORT);
                        udpSender.run(ipAddress, threshold.toString(), 1003);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }
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
