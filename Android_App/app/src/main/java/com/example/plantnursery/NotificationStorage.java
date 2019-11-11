package com.example.plantnursery;

import java.sql.Time;
import java.util.Date;

/**
 * keeps track of all the notifications given
 * shows notification on the notificationActivity
 */

public class NotificationStorage {
    private String type, message;
    private Date date;
//    private String time;

    public NotificationStorage(String typeOfNotification, String msg, Date dateReceived) {
        type = typeOfNotification;
        message = msg;
        date = dateReceived;
//        time = timeReceived;
    }


    public String getType() {
        return type;
    }

    public String getMessage() {
        return message;
    }

    public Date getDate() {
        return date;
    }

//    public String getTime(){
//        return time;
//    }

    public String toString() {
        return "" + this.getType() + this.getMessage() + this.getDate();
    }

}
