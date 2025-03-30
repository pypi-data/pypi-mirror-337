""" Creating batch payloads 

    Evrmail uses batchable, encrypted IPFS payloads. 
    Each individual message payload will be in a batch payload.

    Batch payload:
    {
        "batch_id": str,            # Optional: UUID or hash
        "created": str,             # ISO 8601 UTC timestamp
        "sender": str,              # Sender's address
        "sender_pubkey": str,       # Cached sender pubkey (for audit)
        "version": 1,               # For protocol upgrades
        "messages": [               # Array of individual encrypted messages
            {message_payload},      # An individual message payload
            {message_payload}
            ...
        ]
    }

    Individual message payload:
    {
        'to': str                   # The address this payload is for
        'from': str,                # The address this payload is from
        'to_pubkey': str,           # The pubkey this payload is for 
        'from_pubkey': str,         # The pubkey this payload is from
        'ephemeral_pubkey': str,    # The ephemeral pubkey of the payload
        'nonce': str,               # The hex string nonce of the payload
        'ciphertext': str,          # The encrypted payload message 
        'signature': str            # The senders signature of the message    
    }

"""
import json
import os
import subprocess
import time
from pathlib import Path
from evrmore_rpc import EvrmoreClient
from evrmore_rpc.zmq import EvrmoreZMQClient, ZMQTopic
from evrmail.config import load_config
from evrmail.utils.scan_payload import scan_payload
from evrmail.utils.inbox import save_messages
from evrmail.utils.ipfs import fetch_ipfs_json
from evrmail.utils.decrypt_message import decrypt_message
from evrmail.utils.wif_to_privkey_hex import wif_to_privkey_hex

config = load_config()
known_addresses = config.get("addresses", {})

STORAGE_DIR = Path.home() / ".evrmail"
INBOX_FILE = STORAGE_DIR / "inbox.json"
PROCESSED_TXIDS_FILE = STORAGE_DIR / "processed_txids.json"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def load_processed_txids():
    if PROCESSED_TXIDS_FILE.exists():
        return json.loads(PROCESSED_TXIDS_FILE.read_text())
    return []

def save_processed_txids(txids):
    PROCESSED_TXIDS_FILE.write_text(json.dumps(txids, indent=2))

def main():
    print("📡 evrmail Daemon Starting...")
    rpc = EvrmoreClient()
    zmq = EvrmoreZMQClient()

    @zmq.on(ZMQTopic.TX)
    def on_transaction(notification):

        # Get transaction id
        txid = notification.tx.get("txid")

        # Cache the txid
        processed_txids = load_processed_txids()
        if txid in processed_txids:
            return
        processed_txids.append(txid)
        save_processed_txids(processed_txids)


        for vout in notification.tx.get("vout", []):
            script = vout.get("scriptPubKey", {})
            if script.get("type") == "transfer_asset":
                asset = script.get("asset", {})
                cid = asset.get("message")
                if cid:
                    print(f"📥 New message CID detected: {cid}")
                    messages = scan_payload(cid)
                    save_messages(messages)

    zmq.start()
    print("✅ Daemon is now listening for messages.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Stopping evrmail Daemon...")
    finally:
        zmq.stop_sync()
        rpc.close_sync()

if __name__ == "__main__":
    main()