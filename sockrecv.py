#!/usr/bin/env python 

import socket
import struct
import sys, argparse, fcntl

def parse_arguments():
    parser = argparse.ArgumentParser(description='Receive File via Socket', prog='Send By Socket')
    parser.add_argument('-a', '--address', help="Your IP Address")
    return parser.parse_args()

def get_ip_address(s, ifname):
    return socket.inet_ntoa(fcntl.ioctl(  
        s.fileno(),  
        0x8915, # SIOCGIFADDR  
        struct.pack('256s', ifname[:15])  
    )[20:24])

def main():
    args = vars(parse_arguments())
    if not args['address']:
        print "You must specify your address"
        exit(-1)
        
    recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    BUFSIZE = 1024
    FILEINFO_SIZE = struct.calcsize('128s32sI8s')

    ADDR = (args['address'], 8000)

    recvSock.bind(ADDR)
    recvSock.listen(1)

    print "Waiting..."
    conn, addr = recvSock.accept()
    print "Send From ", addr[0]

    fhead = conn.recv(FILEINFO_SIZE)
    filename, temp1, filesize, temp2 = struct.unpack('128s32sI8s', fhead)
    #print filename, temp1, filesize, temp2
    #print filename, len(filename), type(filename)
    #print filesize
    print "filename='%s', size='%d'" % (filename, filesize)

    filename = 'new_' + filename.strip('\0')
    print "Save in ", filename, '\n'

    fp = open(filename, 'wb')
    restsize = filesize
    while True:
        if restsize > BUFSIZE:
            filedata = conn.recv(BUFSIZE)
        else:
            filedata = conn.recv(restsize)

        if not filedata: break
        fp.write(filedata)
        restsize = restsize - len(filedata)
        if len(filedata) != 0:
            print 'Remain %.2f%%' % (float(restsize) / filesize * 100)
        if restsize == 0: break

    fp.close()
    recvSock.close()

    print "\nRecv Finished"

if __name__ == '__main__':
    main()
