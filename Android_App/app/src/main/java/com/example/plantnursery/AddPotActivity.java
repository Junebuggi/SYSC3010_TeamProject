package com.example.plantnursery;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

public class AddPotActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addpot);

        EditText piID = findViewById(R.id.editText7);
        EditText arduinoID = findViewById(R.id.editText8);
        EditText PlantName = findViewById(R.id.editText9);
        EditText waterAmount = findViewById(R.id.editText5);
        Button addPot = findViewById(R.id.button8);

        final String str = new String("" + piID + arduinoID + PlantName + waterAmount);

        UDPSender udpSender = new UDPSender();

        addPot.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                UDPSender.run(str, 8008);
            }
        });
    }




   }
