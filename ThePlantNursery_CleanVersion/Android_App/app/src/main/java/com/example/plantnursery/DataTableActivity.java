package com.example.plantnursery;

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import de.codecrafters.tableview.TableView;
import de.codecrafters.tableview.toolkit.SimpleTableDataAdapter;
import de.codecrafters.tableview.toolkit.SimpleTableHeaderAdapter;

/**
 * table view of the data the user requested
 * handles message received from UDPReceiver
 *
 * @author Ruqaya Almalki
 */
public class DataTableActivity extends AppCompatActivity {

    private TableView tableView;
    public static Handler exHandler;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_datatable);

        tableView = findViewById(R.id.tableView);

        String[] spaceProbeHeaders = {"Sensor", "Value", "Date", "Time"}; //set headers
        tableView.setHeaderBackgroundColor(Color.parseColor("#95F80D")); //set color
        tableView.setHeaderAdapter(new SimpleTableHeaderAdapter(this, spaceProbeHeaders));
        tableView.setColumnCount(4);

        //handling message from receiver
        exHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);

                ArrayList<String[]> list = new ArrayList<>();//store info in arraylist
                String[] stats;
                String sensor = "";
                String name = "";

                try {
                    JSONObject obj = new JSONObject((String) msg.obj); //cast to json
                    JSONArray result = obj.getJSONArray("statsArray"); //get jsonarray

                    if (result.length() == 0) { //inavlid potId, nothing returned
                        Toast.makeText(DataTableActivity.this, "invalid potID, no data found", Toast.LENGTH_SHORT).show();
                    }

                    //iterate through JSONArray and put info under the corrected header
                    for (int i = 0; i < result.length(); i++) {
                        JSONObject jsonObject = result.getJSONObject(i);

                        //checking for what data has been sent to me
                        //letters were used here since it would increase the number of rows that could be sent at once
                        if (jsonObject.has("l")) {
                            sensor = "Light";
                            //unpack object and place in the list
                            name = jsonObject.getString("l");
                            String date = jsonObject.getString("d");
                            String time = jsonObject.getString("T");
                            stats = new String[]{sensor, name, date, time};
                            list.add(stats);
                        }

                        if (jsonObject.has("t")) {
                            sensor = "Temp";
                            //unpack object and place in the list
                            name = jsonObject.getString("t");
                            String date = jsonObject.getString("d");
                            String time = jsonObject.getString("T");
                            stats = new String[]{sensor, name, date, time};
                            list.add(stats);
                        }

                        if (jsonObject.has("h")) {
                            sensor = "Humidity";
                            //unpack object and place in the list
                            name = jsonObject.getString("h");
                            String date = jsonObject.getString("d");
                            String time = jsonObject.getString("T");
                            stats = new String[]{sensor, name, date, time};
                            list.add(stats);
                        }

                        if (jsonObject.has("s")) {
                            sensor = "Moisture";
                            //unpack object and place in the list
                            name = jsonObject.getString("s");
                            String date = jsonObject.getString("d");
                            String time = jsonObject.getString("T");
                            stats = new String[]{sensor, name, date, time};
                            list.add(stats);
                        }

                        if (jsonObject.has("w")) {
                            sensor = "WaterLevel";
                            //unpack object
                            name = jsonObject.getString("w");
                            String date = jsonObject.getString("d");
                            String time = jsonObject.getString("T");
                            stats = new String[]{sensor, name, date, time};
                            list.add(stats);
                        }
                    }

                    //place the arraylist in the table view
                    tableView.setDataAdapter(new SimpleTableDataAdapter(DataTableActivity.this, list));

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }


        };
    }
}
