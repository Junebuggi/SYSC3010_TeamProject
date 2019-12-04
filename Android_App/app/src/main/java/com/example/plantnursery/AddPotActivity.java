package com.example.plantnursery;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

public class AddPotActivity extends AppCompatActivity {

    private static final int PORT = 8008;
    private static final String ipAddress = "192.168.137.101";

    private Button addPot;
    private  EditText piID, arduinoID, rmName;
    private UDPSender udpsender;
    private String str;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addpot);


        //needs to be here
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        piID = (EditText)findViewById(R.id.editText7);
        arduinoID = (EditText)findViewById(R.id.editText8);
        addPot = (Button)findViewById(R.id.button8);
        rmName = findViewById(R.id.editText15);


        //create JSON object here


        addPot.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddPotActivity.this, "add a plantzzzz", Toast.LENGTH_SHORT).show();
                //System.out.println("~~~~~~~~\n\n\ni am here " + str );
                //0x02 [‘opcode’: ‘2’, ‘roomID’: Integer, ‘roomName’: String, ‘potID: integer, ‘plantName’: String, ‘owner’:String]
                JSONObject newPot = new JSONObject();
                try {
                    newPot.put("opcode", "2");
                    newPot.put("roomID", piID.getText().toString());
                    newPot.put("ownerID", rmName.getText().toString()); //getting rid of rmName?
                    newPot.put("potID",arduinoID.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }

//                str = "" + piID.getText().toString()+ arduinoID.getText().toString() + plantName.getText().toString() + waterAmount.getText().toString();
                udpsender.run(ipAddress, newPot.toString(), PORT);
            }
        });

        try {
            udpsender = new UDPSender();
            Log.d("User", "Thread start...");
        } catch (Exception e) {
            String str = e.toString();
            Log.e("Error by User", str);
        }

    }

}




