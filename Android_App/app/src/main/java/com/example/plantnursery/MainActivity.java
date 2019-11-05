package com.example.plantnursery;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

   // private static final String TAG = "MainActivity";
    Button button;
    Button button2;
    Button button3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //links it to the first button (notifications)
        button = findViewById(R.id.button);
        button2 =
        button3 = findViewById(R.id.button3);


        //for each button when u click
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                //Log.d(TAG, "onClick: hey there!");
                //message at bottom of screen
                //length short--. how long u want it to show for
                Toast.makeText(MainActivity.this, "Welcome", Toast.LENGTH_SHORT).show();//mini notification
                startActivity(new Intent(MainActivity.this, NotificationActivity.class));
            }
        });
        button3.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                //Log.d(TAG, "onClick: hey there!");
                //message at bottom of screen
                //length short--. how long u want it to show for
                Toast.makeText(MainActivity.this, "Welcome", Toast.LENGTH_SHORT).show();//mini notification
                startActivity(new Intent(MainActivity.this, NotesActivity.class));
            }
        });

        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            //when clicked everything in this will get executed
            public void onClick(View v) {
                //Log.d(TAG, "onClick: hey there!");
                //message at bottom of screen
                //length short--. how long u want it to show for
                Toast.makeText(MainActivity.this, "viewData", Toast.LENGTH_SHORT).show();//mini notification
                startActivity(new Intent(MainActivity.this, NotesActivity.class));
            }
        });
    }
}
