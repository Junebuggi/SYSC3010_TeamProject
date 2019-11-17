package com.example.plantnursery;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

public class ViewDataActivity extends AppCompatActivity {

    private String ipAddress = "192.168.1.94";
    private static final int PORT = 1000;
    UDPSender  udpSender;
    private Button viewData;
    private EditText numRecords;
    private CheckBox temp, humidity, light, ultrasonic, soilMoisture;
    String sensorType = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewdata);

        viewData = findViewById(R.id.button7);
        numRecords = findViewById(R.id.editText16);
        temp = findViewById(R.id.checkBox9);
        humidity = findViewById(R.id.checkBox10);
        light = findViewById(R.id.checkBox11);
        ultrasonic = findViewById(R.id.checkBox12);
        soilMoisture = findViewById(R.id.checkBox14);

        viewData.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(ViewDataActivity.this, "view data", Toast.LENGTH_SHORT).show();
                //put it in JSON format
                //[‘opcode’: ‘5’, ‘sensorType’: comma separated string, ‘rowNumbers’: integer]
                JSONObject data = new JSONObject();
                try {
                    data.put("opcode", "5");

                    if(temp.isChecked()){
                        sensorType += "roomTemperature,";
                    }
                    if(humidity.isChecked()){
                        sensorType += "roomHumidity,";
                    }
                    if(light.isChecked()){
                        sensorType += "light,";
                    }
                    if(ultrasonic.isChecked()){
                        sensorType += "waterLevel,";
                    }
                    if(soilMoisture.isChecked()){
                        sensorType += "soilMoisture,";
                    }

                    //remove last comma?

                    data.put("rowNumbers", numRecords.getText().toString());
                    data.put("sensorType", sensorType);

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                udpSender.run(ipAddress, data.toString() , PORT);

                //bring to another page that will display the data
                //need to use recycler view again so can scroll
                //figure out how to output data in a table???
            }
        });




    }

}
