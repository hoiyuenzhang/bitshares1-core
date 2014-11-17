
#   run client:   ./programs/client/bitshares_client --min-delegate-connection-count=0 --httpport=8080 --rpcuser=a --rpcpass=a --server
#   make file:  touch test_iter

import requests
import sys
import json
import time

i = 0
with open("test_iter") as test:
    i = int(test.read())
with open("test_iter", "w") as test:
    test.write(str(i+1))

def req(f, *args):
    url = "http://a:a@localhost:8080/rpc"
    # user: a  pass: a
    headers = {
      'content-type': 'application/json',
      'Authorization': "Basic YTph"
    }

    payload = {
        "method": f,
        "params": [i for i in args],
        "jsonrpc": "2.0",
        "id": 0
    }
    print "Calling " + f
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print response
    if response.json()["result"]:
        print response.json()["result"]
        return response.json()["result"]
    else:
        print "Error?"
        print response.json()


def wait():
    req("wallet_open", "default")
    req("wallet_unlock", 999, "password")
    print("Sleeping 11 sec...")
    time.sleep(11)
    req("wallet_open", "test"+str(i), "password")
    req("wallet_unlock", 999999, "password")


req("wallet_close")
req("wallet_create", "test"+str(i), "password")
req("wallet_account_create", "money")
with open("dev-test-keys.txt") as keys:
    j = 0
    for k in keys:
        j += 1
        if j > i:
            req("wallet_import_private_key", k, "money")
            break
        if j >= 100:
            print "No more keys!"
            sys.exit(1)
req("scan")
req("wallet_account_create", "acct1")
addr1 = req("wallet_address_create", "acct1")
addr2 = req("wallet_address_create", "acct1")
addr3 = req("wallet_address_create", "acct1")
bal_id = req("wallet_multisig_get_balance_id", 2, [addr1, addr2, addr3])
trx_rec = req("wallet_multisig_deposit", "money", 100, "XTS", 2, [addr1, addr2, addr3])

wait()

req("blockchain_get_balance", bal_id)
req("blockchain_list_address_balances", addr1)
addr4 = req("wallet_address_create", "acct1")
trx_rec = req("wallet_multisig_withdraw_start", bal_id, addr4, 33, "XTS")

wait()

res = req("blockchain_list_address_balances", addr4)
assert(len(res) > 0)


req("wallet_account_create", "acct2")
addr5 = req("wallet_address_create", "acct2")
req("wallet_transfer_asset_to_address", 1000, "XTS", "money", addr5)

wait()

res = req("blockchain_list_address_balances", addr5)
