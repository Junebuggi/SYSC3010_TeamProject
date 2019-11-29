package com.example.plantnursery;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * This class is used to display the current soil moisture, temperature,
 * humidity, light, and water level of a pot in the Plant Nursery
 */
public class ViewStatusActivity extends AppCompatActivity {

    /**
     * these variables correspond with the output views used to display the sensory data
     */
    private TextView textTemp, textHumidity, textLight, textWaterLevel, textSoil;

    /**
     * initialize handler that will be used when app receives the data from UDPReceiver.java
     */
    public static Handler exHandler = null;


    @Override
    /**
     * method invoked when ViewStatusActivity is created
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //set the view of the app to the activity_viewstatus.xml layout in resources
        setContentView(R.layout.activity_viewstatus);

        //find the textviews that are of interest in the layout
        textTemp = findViewById(R.id.textView11);
        textHumidity = findViewById(R.id.textView10);
        textLight = findViewById(R.id.textView13);
        textWaterLevel = findViewById(R.id.textView9);
        textSoil = findViewById(R.id.textView12);


        //checks for compatibility
        //sets policy for UDPReceiver.java thread
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        //Handles the JSON received from UDPReceiver.java so it
        // may be displayed correctly on the layout
        exHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);

                JSONObject obj = null;
                try {
                    obj = new JSONObject((String) msg.obj);

                    JSONArray result = obj.getJSONArray("statsArray");

                    if(result.length() == 0){
                        Toast.makeText(ViewStatusActivity.this, "invalid potID, no data found :(", Toast.LENGTH_SHORT).show();
                    } else{
                        // for (int i = 0; i < result.length(); i++) {
                        JSONObject jsonObject = result.getJSONObject(0);

                        String light = jsonObject.getString("light");
                        String temperature = jsonObject.getString("temperature");
                        String humidity = jsonObject.getString("humidity");
                        String waterLevel = jsonObject.getString("waterDistance");
                        String soil = jsonObject.getString("soilMoisture");
//                        String date = jsonObject.getString("tdate");
//                        String time = jsonObject.getString("ttime");
                        String[] stats = {light, temperature, humidity, waterLevel, soil};

                        textTemp.setText(stats[1]);
                        textHumidity.setText(stats[2]);
                        textWaterLevel.setText(stats[3]);
                        textLight.setText(stats[0]);
                        textSoil.setText(stats[4]);
                        // }
                    }


                } catch (JSONException e) {
                    e.printStackTrace();
                }



//                JSONObject obj = null;
//                try {
//                    //cast string to JSON
//                    obj = new JSONObject((String) msg.obj);
//
//                    //interpret JSON and set text of textviews to corresponding values
//                    textTemp.setText(obj.getString("roomTemperature"));
//                    textHumidity.setText(obj.getString("roomHumidity"));
//                    textWaterLevel.setText(obj.getString("waterDistance"));
//                    textLight.setText(obj.getString("light"));
//                    textSoil.setText(obj.getString("soilMoisture"));
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
                Log.d("Handler", "Now in Handler");
            }
        };
    }
}
