package com.example.plantnursery;

import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;


/**
 * this class allows users to enter notes about their plant to
 * be sent to the database in the globalServer
 *
 * @author Ruqaya Almalki
 */
public class NotesActivity extends AppCompatActivity {

    private static final String ipAddress = "192.168.137.101"; //globalServer IP
    private static final int PORT = 8008;

    private ImageButton sendNotes; //used to trigger sending info to server
    private EditText plantID, notes; //used to allow users to input data
    private UDPSender udpSender;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addnotes); //reference correct layout

        //compatibility checked and new policy created
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
                //notify users button was pressed and info should be sent
                Toast.makeText(NotesActivity.this, "add a note", Toast.LENGTH_SHORT).show();

                //created new JSONobject and sending the data with inputted values
                JSONObject addNotes = new JSONObject();
                try {
                    addNotes.put("opcode", "1");
                    addNotes.put("potID", plantID.getText().toString());
                    addNotes.put("notes", notes.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                //send data
                udpSender = new UDPSender();
                udpSender.run(ipAddress, addNotes.toString(), PORT);

            }
        });

    }
}
