/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Robotics3478
 */
import java.awt.Color;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.*;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.concurrent.Semaphore;

import java.io.*;
import java.net.*;
import java.util.*;
import static java.lang.System.out;
import java.lang.String;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.border.BevelBorder;
import javax.swing.border.EmptyBorder;

/*
public class JavaApplication4 {

    public static void main(String args[]) throws SocketException {
        
        // these netwrok cards are the original network card names
        String networkCard = "net4";      
        //String networkCard2 = "net4";
        //String networkCard3 = "net13";
        
        AC13Comunicator robot1 = new AC13Comunicator();
        //AC13Comunicator robot2 = new AC13Comunicator();
        //AC13Comunicator robot3 = new AC13Comunicator();
        robot1.Connect(networkCard);
        //robot2.Connect(networkCard2);
        
        //robot3.Connect(networkCard3);
        //out.printf("InetAddress: %s\n", robot1.);
        
        //out.printf("Move forward \n");
        int i = 0;
        //*
      //  for (int j=0; j<4; j++)
       // {
            /*i = 0;
            while (i<100)
            {
                robot1.MoveFoward();
                robot2.MoveFoward();
                robot3.MoveFoward();
                i++;
            }
            i = 0;8*/
           // while (i<5)
           // {
//                robot1.MoveFoward();
//                robot2.RotateRight();
  //              robot3.RotateRight();
  //              i++;
           // }
            /*i = 0;
            while (i<100)
            {
                robot1.MoveFoward();
                robot2.MoveFoward();
                robot3.MoveFoward();
                i++;
            }*/
        //}
        
    //    robot1.Disconnect();
        //robot2.Disconnect();

  //  }
    
//}

  //  */
    
    
    

    /******************************************************************/

// Use the code below if you want to find out the name of all the network cards
// connected to this computer.
    
    
    
    
    
   //* 
    
public class JavaApplication4 {

    public static void main(String args[]) throws SocketException {    
    
        Enumeration<NetworkInterface> nets = NetworkInterface.getNetworkInterfaces();
        out.printf("This program prints out all the connections made by all\n");
        out.printf("network interface cards hooked to this computer.\n\n");
        out.printf("Run this to figure out which robot is connected to which card. \n");
        out.printf("\n");
        out.printf("Robot Addresses are generally similar to 192.168.1.100\n");
        out.printf("If the host IP address looks very different than this, then that\n");
        out.printf("network interface card is not connected to a brookstone rover\n");
        out.printf("\n\n");
        for (NetworkInterface netint : Collections.list(nets))
            displayInterfaceInformation(netint);
    }

    static void displayInterfaceInformation(NetworkInterface netint) throws SocketException {
        //out.printf("Display name: %s\n", netint.getDisplayName());
        //out.printf("Name: %s\n", netint.getName());
        Enumeration<InetAddress> inetAddresses = netint.getInetAddresses();
        for (InetAddress inetAddress : Collections.list(inetAddresses)) {
            out.printf("Display name: %s\n", netint.getDisplayName());
            out.printf("Name: %s\n", netint.getName());
            out.printf("InetAddress: %s\n", inetAddress);
            out.printf("Address: %s\n", inetAddress.getAddress());
            out.printf("HostAddress (Robot Address): %s\n", inetAddress.getHostAddress());
            out.printf("Host Name: %s\n\n", inetAddress.getHostName());
        }
        out.printf("\n");
     }
}  

// */
