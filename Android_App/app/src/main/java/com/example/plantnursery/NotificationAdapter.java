package com.example.plantnursery;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

/**
 * notification adapter used to bind the view with the rows that appear periodically
 *
 * @author Ruqaya Almalki
 */

public class NotificationAdapter extends RecyclerView.Adapter<NotificationAdapter.ViewHolder> {

    //storing the notifications
    private ArrayList<String> notifications;

    public NotificationAdapter(ArrayList<String> dataset) {
        notifications = dataset;
    }

    @Override
    public NotificationAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.row, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(NotificationAdapter.ViewHolder holder, int position) {
        holder.typeOfNotification.setText(notifications.get(position));
    }

    @Override
    public int getItemCount() {
        return notifications.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView typeOfNotification;

        public ViewHolder(View itemView) {
            super(itemView);

            typeOfNotification = itemView.findViewById(R.id.title);
        }
    }
}
