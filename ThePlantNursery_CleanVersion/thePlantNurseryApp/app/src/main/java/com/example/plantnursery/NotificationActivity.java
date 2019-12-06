package com.example.plantnursery;

import android.annotation.SuppressLint;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

/**
 * displays all the notifications sent to the app
 *
 * @author Ruqaya Almalki
 */
public class NotificationActivity extends AppCompatActivity {

    private RecyclerView mRecyclerView;
    private RecyclerView.LayoutManager mLayoutManager;
    private RecyclerView.Adapter mAdapter;


    @SuppressLint("HandlerLeak")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications); //shows correct layout

        mRecyclerView = findViewById(R.id.recycler_view); //allows notifications to be scrollable

        //Recycler View looks
        mLayoutManager = new LinearLayoutManager(this);
        mAdapter = new NotificationAdapter(MainActivity.notificationHistory);
        mRecyclerView.setLayoutManager(mLayoutManager);
        mRecyclerView.setAdapter(mAdapter);

    }
}
