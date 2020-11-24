# The data is provided via a class DataSimulator
import time
import os
import DataSimulator as DSim
import ECC
import hashlib
import multiprocessing
import threading

DS = DSim.DataSimulator()

class blockchian:

    block=[]
    nonce=0
    hash=""
    pre_hash=""
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

    def start(self):

        # f = open("validMessage.txt", "w")
        # f.write("")
        # f.close()

        print("=========build blockchain=========")
        start=int(round(time.time() * 1000))
        for i in range(6):

            # init data
            self.init_data(i)

            # get data
            data = DS.getNewData()

            # validate data
            data = self.validate_signature(data)

            # build tree
            self.buildMerkleTree(data,self.tree,0,0,len(data)-1)
            self.hash_tree[i]=self.tree

            # proof of work
            # self.proof_of_work('Micky')

            p1 = threading.Thread(target=self.proof_of_work, args=('Micky',))
            p2 = threading.Thread(target=self.proof_of_work, args=('Minnie',))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

            # build block
            self.build_block()

            time.sleep(1)

            print(self.block[i])
        print("\n")

        end=int(round(time.time() * 1000))
        print(end-start)

        # proof
        self.proof()

    # init data
    def init_data(self,i):
        self.foundFirst = False
        self.tree=[0]*1000
        self.nonce=0
        self.block_num=i
        self.foundFirst = False
        if not self.pre_hash:
            self.pre_hash="0000"*8
        else:
            self.pre_hash=self.hash

    # validate data
    def validate_signature(self,data):
        msg=""
        for v in data[:]:
            check=(ECC.verify(v['pk'], v["msg"], v["signature"]))
            if check is not True:
                data.remove(v)
            else:
                msg+=v["msg"]+"\n"
                self.hash_msg[v["msg"]]={'block_num':self.block_num,'data':v}

        f = open("validMessage.txt", "a")
        f.write(msg)
        f.close()

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
            self.hash = ECC.hash(data)
            if self.hash[:len(self.difficult)] == self.difficult:
                success=True
                self.foundFirst = True
                print(thread_name, "won!")
            self.nonce+=1

    # build block
    def build_block(self):
        rs_block={'pre_hash':self.pre_hash,'nonce':self.nonce,'merkle_tree':self.tree[0]}
        self.block.append(rs_block)

    # proof
    def proof(self):
        self.log()
        if self.sample in self.hash_msg:
            # proof of merkle_tree
            data=self.hash_msg[self.sample]
            hash=ECC.hash(str(data['data']))
            tree=self.hash_tree[data['block_num']]
            tree_hash=self.find_tree_path(tree,hash)

            print("=========merkle tree proof=========")
            print("tree_leef => "+str(self.sample)+" => "+str(hash))
            for v in self.tree_proof:
                print(v)
            print("tree_root => "+str(tree_hash))
            print("\n")

            # proof block
            print("=========block chain route=========")
            pre_hash=ECC.hash(str(self.block[data['block_num']]['nonce'])+tree_hash+self.block[data['block_num']]['pre_hash'])
            print("pre_hash => "+str(pre_hash))
            for i in range(data['block_num']+1,6):
                print(pre_hash+" => "+str(self.block[i]))
                pre_hash=ECC.hash(str(self.block[i]['nonce'])+self.block[i]['merkle_tree']+self.block[i]['pre_hash'])

            exit()
        else:
            print("false")

    def log(self):
        f = open("resultTransaction.txt", "w")
        f.write(str(self.hash_msg))
        f.close()

        f = open("resultMerkleTree.txt", "w")
        f.write(str(self.hash_tree))
        f.close()

        f = open("resultBlock.txt", "w")
        f.write(str(self.block))
        f.close()

    def find_tree_path(self,tree,hash):
        node_index=tree.index(hash)
        node=tree[node_index]

        if node_index==0:
            return node

        # even
        if(node_index % 2) == 0:
            pair=tree[node_index-1]
            parent=ECC.hash(str(pair + node))
            self.tree_proof.append({"pair":pair,'node':node})

        # odd
        else:
            pair=tree[node_index+1]
            parent=ECC.hash(str(node + pair))
            self.tree_proof.append({"node":node,'pair':pair})

        return self.find_tree_path(tree,parent)

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ( threadName, time.ctime(time.time()) )

b = blockchian()
b.start()
p1 = threading.Thread(target=b.start)
p2 = threading.Thread(target=b.start)
p1.start()
p2.start()
p1.join()
p2.join()


