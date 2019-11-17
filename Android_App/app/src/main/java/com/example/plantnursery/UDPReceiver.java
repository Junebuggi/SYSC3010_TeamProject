package com.example.plantnursery;

import android.util.Log;

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
                    ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1,txt));
                    Log.d("User","Handler send Message");
                    if(true) break;
                }
                //CloseSocket(client);
            }
        }
        catch(IOException e)
        {}
    }

    private void CloseSocket(DatagramSocket socket) throws IOException{
        socket.close();
    }
}