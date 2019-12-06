package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * allows users to add a pot to their system and/or register a new pot with the server
 *
 * @author Ruqaya Almalki
 */
public class AddPotActivity extends AppCompatActivity {

    private static final String ipAddress = "192.168.137.101"; //globalServer IP
    private static final int PORT = 8008;

    private Button addPot;
    private EditText piID, arduinoID, OwnerID;
    private UDPSender udpSender;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addpot); //reference layout

        //compatibility checked and new policy created
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //use edit text initialized
        piID = findViewById(R.id.editText7);
        arduinoID = findViewById(R.id.editText8);
        OwnerID = findViewById(R.id.editText15);

        //button to trigger sending of information
        addPot = findViewById(R.id.button8);


        addPot.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //notify user button is clicked by a toast
                Toast.makeText(AddPotActivity.this, "add a pot", Toast.LENGTH_SHORT).show();

                //create JSON object and add all necessary values
                JSONObject newPot = new JSONObject();
                try {
                    newPot.put("opcode", "2");
                    newPot.put("roomID", piID.getText().toString());
                    newPot.put("ownerID", OwnerID.getText().toString());
                    newPot.put("potID", arduinoID.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //send information
                udpSender = new UDPSender();
                udpSender.run(ipAddress, newPot.toString(), PORT);

            }
        });
    }
}




