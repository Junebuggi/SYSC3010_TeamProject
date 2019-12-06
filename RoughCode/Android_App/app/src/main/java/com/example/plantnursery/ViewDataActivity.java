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

import java.io.IOException;
import java.net.SocketException;

public class ViewDataActivity extends AppCompatActivity {

    private String ipAddress = "192.168.137.101";
    private static final int PORT = 8008;

    UDPSender  udpSender = new UDPSender();
    private Button viewData;
    private EditText numRecords, potID;
    private CheckBox temp, humidity, light, ultrasonic, soilMoisture;
    String sensorType = "";
    JSONObject data;

    public ViewDataActivity() throws IOException, JSONException {
    }

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
        potID = findViewById(R.id.editText3);


        viewData.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Toast.makeText(ViewDataActivity.this, "view data", Toast.LENGTH_SHORT).show();
                //put it in JSON format
                //[‘opcode’: ‘5’, ‘sensorType’: comma separated string, ‘rowNumbers’: integer]
                data = new JSONObject();
                int count = 0;
                try {
                    data.put("opcode", "5");

                    if(temp.isChecked()){
                        sensorType += "temperature,";
                        count++;
                    }
                    if(humidity.isChecked()){
                        sensorType += "humidity,";
                        count++;
                    }
                    if(light.isChecked()){
                        sensorType += "light,";
                        count++;
                    }
                    if(ultrasonic.isChecked()){
                        sensorType += "waterDistance,";
                        count++;
                    }
                    if(soilMoisture.isChecked()){
                        sensorType += "soilMoisture,";
                        count++;
                    }


                    String sensor = sensorType.substring(0, sensorType.lastIndexOf(","));
                    System.out.println("~~~~~~~~~~" + sensor);


                    data.put("potID", potID.getText().toString());
                    data.put("sensorType", sensor);
                    data.put("rowNumbers", numRecords.getText().toString());

                    if(temp.isChecked() && humidity.isChecked() && light.isChecked() && ultrasonic.isChecked() && soilMoisture.isChecked()){
                        if(Integer.parseInt(numRecords.getText().toString()) < 11){
                            Toast.makeText(ViewDataActivity.this, "sent", Toast.LENGTH_SHORT).show();
                            udpSender.run(ipAddress, data.toString() , PORT);
                            startActivity(new Intent(ViewDataActivity.this, DataTableActivity.class));
                        }else{
                            Toast.makeText(ViewDataActivity.this, "row numbers must be less than 11", Toast.LENGTH_SHORT).show();
                        }
                    }


                    if(count <= 4){
                        //count = 0;
                        if((Integer.parseInt(numRecords.getText().toString()) < 11) &&( Integer.parseInt(numRecords.getText().toString()) >0)){
                            Toast.makeText(ViewDataActivity.this, "sent", Toast.LENGTH_SHORT).show();
                            udpSender.run(ipAddress, data.toString() , PORT);
                            startActivity(new Intent(ViewDataActivity.this, DataTableActivity.class));
                        }else{
                            Toast.makeText(ViewDataActivity.this, "row numbers must be less than 11", Toast.LENGTH_SHORT).show();
                        }
                    }




                    //udpSender.run(ipAddress, data.toString() , PORT);
//                    boolean received = true;
//                    int count = 0;
//                    while(received) {
//                        try {
//                            udpSender = new UDPSender();
//                            udpSender.run(ipAddress, data.toString(), PORT);
//                            udpSender.socket.setSoTimeout(1000);
//                            if(count == 0){
//                                received = false;
//                            }
//                            System.out.println("~~~~~~~~~~~ timeout");
//                        } catch (SocketException e) {
//                            try {
//                                count++;
//                                System.out.println("~~~~~~~~~~~" + count);
//                                if (count >= 3) {
//                                    received = false;
//                                }
//                            } finally {
//                                udpSender.socket.close();
//                            }
//                        } catch (JSONException e) {
//                            e.printStackTrace();
//                        } catch (IOException e) {
//                            e.printStackTrace();
//                        }
//                    }

                    //startActivity(new Intent(ViewDataActivity.this, DataTableActivity.class));

                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (NumberFormatException e){
                    Toast.makeText(ViewDataActivity.this, "row numbers must be less than 11", Toast.LENGTH_SHORT).show();
                }
                }
            });

    }

}
