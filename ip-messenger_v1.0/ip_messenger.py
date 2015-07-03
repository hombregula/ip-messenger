#!/bin/sh
# launcher.sh

import requests
import smtplib
import time

import os

class mail_ip ():
    def __init__(self,user, psw, to,public_ip_old):
        self.user=user
        self.psw=psw
        self.to=to

        self.public_ip_old=public_ip_old
        self.public_ip= self.return_public_ip()

        if self.public_ip <> self.public_ip_old:
            myfile = open(os.path.dirname(os.path.abspath(__file__)) + '/public_ip', 'w')
            myfile.write(self.public_ip + '\n')

            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.ehlo()
            self.server.starttls()

            self.login(self.user, self.psw)
            self.send_mail(self.user, self.to, self.public_ip)
            self.server.close()

    def login(self, user, psw) :
        self.server.login(user,psw)

    def send_mail (self, user, to, public_ip):
        self.server.sendmail(user, to, public_ip)

    def return_public_ip (self):
        r = requests.get(r'http://jsonip.com')
        return r.json()['ip']

def send_ip_hora ():
    diccionario_datos = {}
    arch = open(os.path.dirname(os.path.abspath(__file__)) + '/period', 'r')
    for line in arch:
        diccionario_datos['period']=[line.strip()]

    arch = open(os.path.dirname(os.path.abspath(__file__)) + '/user_mail', 'r')
    for line in arch:
        diccionario_datos['user_mail']=[line.strip()]

    arch = open(os.path.dirname(os.path.abspath(__file__)) + '/user_psw', 'r')
    for line in arch:
        diccionario_datos['user_psw']=[line.strip()]

    arch = open(os.path.dirname(os.path.abspath(__file__)) + '/mail_to', 'r')
    for line in arch:
        diccionario_datos['mail_to']=[line.strip()]

    arch = open(os.path.dirname(os.path.abspath(__file__)) + '/public_ip', 'r')
    for line in arch:
        diccionario_datos['public_ip']=[line.strip()]

    return diccionario_datos


while True:
    # store the value of the different variables of the files
    data = send_ip_hora()

    # check if ip address has changed. If it has change, send the mail
    send_ip = mail_ip(data['user_mail'][0],data['user_psw'][0],data['mail_to'][0],data['public_ip'][0])

    # sleep during the indicated period
    time.sleep (int(data['period'][0]))

