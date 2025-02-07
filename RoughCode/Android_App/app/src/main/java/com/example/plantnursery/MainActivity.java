package com.example.plantnursery;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.Toolbar;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    public static final int PORT = 8008;
    private static final String ipAddress = "192.168.137.101";
    public  static UDPReceiver udpReceiver;

    Button b_status, b_notification, b_data, b_notes, b_addPot, b_thresholds;
    static ArrayList<String> notificationHistory= new ArrayList<>(); //keep track of notifications
    private UDPSender udpSender;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        //compatibility
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //this is here for notifications purposes
        try{
            udpReceiver = new UDPReceiver();
            udpReceiver.start();
            Log.d("User","Thread start...");
        }catch(Exception e)
        {
            String str = e.toString();
            Log.e("Error by User", str);
        }

        //receive text
//        exHandler=new Handler() {
//            @Override
//            public void handleMessage(Message msg) {
//                super.handleMessage(msg);
//                String msgString = (String)msg.obj;
//                Log.d("Handler","Now in Handler");
//                texv_recv.setText(null);
//                texv_recv.setText("Receive: " + msgString);
//            }
//        };
        b_thresholds = findViewById(R.id.button6); //threholds
        b_status = findViewById(R.id.button14); //view status
        b_notification = findViewById(R.id.button); //notifications
        b_data = findViewById(R.id.button2); //view data
        b_notes = findViewById(R.id.button3); //add notes
        b_addPot = findViewById(R.id.button5); //add pot


        //when buttons are clicked
        b_notification.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                //Log.d(TAG, "onClick: hey there!");
                //message at bottom of screen
                //length short--. how long u want it to show for
                Toast.makeText(MainActivity.this, "view notifications", Toast.LENGTH_SHORT).show();//mini b_notification
                startActivity(new Intent(MainActivity.this, NotificationActivity.class));
            }
        });
        b_notes.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "add a note", Toast.LENGTH_SHORT).show();//mini b_notification
                startActivity(new Intent(MainActivity.this, NotesActivity.class));
            }
        });

        b_data.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "view data", Toast.LENGTH_SHORT).show();//mini b_notification
                startActivity(new Intent(MainActivity.this, ViewDataActivity.class));
            }
        });


        b_addPot.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "add a pot", Toast.LENGTH_SHORT).show();//mini b_notification
                startActivity(new Intent(MainActivity.this, AddPotActivity.class));

            }
        });


        b_status.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "view status", Toast.LENGTH_SHORT).show();//mini b_notification

                //send request to globalServer
                //[‘opcode’: ‘5’, ‘sensorType’: comma separated string, ‘rowNumbers’: integer]
//                JSONObject request = new JSONObject();
//                try {
//                    request.put("opcode", "5");
//                    request.put("sensorType", "light, temperature, humidity, soilMoisture"); //did we decide no water supply?
//                    request.put("rowNumbers", 0);
//                    udpSender.run(ipAddress, request.toString() , PORT);
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }

                startActivity(new Intent(MainActivity.this, StatusActivity.class));
            }
        });


        b_thresholds.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "thresholds", Toast.LENGTH_SHORT).show();//mini b_notification
                startActivity(new Intent(MainActivity.this, AddThresholdsActivity.class));
            }
        });



    }
}
