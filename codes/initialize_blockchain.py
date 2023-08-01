
import time
import subprocess
from Savoir import Savoir

#----------------------------Admin functions---------------------------------------#
class AdminNode:
	def __init__(self, name):
		self.name = name
	
	def create_blockchain(self):
		subprocess.check_call(['./initialize_blockchain.sh', self.name, '-a', 'create'])

	def start_admin_blockchain(self):
		subprocess.check_call(['./initialize_blockchain.sh', self.name, '-a', 'run'])

	def stop_admin_blockchain(self):
		subprocess.check_call(['./initialize_blockchain.sh', self.name, '-a', 'stop'])

	def get_admin_object(self):
		admin_config_file = open('/home/ken/.multichain/'+self.name+'/multichain.conf', 'r')
		rpcuser = ''
		rpcpasswd = ''

		lines = admin_config_file.readlines()	
		for line in lines:
			line_x = line.strip()
			#print ("line : " + line_x)
			tokens = line_x.split("=")
			if(tokens[0] == "rpcuser"):
				rpcuser = tokens[1]
			elif(tokens[0] == "rpcpassword"):
				rpcpasswd = tokens[1]
			else:
				continue
		#print("rpcuser : " + rpcuser)
		#print("rpcpasswd : " + rpcpasswd) 
		
		admin_params_file = open('/home/ken/.multichain/'+self.name+'/params.dat', 'r')
		rpcport = ''

		lines = admin_params_file.readlines()	
		for line in lines:
			line_x = line.strip()
			tokens = line_x.split(" = ")
			if(tokens[0] == "default-rpc-port"):
				rpcport = tokens[1].split('#')[0].strip()
				#print ("rpcport : " + rpcport)
			else:
				continue

		if (rpcport != ''):
			return Savoir(rpcuser, rpcpasswd, 'localhost', rpcport, self.name)
			

	def initialize_energy_ecoin_assets(self):
		address = self.get_admin_object().getaddresses()[0]
		subprocess.check_call(['./initialize_assets.sh', self.name, address])
#----------------------------------Peer functions---------------------------------#
#self.kind is prosumer/ consumer. self.index is its position
#this shall form blockchain name e.g. prosumer1

class PeerNode:
	def __init__(self, admin_object, admin_name, kind, index):
		self.admin_object = admin_object
		self.admin_name = admin_name
		self.kind = kind
		self.index = index

	def calculate_peer_port(self):
		#using ephemeral ports
		return 35000 + self.index*3

	def create_peer_blockchain(self):
		parent_tcpport = self.admin_object.getinfo()['port']
		print ("parent_tcpport\t\t"+str(parent_tcpport))
		new_node_tcpport = self.calculate_peer_port()
		subprocess.check_call(['./initialize_blockchain.sh', self.admin_name, '-p', self.kind+str(self.index), str(parent_tcpport), str(new_node_tcpport), 'create'])


	def start_peer_node(self):
		new_node_tcpport = self.calculate_peer_port()
		subprocess.check_call(['./initialize_blockchain.sh', self.admin_name, '-p', self.kind+str(self.index),  str(new_node_tcpport), 'run'])


	def stop_peer_node(self):
		new_node_tcpport = self.calculate_peer_port()
		subprocess.check_call(['./initialize_blockchain.sh', self.admin_name, '-p', self.kind+str(self.index),  str(new_node_tcpport), 'stop'])


	def get_peer_object(self):
		#TODO: modify source dir elow to be functional on any machine
		peer_config_file = open('/home/ken/.multichain-'+self.kind+str(self.index)+'/'+self.admin_name+'/multichain.conf', 'r')
		rpcuser = ''
		rpcpasswd = ''

		lines = peer_config_file.readlines()	
		for line in lines:
			line_x = line.strip()
			#print ("line : " + line_x)
			tokens = line_x.split("=")
			if(tokens[0] == "rpcuser"):
				rpcuser = tokens[1]
			elif(tokens[0] == "rpcpassword"):
				rpcpasswd = tokens[1]
			else:
				continue
		#print("rpcuser : " + rpcuser)
		#print("rpcpasswd : " + rpcpasswd) 
		
		if(rpcuser != '' and rpcpasswd != ''):
			return Savoir(rpcuser, rpcpasswd, 'localhost', str(self.calculate_peer_port() - 1), self.admin_name)

	def request_energy_issue_permission(self):
		address = self.get_peer_object().getaddresses()[0]
		print("Peer address\t\t"+address)
		print(self.admin_object.grant(address, "energy.issue"))
		
	def issue_energy(self,amount_of_energy):
		peer_object = self.get_peer_object()
		print(peer_object.issuemore(peer_object.getaddresses()[0], "energy", amount_of_energy))
		print("Multibalances :: \n" + str(peer_object.getmultibalances()))


############# Testing Initialization #################

adminNode = AdminNode("mambo")
adminNode.create_blockchain()
adminNode.start_admin_blockchain()
#adminNode.stop_admin_blockchain()
#adminNode.start_admin_blockchain()
print("Sleeping 5s")
time.sleep(5)
adminNode.initialize_energy_ecoin_assets()


admin_object = adminNode.get_admin_object()
# list of PeerNodes
peer_nodes_list = []
for x in range(10):
	print("***************creating peer node %d**************", x)
	peer_nodes_list.append(PeerNode(admin_object, "mambo","prosumer", x))
	peer_nodes_list[x].create_peer_blockchain()
	peer_nodes_list[x].start_peer_node()
	print("****************sleeping 3s********************")
	time.sleep(5)




			
