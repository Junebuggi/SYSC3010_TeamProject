package com.example.plantnursery;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.concurrent.TimeoutException;

public class UDPSender extends Thread {


    DatagramPacket packet;
    //UDPReceiver udpReceiver = new UDPReceiver();
    int count = 0;
    DatagramSocket socket = null;

    public UDPSender() throws IOException, JSONException {
    }
    //implemtn ack in this thread..i think receiving ack


    public void run(String strIP, String str, int port) throws IOException {
        //DatagramSocket socket = null;
        try
        {
            socket = new DatagramSocket();
            InetAddress serverAddress = InetAddress.getByName(strIP);
            Log.d("IP Address", serverAddress.toString());

            //DatagramPacket packet;

            //send socket
            packet=new DatagramPacket(str.toString().getBytes(),str.length(),serverAddress,port);
            System.out.println("~~~~~~~~~~~~/n/n/nsendinggggggggg");
            socket.send(packet);
            System.out.println("~~~~~/n/n/nsent");

        }
        catch(UnknownHostException e)
        {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        }
        catch(IOException e)
        {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        }
        catch(Exception e)
        {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        }
        finally{
            if(socket != null){
                socket.close();
            }
        }
    }

}
