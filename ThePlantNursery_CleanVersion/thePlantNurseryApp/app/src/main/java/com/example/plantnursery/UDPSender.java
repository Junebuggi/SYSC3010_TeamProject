package com.example.plantnursery;

import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

/**
 * this class is used to facilitate the sending of information to the globalServer
 *
 * @author Ruqaya Almalki
 */
public class UDPSender extends Thread {

    private DatagramPacket packet;
    private DatagramSocket socket;


    public void run(String strIP, String str, int port) {
        try {
            socket = new DatagramSocket();
            InetAddress serverAddress = InetAddress.getByName(strIP);
            Log.d("IP Address", serverAddress.toString());

            //pack the message
            packet = new DatagramPacket(str.getBytes(), str.length(), serverAddress, port);

            //dealing with ACK
            //sends 3 times max then stops
            boolean notReceived = true;
            int count = 0;
            while (notReceived) {
                socket.send(packet);
                try {
                    socket.setSoTimeout(3000); //times out in 3s
                    if (count == 0) { //sent it before timeout
                        notReceived = false;
                    }
                } catch (SocketException e) {
                    count++;
                    if (count >= 3) { //already sent 3 times don't send anymore
                        notReceived = false;
                    }
                    e.printStackTrace();
                }
            }

        } catch (UnknownHostException e) {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        } catch (IOException e) {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        } catch (Exception e) {
            e.printStackTrace();
            String error = e.toString();
            Log.e("Error by Sender", error);
        } finally {
            if (socket != null) {
                socket.close();
            }
        }
    }

}
