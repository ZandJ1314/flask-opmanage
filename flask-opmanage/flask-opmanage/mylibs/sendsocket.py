#!/usr/bin/evn python
#coding:utf-8
import socket,os,random,traceback
from flask import current_app
bufsize = 8192
def send_socket(SendMsg):
    addr = ("127.0.0.1",1005)
    try:
        SendSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        SendSocket.connect(addr)
        SendSocket.send(SendMsg)
        End = "#zbcyh#"
        total_data = []
        data = ""
        while True:
            data = SendSocket.recv(bufsize)
            if not len(data):
                break
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                last_pair = total_data[-2] + total_data[-1]
                if End in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
        SendRevalue = ''.join(total_data)
        SendSocket.close()
        return SendRevalue
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return '{"code":"-5","codemessage":"connect server error"}'

def NoResultSocket(SendMsg):
    addr = ("127.0.0.1",1005)
    try:
        SendSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        SendSocket.connect(addr)
        SendSocket.send(SendMsg+"#zbcyh#")
        SendSocket.close()
    except Exception,e:
        current_app.logger.error(str(e))