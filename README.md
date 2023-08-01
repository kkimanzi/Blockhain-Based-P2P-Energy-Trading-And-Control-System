# Blockhain-Based-P2P-Energy-Trading-And-Control-System
## Objectives
- To propose a blockchain-enabled P2P market model of generated PV energy.
- To propose a dual power source controller for switching power between the internal SHS battery and external grid connection.

## Design
**Information Flow**
	![transaction-flow-1](https://github.com/kkimanzi/Blockhain-Based-P2P-Energy-Trading-And-Control-System/assets/62201012/f8ce34ec-0fa5-4505-9887-f9a40f933e91)
 ![transaction-flow-2](https://github.com/kkimanzi/Blockhain-Based-P2P-Energy-Trading-And-Control-System/assets/62201012/152d97d3-1ddd-4583-860e-3f06d86e0625)

**Prosumer Control System Block Diagram**
![image](https://github.com/kkimanzi/Blockhain-Based-P2P-Energy-Trading-And-Control-System/assets/62201012/dbc5c51a-640c-41ad-b2e0-a950b25e24ad)

## Results
Refer to the report at the root of this repository.

## "/codes" Direcory Structure
1. /savoir - 
2. get-pip.py - installer for pip
3. **initilize_assets.sh** - script to intialize econ & energy assets. Ecoin asset buys energy asset.
4. **initialize_blockchain.sh** - shell file for interacting with the blockhain using CLI commands.
5. **initialize_blockchain.py** - user-friendly wrapper of **initialize_blockchain.sh** to allow automation and testing
   
