#!/bin/bash
#generate energy asset
#$1 is positional parameter for chain name
#$2 is positional parameter for address


multichain-cli $1 issuefrom $2 $2 '{"name":"energy","open":true}' 0 0.001 0 '{"form":"KW", "stage":"0", "purpose":"excess generation"}'

#generate ecoin asset
multichain-cli $1 issuefrom $2 $2 '{"name":"ecoin","open":true}' 0 1 0 '{"form":"BDT", "stage":"0", "purpose":"ecoin sale"}'
