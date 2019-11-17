package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

public class AddRoomActivity extends AppCompatActivity {
    private EditText roomID, roomName;
    private Button sendRoom;
    private String strToSend;
    private UDPSender udpSender;
    private String ipAddress = "192.168.1.94";
    private static final int PORT = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addroom);

        //needs to be here
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        sendRoom = findViewById(R.id.button4);
        roomID = findViewById(R.id.editText3);
        roomName = findViewById(R.id.editText4);


        sendRoom.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddRoomActivity.this, "add a note", Toast.LENGTH_SHORT).show();
                //put it in JSON format
                //JSON [‘opcode’=’7’, ‘roomID’ : integer, ‘roomName’: String]
                JSONObject newRoom = new JSONObject();
                try {
                    newRoom.put("opcode", "7");
                    newRoom.put("roomID", roomID.getText().toString());
                    newRoom.put("roomName", roomName.getText().toString());

                } catch (JSONException e) {
                    e.printStackTrace();
                }

                strToSend = "7" + "" + roomID.getText().toString()+ " " + roomName.getText().toString();
                udpSender.run(ipAddress, newRoom.toString() , PORT);
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
