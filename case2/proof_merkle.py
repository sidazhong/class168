# The data is provided via a class DataSimulator
import time
import os
import DataSimulator as DSim
import ECC
import hashlib
import json

DS = DSim.DataSimulator()
class proof_merkle:
    tree_proof=[]
    hash_msg={}
    hash_tree={}
    block=[]

    sample="nsw opp defends claims of running race campaign"

    def start(self):
        print("=========proof merkle tree path=========")

        self.hash_msg=json.loads(self.file_get_contents("resultTransaction.txt"))
        self.hash_tree=json.loads(self.file_get_contents("resultMerkleTree.txt"))
        self.block=json.loads(self.file_get_contents("resultBlock.txt"))

        # proof
        self.proof()


    def file_get_contents(self,filename):
        with open(filename) as f:
            return f.read()

    # proof
    def proof(self):
        if self.sample in self.hash_msg:
            # proof of merkle_tree
            data=self.hash_msg[self.sample]
            hash=ECC.hash(str(data['data']))
            tree=self.hash_tree[str(data['block_num'])]
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


obj = proof_merkle()
obj.start()
