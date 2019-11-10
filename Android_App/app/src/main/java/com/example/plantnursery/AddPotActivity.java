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

public class AddPotActivity extends AppCompatActivity {
//private Button addPot;

    public static Handler exHandler;
    private Button addPot;
    private  EditText piID, arduinoID, plantName, waterAmount;
    private UDPSender udpsender;
    private String ipAddress = "192.168.1.94";
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
        plantName = (EditText)findViewById(R.id.editText9);
        waterAmount = (EditText)findViewById(R.id.editText5);
        addPot = (Button)findViewById(R.id.button8);

        //create JSON object here


       // str = "" + piID.getText().toString()+ arduinoID.getText().toString() + plantName.getText().toString() + waterAmount.getText().toString();

        addPot.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddPotActivity.this, "add a plantzzzz", Toast.LENGTH_SHORT).show();
                //System.out.println("~~~~~~~~\n\n\ni am here " + str );
                str = "" + piID.getText().toString()+ arduinoID.getText().toString() + plantName.getText().toString() + waterAmount.getText().toString();
                udpsender.run(ipAddress, str, 8008);
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




