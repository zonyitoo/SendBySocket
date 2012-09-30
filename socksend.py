#!/usr/bin/env python

from socket import *
import os, sys, argparse
import struct

def parse_arguments():
    parser = argparse.ArgumentParser(description='Send File via Socket', prog='Send By Socket')
    parser.add_argument('-a', '--address', help='Send to this address')
    parser.add_argument('-f', '--file', help='File to send')
    return parser.parse_args()

def main():
    args = vars(parse_arguments())
    if not args['address']:
        print "Please specify the destination IP address."
        exit(-1)
    
    if not args['file']:
        print "Please specify the file to send."
        exit(-1)
    
    ADDR = (args['address'], 8000)
    BUFSIZE = 1024
    filename = args['file']
    print "Sending file '%s' to '%s'" % (filename, sys.argv[1])
    FILEINFO_SIZE = struct.calcsize('128s32sI8s')
    FILE_SIZE = os.stat(filename).st_size

    sendSock = socket(AF_INET, SOCK_STREAM)
    sendSock.connect(ADDR)
    
    sind = filename.rfind('/')
    if sind != -1:
        fname = filename[sind + 1:]
    else:
        fname = filename
        
    fhead = struct.pack('128s11I', fname, 0, 0, 0, 0, 0, 0, 0, 0, FILE_SIZE, 0, 0)
    print "Sending Header...\n"
    sendSock.send(fhead)

    fp = open(filename, 'rb')
    hasSend = 0
    while True:
        filedata = fp.read(BUFSIZE)
        if not filedata: break
        sendSock.send(filedata)
        hasSend = hasSend + len(filedata)
        if len(filedata) != 0:
            print 'Sent %.2f%%' % (float(hasSend) / FILE_SIZE * 100, )

    print '\nFinished'
    fp.close()
    sendSock.close()

if __name__ == '__main__':
    main()
