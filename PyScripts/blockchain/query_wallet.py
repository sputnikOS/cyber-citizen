from moralis import evm_api

api_key = ""
params = {
    "address": "0x408D21640EdDd84DeA390bd05342b6c163eE0Aa8",
    "chain": "eth",
}

result = evm_api.token.get_wallet_token_balances(
    api_key=api_key,
    params=params,
)

print(result)