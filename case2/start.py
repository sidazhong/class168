# The data is provided via a class DataSimulator
import time
import os
import DataSimulator as DSim
import ECC
import hashlib
import threading
from threading import Lock
import random
import json

DS = DSim.DataSimulator()
print_lock = Lock()
update_hash_locak = Lock()

class blockchian:

    block=[]
    hash=""
    pre_hash=''
    block_num=0
    tree=[]
    tree_proof=[]

    hash_block={}
    hash_code={}
    hash_msg={}
    hash_tree={}
    sample="nsw opp defends claims of running race campaign"
    difficult="0000"
    foundFirst = False
    pre_hash_init_count = 0
    data_list = []

    nonce=0

    def file_get_contents(self,filename):
        with open(filename) as f:
            return f.read()

    def start(self, thread_name):

        self.data_list=json.loads(self.file_get_contents("transaction.json"))

        print("=========build blockchain=========")
        start=int(round(time.time() * 1000))
        for i in range(5):

            # init data
            self.init_data(i)
            #self.nonce= random.randint(0, 100000)
            self.nonce=0

            # get data
            data = self.data_list[str(i)]

            # validate data
            data = self.validate_signature(data)

            # build tree
            self.buildMerkleTree(data,self.tree,0,0,len(data)-1)
            self.hash_tree[i]=self.tree

            # proof of work
            self.proof_of_work(thread_name)

            # build block
            self.build_block()

            time.sleep(0.1)

            
        print("\n")

        end=int(round(time.time() * 1000))
        print(end-start)

        return True

    # init data
    def init_data(self,i):
        self.foundFirst = False
        self.tree=[0]*1000
        self.block_num=i
        self.foundFirst = False
        if not self.pre_hash or self.pre_hash_init_count < 2:
            self.pre_hash="0000"*8
            self.pre_hash_init_count = self.pre_hash_init_count + 1
        else:
            self.pre_hash=self.hash

    # validate data
    def validate_signature(self,data):
        msg=""
        for v in data[:]:
            check=(ECC.verify(v['pk'], v["msg"], v["signature"]))
            if check is not True and v in data:
                data.remove(v)
            else:
                msg+=v["msg"]+"\n"
                hash=ECC.hash(str(v))
                self.hash_msg[hash]={'block_num':self.block_num,'data':v}

        return data

    # build tree
    def buildMerkleTree(self,data,tree,node,start,end):
        if (start == end):
            hash=ECC.hash(str(data[start]))
            self.hash_code[hash]=data[start]
            self.tree[node]=hash	
            return hash
        else:
            mid=(start+end)/2
            lef_node=(2*node)+1
            rig_node=(2*node)+2
            
            lefHash=self.buildMerkleTree(data,self.tree,lef_node,start,mid)
            rigHash=self.buildMerkleTree(data,self.tree,rig_node,mid+1,end)
            hash=ECC.hash(str(lefHash + rigHash))
            self.tree[node]=hash

            return hash

    # ps aux|grep start.py
    # kill
    # proof of work
    def proof_of_work(self, thread_name):
        success = False
        while not success and not self.foundFirst:
            data=str(self.nonce)+self.tree[0]+self.pre_hash
            hash_temp = ECC.hash(data)
            if hash_temp[:len(self.difficult)] == self.difficult:
                success=True
                with update_hash_locak:
                    self.foundFirst = True
                with print_lock:
                    print thread_name + " won!" 
            if self.foundFirst:
                self.hash = hash_temp

            self.nonce+=1

    # build block
    def build_block(self):
        rs_block={'pre_hash':self.pre_hash,'nonce':self.nonce,'merkle_tree':self.tree[0]}
        with print_lock:
            print(rs_block)
        self.block.append(rs_block)

    def log(self):
        f = open("resultTransaction.txt", "w")
        f.write(json.dumps(self.hash_msg,indent=4))
        f.close()

        f = open("resultMerkleTree.txt", "w")
        f.write(json.dumps(self.hash_tree,indent=4))
        f.close()

        f = open("resultBlock.txt", "w")
        f.write(json.dumps(self.block,indent=4))
        f.close()


# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ( threadName, time.ctime(time.time()) )

b = blockchian()
# b.start()
p1 = threading.Thread(target=b.start, args=('Minnie',))
p2 = threading.Thread(target=b.start, args=('Micky',))
p1.start()
p2.start()
p1.join()
p2.join()

f = open("resultTransaction.txt", "w")
f.write(json.dumps(b.hash_msg,indent=4))
f.close()

f = open("resultMerkleTree.txt", "w")
f.write(json.dumps(b.hash_tree,indent=4))
f.close()

'''
f = open("resultBlock.txt", "w")
f.write(json.dumps(b.block,indent=4))
f.close()
'''

f = open("resultBlock.txt", "w")
pool_block = []
for i in range(0,len(b.block),2):
    if(b.block[i]['nonce'] > b.block[i+1]['nonce']):
        pool_block.append(b.block[i+1])
    else:
        pool_block.append(b.block[i])
f.write(json.dumps(pool_block,indent=4))
f.close()
