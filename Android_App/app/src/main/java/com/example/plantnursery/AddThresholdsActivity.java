package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

public class AddThresholdsActivity extends AppCompatActivity {

    private UDPSender udpSender;
    private Button setThreshold;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addthreshold);

        //needs to be here
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //findViewById
        setThreshold = findViewById(R.id.button13);



        setThreshold.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddThresholdsActivity.this, "set Thresholds", Toast.LENGTH_SHORT).show();
                //put it in JSON format
                //JSON[‘opcode’:’3’, ‘lessGreaterThan’:String, ‘thresholdValue’: integer, ‘sensorType’: String, ‘potID’:Integer, ‘roomID’ :Integer]
                JSONObject thresholds = new JSONObject();
//                try {
//                    thresholds.put("opcode", );
//                }

                //str = "1" + "" + plantID.getText().toString()+ " " + notes.getText().toString();
                //udpSender.run(ipAddress, str, 8008);
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
