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

class init:
    def start(self):

        f_UTXO = open("UTXO.txt", "w")
        UTXO={
            "371 417":"someone1 paid alice 1000",
            "81 76":"someone2 paid alice 2000",
            "148 31":"someone3 paid bob 3000",
            "397 87":"someone4 paid bob 4000",
        }
        f_UTXO.write(json.dumps(UTXO,indent=4))
        f_UTXO.close()

        f_alice_wallet = open("alice_wallet.txt", "w")
        alice_wallet=[[79,100],[98,141]]
        f_alice_wallet.write(json.dumps(alice_wallet,indent=4))
        f_alice_wallet.close()

        f_bob_wallet = open("bob_wallet.txt", "w")
        bob_wallet=[[101,7],[129,33]]
        f_bob_wallet.write(json.dumps(bob_wallet,indent=4))
        f_bob_wallet.close()

b = init()
b.start()


