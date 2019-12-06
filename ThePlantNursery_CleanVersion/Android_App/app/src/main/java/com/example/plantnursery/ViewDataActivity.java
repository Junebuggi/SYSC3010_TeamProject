package com.example.plantnursery;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Sends data needed to fetch data for the tableview in the DataTableActivity.java class
 * user inputs the potID of interest, the number of rows they would like to retrieve, and the sensors
 * they would like to view the backlog of
 *
 * @author Ruqaya Almalki
 */
public class ViewDataActivity extends AppCompatActivity {

    private String ipAddress = "192.168.137.101"; //globalServer IP
    private static final int PORT = 8008;

    UDPSender udpSender;
    private Button viewData; //triggers sending the data
    private EditText numRecords, potID;
    private CheckBox temp, humidity, light, ultrasonic, soilMoisture;
    String sensorType = "";
    JSONObject data;

    public ViewDataActivity() {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewdata);

        viewData = findViewById(R.id.button7); //triggers sending data
        numRecords = findViewById(R.id.editText16);
        potID = findViewById(R.id.editText3);

        //checkboxes used to decrease user input errors
        temp = findViewById(R.id.checkBox9);
        humidity = findViewById(R.id.checkBox10);
        light = findViewById(R.id.checkBox11);
        ultrasonic = findViewById(R.id.checkBox12);
        soilMoisture = findViewById(R.id.checkBox14);


        //collects and sends data when the view data button is clicked in the layout
        viewData.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //create new JSON object to be sent
                data = new JSONObject();
                int count = 0;
                try {
                    data.put("opcode", "5");

                    if (temp.isChecked()) {
                        sensorType += "temperature,";
                        count++;
                    }
                    if (humidity.isChecked()) {
                        sensorType += "humidity,";
                        count++;
                    }
                    if (light.isChecked()) {
                        sensorType += "light,";
                        count++;
                    }
                    if (ultrasonic.isChecked()) {
                        sensorType += "waterDistance,";
                        count++;
                    }
                    if (soilMoisture.isChecked()) {
                        sensorType += "soilMoisture,";
                        count++;
                    }

                    String sensor = sensorType.substring(0, sensorType.lastIndexOf(",")); //remove last ',''
                    data.put("sensorType", sensor);
                    data.put("potID", potID.getText().toString());
                    data.put("rowNumbers", numRecords.getText().toString());

                    //all five of them are picked
                    if (count >= 5) {
                        if (Integer.parseInt(numRecords.getText().toString()) < 11) { //max limit for socket
                            //notify user button is clicked and info is sent
                            Toast.makeText(ViewDataActivity.this, "sent", Toast.LENGTH_SHORT).show();

                            //send data to server
                            udpSender = new UDPSender();
                            udpSender.run(ipAddress, data.toString(), PORT);
                            startActivity(new Intent(ViewDataActivity.this, DataTableActivity.class));
                        } else {
                            //rows limit, inform user
                            Toast.makeText(ViewDataActivity.this, "row numbers must be less than 11", Toast.LENGTH_SHORT).show();
                        }
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (NumberFormatException e) {
                    //must input a number for rowNumbers
                    Toast.makeText(ViewDataActivity.this, "row numbers must be a number", Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                } catch (Exception e){
                    Toast.makeText(ViewDataActivity.this, "please fill in all fields", Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                }
            }
        });

    }

}
