package com.example.plantnursery;

import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class UDPSender extends Thread {

    //port = 8008 from receiver
    //input should be JSON file in the future
    public static void run(String str, int port){
        DatagramSocket socket = null;
        try
        {
            socket = new DatagramSocket();
           // InetAddress serverAddress = InetAddress.getByName(strIP);
            InetAddress serverAddress = InetAddress.getByName("127.0.0.1");

            Log.d("IP Address", serverAddress.toString());

            DatagramPacket packet;

            //send socket
            packet=new DatagramPacket(str.getBytes(),str.length(),serverAddress,port);
            socket.send(packet);

        }
        catch(SocketException e)
        {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
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
