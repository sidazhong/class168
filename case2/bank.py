# The data is provided via a class DataSimulator
import time
import os
import DataSimulator as DSim
import ECC
import hashlib
import multiprocessing
import threading
import random
import json
import sys

DS = DSim.DataSimulator()

class bank:
    def start(self):
        UTXO=json.loads(self.file_get_contents("UTXO.txt"))
        alice_wallet=json.loads(self.file_get_contents("alice_wallet.txt"))
        bob_wallet=json.loads(self.file_get_contents("bob_wallet.txt"))

        #user
        alice_amount=0
        bob_amount=0
        for k, v in UTXO.iteritems():
            for vv in alice_wallet:
                if(ECC.verify(k, v, vv)):
                    alice_amount += int(v.split(" ")[3])

            for vv in bob_wallet:
                if(ECC.verify(k, v, vv)):
                    bob_amount += int(v.split(" ")[3])

        print("Alice: "+str(alice_amount))
        print("Bob: "+str(bob_amount))
                    
    def file_get_contents(self,filename):
        with open(filename) as f:
            return f.read()

b = bank()
b.start()


