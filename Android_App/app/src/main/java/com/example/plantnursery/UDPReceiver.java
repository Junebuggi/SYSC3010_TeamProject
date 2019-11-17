package com.example.plantnursery;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;


class UDPReceiver extends Thread{
    private DatagramSocket server = null;
    private static final int PORT = 8008;

    public UDPReceiver() throws IOException {
        server = new DatagramSocket(PORT);
        Log.d("User","new server socket");
    }
    public void run(){

        try {
            //ensures handler is initialized first before thread is executed
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        byte[] byte1024 = new byte[1024];
        //Message msg = new Message();
        //Bundle data = new Bundle();
        DatagramPacket dPacket = new DatagramPacket(byte1024, 100);
        String txt;
        try{
            Log.d("User","runing run()");
            while(true){
                server.receive(dPacket);
                while(true)
                {
                    txt = new String(byte1024, 0, dPacket.getLength());
                    System.out.println("this is the string" + txt);
                    //ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1,txt));

                    JSONObject obj = new JSONObject(txt);
                    String opcode = obj.getString("opcode");
                    switch (opcode){
                        case "D":
                            //process the array, add the data
                            String errors = obj.getString("sensorArray");
                            MainActivity.notificationHistory.add(txt);
                        case "0":
                            //ACK
                        case "6":
                            //stats are sent
                            //ViewDataActivity.exHandler.sendMessage(ViewDataActivity.exHandler.obtainMessage(1, txt));
                        case "E":
                            ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(2, txt));
                    }


                    Log.d("User","Handler send Message");
                    if(true) break;
                }
                //CloseSocket(client);
            }
        }
        catch(IOException e)
        {} catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void CloseSocket(DatagramSocket socket) throws IOException{
        socket.close();
    }
}