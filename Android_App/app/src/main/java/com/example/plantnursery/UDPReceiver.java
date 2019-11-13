package com.example.plantnursery;

import android.util.Log;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Date;

import org.json.*;

public class UDPReceiver extends Thread {

    private DatagramSocket server = null;
    private static final int PORT = 8008;
    //private String activity = "ViewStatusActivity";

    public UDPReceiver() throws IOException {
        server = new DatagramSocket(PORT);
        Log.d("User", "new server socket");
    }

    public void run() {

        byte[] byte1024 = new byte[1024];
        //Message msg = new Message();
        //Bundle data = new Bundle();
        DatagramPacket dPacket = new DatagramPacket(byte1024, 100);
        String txt;
        try {
            Log.d("User", "runing run()");
            while (true) {
                server.receive(dPacket);
                while (true) {
                    txt = new String(byte1024, 0, dPacket.getLength());
                    String data = new String(dPacket.getData()).trim();
//                    MainActivity.notificationHistory.add(data);

                    JSONObject obj = new JSONObject(data);
                    String opcode = obj.getString("Opcode");
                    switch (opcode){
                        case "D":
                            //process the array, add the data
                            String errors = obj.getString("sensorArray");
                            MainActivity.notificationHistory.add(data);
                        case "0":
                            //ACK
                        case "6":
                            //stats are sent
                            //ViewDataActivity.exHandler.sendMessage(ViewDataActivity.exHandler.obtainMessage(1, txt));
                        case "E":
                            ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1, txt));


                    }


                    System.out.println(obj.toString());

                    //ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1, txt));
//                    JSONObject obj = new JSONObject("data"); //cast to JSON
//                    String opCode = obj.getString("OpCode"); //get string associated with JSON
//                    switch (opCode) {
//                        case "0x05" :
//                            ViewStatusActivity.exHandler.sendMessage(ViewStatusActivity.exHandler.obtainMessage(1,txt));
//                        case "0x04" :
//                            //NotificationActivity.exHandler.sendMessage(NotificationActivity.exHandler.obtainMessage(1,txt));
//                    }

                    Log.d("User", "Handler send Message");
                    if (true) break;
                }
                //CloseSocket(client);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
//        catch(IOException e)
//        {} catch (JSONException e) {
//            e.printStackTrace();
//        }
    }

    private void CloseSocket(DatagramSocket socket) throws IOException {
        socket.close();
    }
}
