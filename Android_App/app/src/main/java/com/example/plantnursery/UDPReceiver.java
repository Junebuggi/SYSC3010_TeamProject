package com.example.plantnursery;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Date;


class UDPReceiver extends Thread{
    //private static final String ipAddress = "192.168.137.1";
    private static final int PORT =1000;

    private DatagramSocket server = null;
    private int notificationCount = 0;

    public UDPReceiver() throws IOException {
        server = new DatagramSocket(PORT);
        Log.d("User","new server socket");
    }
    public void run(){

//        try {
//            //ensures handler is initialized first before thread is executed
//            Thread.sleep(100);
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
        byte[] byte1024 = new byte[1024];
        DatagramPacket dPacket = new DatagramPacket(byte1024, 100);
        String txt;

        try{
            JSONObject ack = new JSONObject();
            ack.put("opcode", "0");
            Log.d("User","runing run()");
            while(true){
                server.receive(dPacket);
                while(true)
                {
                    txt = new String(byte1024, 0, dPacket.getLength());
                    System.out.println("~~~~~~~~this is the string" + txt);
                    //MainActivity.notificationHistory.add(notificationCount++ +"Threshold" + ": " + "light threshold is met" + " " + new Date());
                    //MainActivity.notificationHistory.add(txt);
                    //ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1,txt));

                    JSONObject obj = new JSONObject(txt);
                    String opcode = obj.getString("opcode");
                    System.out.println("~~~~~~~~got opcode" + txt);
                    switch (opcode){
                        case "0":
                            System.out.println("~~~~ack received!");
                        case "6":
                            try {
                                //ensures handler is initialized first before thread is executed
                                //Thread.sleep(1000);
                                DataTableActivity.exHandler.sendMessage(DataTableActivity.exHandler.obtainMessage(1, txt));

                            }
                             catch (NullPointerException nullPointerException){
                                System.out.println("Catch the Nullpointer exception");
                            }

                        case "E":
                           // udpSender.run(ipAddress, ack.toString() , PORT);

                            try {
                                //ensures handler is initialized first before thread is executed
                                Thread.sleep(1000);
                                ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1, txt));
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            } catch (NullPointerException nullPointerException){
                                System.out.println("Catch the Nullpointer exception");
                            }

                            //ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1, txt));
                        case "D":
                           // udpSender.run(ipAddress, ack.toString() , PORT);
                            System.out.println("~~~~in notification opcode");
                            //send an ACK here
                            //{"opcode" : "D", "sensorArray" : "0,0,0,0,0,0,1,0,0,0,0"}
                            //process the array, add the data
                            String sensorArray = obj.getString("sensorArray");
                            String[] values = sensorArray.split(",");
                            Integer[] sensors = new Integer[values.length];
                            //create list of ints
                            for(int i = 0; i < values.length; i++) {
                                sensors[i] = Integer.parseInt(values[i].trim());
                            }

                            if (sensors[0] == 1) {
                                MainActivity.notificationHistory.add(0, "#" + notificationCount++ +" Threshold" + ": " + "Light threshold is met" + " " + new Date());
                            }
                            if (sensors[1] == 1) {
                                MainActivity.notificationHistory.add(0, "#" + notificationCount++ +" Threshold" + ": " + "Humidity threshold is met" + " " + new Date());
                            }
                            if (sensors[2] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" Threshold" + ": " + "Temperature threshold is met" + " " + new Date());
                            }
                            if (sensors[3] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" Threshold" + ": " + "Soil moisture threshold is met" + " " + new Date());
                            }
                            if (sensors[4] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" Threshold" + ": " + "Water supply is low, please refill" + " " + new Date());
                            }
                            if (sensors[5] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" ERROR" + ": " + "Light sensor error" + " " + new Date());
                            }
                            if (sensors[6] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" ERROR" + ": " + "Humidity sensor error" + " " + new Date());
                            }
                            if (sensors[7] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" ERROR" + ": " + "Soil Moisture sensor error" + " " + new Date());
                            }
                            if (sensors[8] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" ERROR" + ": " + "Ultrasonic sensor error" + " " + new Date());
                            }
                            if (sensors[9] == 1) {
                                MainActivity.notificationHistory.add(0,"#" + notificationCount++ +" ERROR" + ": " + "Water pump wrror" + " " + new Date());
                            }
                    }

                    Log.d("User","Handler send Message");
                    if(true) break;
                }
                //CloseSocket(client);
            }
        }
        catch(IOException e) {}
      catch (JSONException e) {
         e.printStackTrace();
      }

    }

    private void CloseSocket(DatagramSocket socket) throws IOException{
        socket.close();
    }
}