#Tiia Leinonen 
#Santtu Käpylä 

#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# The modules required
import sys
import socket
import struct
import os 
import binascii


''' 

This program works only in haapa7 (test server of University of Oulu), with hostid 185.38.3.233 and port 10000.

run: python3 CourseWork.py 185.38.3.233 10000 message,
    where the message is at least "HELLO", but if you want to you can add one or several of the following (order doesn't matter, use CAPS)
    MUL - multipart messages
    ENC - encrypting and decrypting of the messages
    PAR - parity
    example: "HELLO MUL ENC" 

''' 

 
def send_and_receive_tcp(address, port, message): 
    print("You gave arguments: {} {} {}".format(address, port, message))
    # create TCP socket
    s = socket.socket()
   
    # connect socket to given address and port
    s.connect((address, port))
    
    #if message contains word ENC, generate keys
    if 'ENC' in message:
        our_keys = random_key_generator()       
        separated_keys = "\r\n".join(our_keys) + "\r\n"
        message += "\r\n" + separated_keys + ".\r\n"
    else:
        our_keys = []
        received = []
    print(message)
    PAR_flag = False
    if 'PAR' in message:
        PAR_flag = True

    # python3 sendall() requires bytes like object. encode the message with str.encode() command
    enc_message = message.encode()   
    
    # send given message to socket
    s.sendall(enc_message)
    
    # receive data from socket
    dec_message = s.recv(1500)   #Could be something like 2048
 
    # data you received is in bytes format. turn it to string with .decode() command
    received_message = dec_message.decode('utf-8')

    # print received data
    print("Received message: " + received_message)
    print()
    
    # close the socket
    s.close()
    
    # Get your CID and UDP port from the message
    words = received_message.split()
    cid = words[1]
    udp_port = int(words[2])
    received_keys = []
    if 'ENC' in message:
        for vo in range(3,(len(words)-1)):
            received_keys.append(words[vo])
    
    # Continue to UDP messaging. You might want to give the function some other parameters like the above mentioned cid and port.
    send_and_receive_udp(address, udp_port, cid, our_keys, received_keys, PAR_flag)
    return
 
 
def send_and_receive_udp(address, port, cid, our_keys, received_keys, PAR_flag):
    '''
    Implement UDP part here.
    '''
    # Open UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket opened in UDP")
    
    # Response
    message = "Hello from " + cid + "\n"
    print(message)

    # Encrypt message
    message = crypt(our_keys, message)

    if(PAR_flag):
        message = make_parity(message)
    
    # Encode message
    enc_message = message.encode()
    
    # Initialize variables
    ACK = True            # True unless PAR implemented      
    EOM = False           # True in last message
    data_remaining = 0    # 0 unless MUL implemented
    #---------------------
    
    # Pack and send data
    data = struct.pack('!8s??HH128s', cid.encode(), ACK, EOM, data_remaining, len(enc_message), enc_message)
    s.sendto(data, (address, port))
    print("Data sent to " + address + " " + str(port) + ".")
    
    # While loop ends when EOM = True
    while(not EOM):
        # Receive and unpack data
        R_data, R_address = s.recvfrom(2048)
        R_enc_address, ACK, EOM, data_remaining, R_content_length, R_enc_message = struct.unpack('!8s??HH128s', R_data)

        # Remove padding
        R_message = R_enc_message.decode('utf-8')
        R_message = R_message[0:(R_content_length)]
        message_list = []
        message_list.append(R_message)
        
        # If MUL, send in parts
        while(data_remaining > 0):

            #print(str(data_remaining))
            R_data, R_address = s.recvfrom(2048)
            R_enc_address, ACK, EOM, data_remaining, R_content_length, R_enc_message = struct.unpack('!8s??HH128s', R_data)
            R_message = R_enc_message.decode('utf-8')
            R_message = R_message[0:(R_content_length)]
            message_list.append(R_message)

        par_msg_list = []
        no_par = False
        
        # if PAR implemented, check parity of received message and get message behind parity bits
        if(PAR_flag == True and not EOM):
            for msg in message_list:
                yes_par, msg = check_parity(msg)
                par_msg_list.append(msg)
                
                # If no parity, raise flag
                if(yes_par == False):
                    print("Received message: '" + msg + "' has no parity!")
                    no_par = True
                    
            # Message without parity bits        
            message_list = par_msg_list 

        #if no parity, request message again    
        if(no_par == True):
            print("False parity")
            ACK = False
            message = "Send again"
            print("Sent: " + message)
            message = crypt(our_keys, message)
            message = make_parity(message)
            
            #Clear the keys meant to be used with message
            for msg in message_list:
                if(len(received_keys) > 0):
                    received_keys.pop(0)
            enc_message = message.encode()
            data = struct.pack('!8s??HH128s', cid.encode(), ACK, EOM, data_remaining, len(message), enc_message)
            s.sendto(data, (address, port))
            #Go back to top (Listen to new message)
            continue

        # Decrypt all but last message
        message_list2 = []
        for viesti in message_list:
            if(not EOM):
                viesti = crypt(received_keys, viesti)
                print("Received: " + viesti)
                message_list2.append(viesti)
            else:
                print("Received: " + viesti)
                break
        
        R_message = "".join(message_list2)
        # Split and reverse
        msg_list = R_message.split()
        msg_list.reverse()

        # Make string
        message = " ".join(msg_list)

        # MUL: divide in chunks
        remain = len(message)
        for piece in pieces(message):
            length = len(piece)
            remain -= length
            print("Sent: " + piece)
            
            #Encrypt message
            message = crypt(our_keys, piece)
            
            # PAR
            if(PAR_flag == True):
                message = make_parity(message)

            # Pack and send 
            enc_message = message.encode()
            data = struct.pack('!8s??HH128s', cid.encode(), ACK, EOM, remain, length, enc_message)
            s.sendto(data, (address, port))
        
    # close the socket
    s.close()
        
    return
    
def random_key_generator():
    """Creates 20 random keys for cryption"""
    keys = []
    for i in range(20):
        a = os.urandom(32)
        keys.append(str(binascii.hexlify(a), 'ascii')) 
    return keys
    
def crypt(keys, message):
    """Crypts the message with given key"""

    #If there are no more keys, just returns the original message
    if(len(keys) == 0):
        return message

    #Taking one key from the list
    key = keys.pop(0)
    enc_msg = ""
    i = 0

    #XOR:ing the message with key
    for ch in message:
        enc_msg += chr(ord(ch) ^ ord(key[i]))
        i += 1
    return enc_msg

def pieces(message, length=64):
    return [message[i:i+length] for i in range(0, len(message), length)]   #line of code from user satomakoto in Stackoverflow

def get_parity(n):   #from CourseWork2019.pdf examples
    while n > 1:
        n = (n >> 1) ^(n & 1)
    return n

def check_parity(message):
    """Checks every character's parity"""
    msg = ""
    for ch in message:
        ch = ord(ch)
        mask = 0b00000001
        pb = mask & ch   # Checks the last bit with the mask
        ch >>= 1
        if(pb == get_parity(ch)):
            ch = chr(ch)
            msg += ch
        else:
            ch = chr(ch)
            msg += ch
            return False, msg
    return True, msg

def make_parity(message):
    msg = ""
    for ch in message:
        ch = ord(ch)              # Char to number
        par_b = get_parity(ch)    # Parity bit for number
        ch <<= 1                  # Bit shifting
        ch += par_b               # Add parity bit to number
        c = chr(ch)               # Return to char
        msg = msg + c
    return msg

def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]
 
    try:
        # Get the server address, port and message from command line arguments
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
    # Print usage instructions and exit if we didn't get proper arguments
        sys.exit(USAGE)
 
    send_and_receive_tcp(server_address, server_tcpport, message)
 
 
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()
