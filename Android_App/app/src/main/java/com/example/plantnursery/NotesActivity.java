package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

public class NotesActivity extends AppCompatActivity {

    private ImageButton sendNotes;
    private EditText plantID, notes;
    private String str;
    private UDPSender udpSender;
    private static final String ipAddress = "192.168.137.101";
    private static final int PORT = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addnotes);

        //needs to be here
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        sendNotes = findViewById(R.id.imageButton2);
        plantID = findViewById(R.id.editText2);
        notes = findViewById(R.id.editText);

        sendNotes.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(NotesActivity.this, "add a note", Toast.LENGTH_SHORT).show();
                //put it in JSON format
                //JSON[‘opcode’: ‘1’, ‘potID’: integer, ‘notes’: String]
                JSONObject addNotes = new JSONObject();
                try {
                    addNotes.put("opcode", "1");
                    addNotes.put("potID", plantID.getText().toString());
                    addNotes.put("notes", notes.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //str = "1" + "" + plantID.getText().toString()+ " " + notes.getText().toString();
                //System.out.println("~~~~~~~~\n\n\ni am here " + PORT);
                System.out.println(addNotes.toString());
                udpSender.run(ipAddress, addNotes.toString(), PORT);
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
