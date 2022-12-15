import requests
import json
import pygsheets
import logging
import pandas as pd
import time

logging.basicConfig(level=logging.INFO)
hydra_decimals = 100000000

def get_hydra_decimal(hydra_value):
    return int(hydra_value)/hydra_decimals

def check_txs(current_transaction):
    # json_response = []
    for i in range(len(current_transaction)):
        endpoint = f"https://explorer.hydrachain.org/api/tx/{current_transaction[i]}" #don't forget [i] for loops
        headers = {'User-Agent': '...', 'referer': 'https://...'}
        response = requests.get(endpoint, headers=headers)
        json_response_loop = json.loads(response.text)
        outputs = json_response_loop["outputs"]

        block_reward = abs(get_hydra_decimal(json_response_loop["fees"]))
            
        if len(outputs) > 3 : # This is a block won by delegator but has other transactions on it , but there are those cases where extra txs are present but the SuperStaker  won so we need to figure out how to identify that case and discard them 
            delegator = json_response_loop["outputs"][2]
            other_tx = json_response_loop["outputs"]
            
            other_values = []
            for values in other_tx:
                v = int(values["value"])
                other_values.append(v)
                    
            check_number = 500000000

            dict_delegator = {"Address":[], "Reward":[], "Fee":[] }
            if other_values[2] > check_number:
                other_values_cut = other_values[2:]
                other_values_total = get_hydra_decimal(sum(other_values_cut))
                delegator_reward = get_hydra_decimal(delegator["value"])
                delegator_address = delegator["address"]
                super_staker_fee = block_reward - other_values_total
                dict_delegator["Address"].append(delegator_address)
                dict_delegator["Reward"].append(delegator_reward)
                dict_delegator["Fee"].append(super_staker_fee)
                # print(delegator_address)
                # print(delegator_reward)
                # print(super_staker_fee)
                # print("output 2")
            
            else:
                correct_address_is_staker = json_response_loop["outputs"][1]
                correct_address = correct_address_is_staker["address"]
                super_staker_fee = block_reward
                dict_delegator["Address"].append(correct_address)
                dict_delegator["Fee"].append(super_staker_fee)
                # print(correct_address)
                # print(super_staker_fee)
                # print("output 1")
            print(dict_delegator)


def get_tx_id():
    wallet_address = "HM6TFbbBvrJ4hcMTFT93R7DBz1FmcUTGAC"
    endpoint = f"https://explorer.hydrachain.org/api/address/{wallet_address}/basic-txs?limit=100000000000000&offset=0"
    headers = {'User-Agent': '...', 'referer': 'https://...'}
    response = requests.get(endpoint, headers=headers)
    json_response = json.loads(response.text)
    tx_transactions = json_response["transactions"]
    # Get data from [{}] type of json : array of objects i think is called:
    tx_ids = []
    for id in tx_transactions:
        tx_id = id["id"]
        tx_ids.append(tx_id)
    return tx_ids

all_txs = get_tx_id()
check_txs(current_transaction=all_txs)

# check_txs(current_transaction="55b2f7fde386f31e76ede065320df742c70ae92f7a09d1e78d79f8a384fda3f1")

""" 
I identified 4 situations for mining blocks transactions  :
    1. Super Staker won the block an easy transaction where there are only 2 results in  outputs:
        https://explorer.hydrachain.org/tx/e2f5c46868cf77b47f5376817a637f85d06baa697f49c8b2f4131be6dc590c4e
            output[0] is always empty 
            output[1] is always your own wallet address but the Hydra near it is not the reward but the utxo used in tx : 
                [outputs][2][value] /= block reward
                block reward = main_json_response["fees"]
    2. Super Staker won the block but there are other transactions , so outputs[2] = superstaker and i check if outputs[3][value] < 5Hydra
        https://explorer.hydrachain.org/tx/55b2f7fde386f31e76ede065320df742c70ae92f7a09d1e78d79f8a384fda3f1
            output[0] is always empty
            output[1] is always your own wallet address
            output[2] is not the delegator in this situation, because the hydra ["value"] = 0.29639692 HYDRA so thats not a reward for staking
                So i filter results with if statments if value <5H is not delegator  and i say SuperSTaker won 
    3. Delegator won the block, only 3 outputs and we check if output[2]< than 5 Hydra :
        https://explorer.hydrachain.org/tx/117e81f24ba7149acea0cd3c159ab0a2202bb0a2d8176c77f81216d0ec17761f
            output[0] is always empty
            output[1] is always your own wallet address
            output[2] is the Delegator
            
    4. Delegator won the block , there are multiple outputs:
        https://explorer.hydrachain.org/tx/34023cc636a3256c5b1a1b3cea60c21d9cac49457c70a559f67116bcc3f14ccf
            output[0] is always empty
            output[1] is always your own wallet address
            output[2] is the Delegator
            output[3 4 5 ] extra fluf we need to discard
    
"""

