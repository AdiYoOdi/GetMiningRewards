# GetMiningRewards

This repository is for https://straypet.org/ , https://t.me/STRAYpet ,
STRAY Pet is a crypto-based project aimed to help no-kill shelters around the world by donating funds needed to feed, treat, spay/neuter, and house homeless cats and dogs. Our second goal is to promote adoption of cats and dogs from shelters instead of buying pets at the stores or from breeders


-------------------------------------

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
	    
Just tought about the transactions in/out of the wallet , those also need to be filtered. Maybe filter first all the transactions that have output[0] as value zero , it seems all mined blocks have that 
