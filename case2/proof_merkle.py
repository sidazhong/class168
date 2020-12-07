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

    sample="388a128e1d99a098efac9e2cae826329"

    def start(self):

        #pre_hash=ECC.hash(str(78765)+"1b83ee373d3be4246c09a68e9b15491b"+"00003abd31767349f28b19d642ab8eca")
        #print(pre_hash)
        #exit()


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
            tree_root=self.find_tree_path(tree,tree.index(self.sample),hash)

            print("=========merkle tree proof=========")
            print("tree_leef => "+str(self.sample))
            for v in self.tree_proof:
                print(v)
            print("tree_root => "+str(tree_root))
            print("\n")

            # proof block
            print("=========block chain route=========")


            #print(data['block_num'])
            #print(str(self.block[data['block_num']]['nonce']-1))
            #print(self.block[data['block_num']]['pre_hash'])

            print("mrekle tree root: "+tree_root)
            pre_hash=ECC.hash(str(self.block[data['block_num']]['nonce']-1)+tree_root+self.block[data['block_num']]['pre_hash'])

            print("pre_hash: "+str(pre_hash))
            for i in range(data['block_num']+1,5):
                print("{nonce: " + str(self.block[i]['nonce']) + ", pre_hash: " + str(pre_hash) + ", merkle_tree: " + str(self.block[i]['merkle_tree'])+ "}")
                pre_hash=ECC.hash(str(self.block[i]['nonce']-1)+self.block[i]['merkle_tree']+pre_hash)
            exit()
        else:
            print("false")

    def find_tree_path(self,tree,node_index,node_hash):
        if node_index==0:
            return node_hash

        # even
        if(node_index % 2) == 0:
            pair_hash=tree[node_index-1]
            parent_node_index=(node_index/2)-1
            parent_node_hash=ECC.hash(str(pair_hash + node_hash))
            self.tree_proof.append({"pair":pair_hash,'node':node_hash})

        # odd
        else:
            pair_hash=tree[node_index+1]
            parent_node_index=((node_index+1)/2)-1
            parent_node_hash=ECC.hash(str(node_hash + pair_hash))
            self.tree_proof.append({"node":node_hash,'pair':pair_hash})

        return self.find_tree_path(tree,parent_node_index,parent_node_hash)


obj = proof_merkle()
obj.start()
