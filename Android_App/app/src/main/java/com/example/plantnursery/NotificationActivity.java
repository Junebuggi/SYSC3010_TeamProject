package com.example.plantnursery;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.sql.Time;
import java.util.ArrayList;
import java.util.Date;

public class NotificationActivity extends AppCompatActivity {
    public static Handler exHandler;
    private static int count = 0;
    private RecyclerView mRecyclerView;
    private RecyclerView.LayoutManager mLayoutManager;
    private RecyclerView.Adapter mAdapter;
    //static ArrayList<String> notificationHistory = new ArrayList<>();;
    //private ArrayList<String> notificationHistory;

    @SuppressLint("HandlerLeak")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notifications);

        mRecyclerView = (RecyclerView) findViewById(R.id.recycler_view);
        //notificationHistory = new ArrayList<>();

        //Recycler View looks
        mLayoutManager = new LinearLayoutManager(this);
        //mRecyclerView.setHasFixedSize(false);
        mAdapter = new NotificationAdapter(MainActivity.notificationHistory);
        mRecyclerView.setLayoutManager(mLayoutManager);
        mRecyclerView.setAdapter(mAdapter);

    }
}
