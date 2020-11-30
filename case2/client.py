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

class client:
    def start(self):
        argv=sys.argv
        user_from=argv[1]
        user_to=argv[3]
        amount=int(argv[4])

        UTXO=json.loads(self.file_get_contents("UTXO.txt"))
        user_from_wallet=json.loads(self.file_get_contents(user_from+"_wallet.txt"))
        user_to_wallet=json.loads(self.file_get_contents(user_to+"_wallet.txt"))

        #user_from
        user_amount=0
        user_from_wallet_burn=[]
        for k, v in UTXO.iteritems():
            for kk,vv in enumerate(user_from_wallet):
                #print ("pk: "+str(k))
                #print ("msg: "+str(v))
                #print ("signature: "+str(vv))
                #verify UTXO
                if(ECC.verify(k, v, vv)):
                    user_amount += int(v.split(" ")[3])
                    user_from_wallet_burn.append({"wallet_value":vv,"UXTO_key":k})
                    if(user_amount >= amount):
                        break
            else:
                continue  # only executed if the inner loop did NOT break
            break

        #check if user_from has enough money
        if(user_amount < amount):
            print(user_from+" doesn't have that much money \n")
            exit()

        #burn UTXO and wallet_key
        for k,v in enumerate(user_from_wallet_burn[:]):
            user_from_wallet.remove(v['wallet_value'])
            UTXO.pop(v['UXTO_key'])

        #update user_from_wallet
        new_transaction=[]
        left_amount=user_amount-amount
        if(left_amount!=0):
            lef_msg=user_to+" paid "+user_from+" "+str(left_amount)
            left_token=DS.getKeyAndSignature(lef_msg)
            user_from_wallet.append(left_token['signature'])
            UTXO[left_token['pk']]=lef_msg
            new_transaction.append({"msg":lef_msg,"pk":left_token['pk'],"signature":left_token['signature']})
        f_user_from_wallet = open(user_from+"_wallet.txt", "w")
        f_user_from_wallet.write(json.dumps(user_from_wallet,indent=4))
        f_user_from_wallet.close()

        #update user_to_wallet
        amount_msg=user_from+" paid "+user_to+" "+str(amount)
        amount_toklen=DS.getKeyAndSignature(amount_msg)
        user_to_wallet.append(amount_toklen['signature'])
        UTXO[amount_toklen['pk']]=amount_msg
        new_transaction.append({"msg":amount_msg,"pk":amount_toklen['pk'],"signature":amount_toklen['signature']})
        f_user_to_wallet = open(user_to+"_wallet.txt", "w")
        f_user_to_wallet.write(json.dumps(user_to_wallet,indent=4))
        f_user_to_wallet.close()

        #update UTXO
        f_UTXO = open("UTXO.txt", "w")
        f_UTXO.write(json.dumps(UTXO,indent=4))
        f_UTXO.close()

        #add to transaction
        transaction=json.loads(self.file_get_contents("transaction.json"))
        for k,v in enumerate(new_transaction[:]):
            transaction['0'].insert(0, v)
        f_transaction = open("transaction.json", "w")
        f_transaction.write(json.dumps(transaction,indent=4))
        f_transaction.close()

    def file_get_contents(self,filename):
        with open(filename) as f:
            return f.read()

b = client()
b.start()


