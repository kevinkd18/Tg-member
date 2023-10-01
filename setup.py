#!/bin/env python3
# code by: Termux Professor

import os
import configparser

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    os.system('clear')
    print(f"""
    {re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
    {re}╚═╗{cy}├┤  │ │ │├─┘
    {re}╚═╝{cy}└─┘ ┴ └─┘┴

                   Version : 1.01
    {re}Subscribe Termux Professor on Youtube
    {cy}www.youtube.com/c/TermuxProfessorYT
    """)

banner()
print(gr + "[+] Installing requirements ...")
os.system('python3 -m pip install telethon')
os.system('pip3 install telethon')
banner()
os.system("touch config.data")
cpass = configparser.RawConfigParser()
cpass.add_section('cred')
xid = input(gr + "[+] Enter API ID: " + re)
cpass.set('cred', 'id', xid)
xhash = input(gr + "[+] Enter API Hash: " + re)
cpass.set('cred', 'hash', xhash)
xphone = input(gr + "[+] Enter your phone number (with country code): " + re)
cpass.set('cred', 'phone', xphone)
setup = open('config.data', 'w')
cpass.write(setup)
setup.close()
print(gr + "[+] Setup complete!")
print(gr + "[+] Now you can run the scraper or adder script.")
print(gr + "[+] Make sure to read the documentation for installation and API setup.")
print(gr + "[+] https://github.com/termuxprofessor/TeleGram-Scraper-Adder/blob/master/README.md")
