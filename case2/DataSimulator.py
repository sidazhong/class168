import json
import random
import os

import ECC



#RSAkey.verify(hash,      signature)    # This sig will check out
#RSAkey.verify(hash[:-1], signature)    # This sig will fail

def verifySignature(G, pk, n, msg, s):
    return ECC.verify(G, pk, n, msg, s)

class DataSimulator:

    def __init__(self):
        self.timer = 0

        raw_data = open(os.path.dirname(__file__)+"/transaction.json").read()

        self.headlines = json.loads(raw_data)
        self.keys = self.headlines.keys()


    def getNewData(self):
        key = list(self.keys)[self.timer]
        self.timer = min(self.timer+1, len(self.keys)-1)
        return self.headlines[key]

    def getKeyAndSignature(self,input_text):
        G = ECC.Point(463, -2, 2, (155, 452))
        ecc = ECC.SimpleECC(G)
        signature = ecc.sign(input_text)
        pk = ecc.exportKey()

        pk=pk.replace("Curve( 463 -2 2 ); G( 155 452 ); PK( ", "")
        pk=pk.replace(" ); PKOrder( 149 )", "")
        return {"pk":pk, "signature": [signature[0],signature[1]]}