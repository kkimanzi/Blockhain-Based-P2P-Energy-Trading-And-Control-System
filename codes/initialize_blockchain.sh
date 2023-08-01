#!/bin/bash
#inputs:
#  $1 is positional parameter for blockchain name
#  $2 is going to be a designation -a or -p (denoting admin or peer node)
#  $3 is going to be the function we want to do on the blockchain
#    funcctions: create, start, stop

echo $*


if [ -a = $2 ]
then
	echo "Inside admin"
	if [ create = $3 ]
	then
		#create blockchain
		print "Creating admin blockchain"
		multichain-util create $1
	elif [ run = $3 ]
	then
		#run the blockchain
		multichaind $1 -daemon
	elif [ stop = $3 ]
	then
		#stop the blockchain
		multichain-cli $1 stop
	else
		#print error message
		echo "Usage..."
	fi
elif [ -p = $2 ]
then
	# usage: initlialize_blockchain [original_blockchain_name] -p [new_blockchain_dir_postfix] **[original_port] [new_node_port] [operation] 
	echo "inside peer"	
	if [ create = $6 ]
	then
		#create blockchain for peer node
		#cd to default home dir		
		cd
		rootname="./.multichain-"
		postfix=$3
		dir_name=$rootname$postfix	
		echo "dir name : $dir_name"	
		mkdir $dir_name
		#TODO: @localhost:6834 fix this to variable
		
		let rpcport=$5-1
		
		stage1_filter="$(multichaind -datadir=$dir_name -port=$5 -rpcport=$rpcport $1@localhost:$4 | grep -o 'grant [^ ,]\+')"
		echo "stage1_flter"		
		echo "$stage1_filter"		
		tokenized_filter=( $stage1_filter )
		echo "token 1"		
		echo ${tokenized_filter[1]}

		#TODO: appends ports to config file	
		#grant this permission to connect,send,receive
		
		multichain-cli $1 grant ${tokenized_filter[1]} connect,send,receive #TODO: fix addr
	elif [ run = $5 ]
	then
		#run the blockchain
		#cd to default home dir	
		cd	
		rootname="./.multichain-"
		postfix=$3
		dir_name=$rootname$postfix
		echo $dir_name
		let rpcport=$4-1
		multichaind -datadir=$dir_name -port=$4 -rpcport=$rpcport $1 -daemon
	
	elif [ stop = $5 ]
	then
		#stop the blockchain
		#cd to default home dir
		cd
		rootname="./.multichain-"
		postfix=$3
		dir_name=$rootname$postfix
		let rpcport=$4-1
		multichain-cli -datadir=$dir_name -port=$4 -rpcport=$rpcport $1 stop
	else
		#print error message
		echo "Usage..."
	fi
else
	#print error message
	echo "Usage...out"
fi


