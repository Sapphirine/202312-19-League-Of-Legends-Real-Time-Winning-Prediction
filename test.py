import urllib.request
import ssl
import json

def get_live_data():
    url = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    scontext.verify_mode = ssl.VerifyMode.CERT_NONE
    with urllib.request.urlopen(url = url, context=scontext) as f:
        return json.loads(f.read().decode('utf-8'))
    

# Using the function to fetch data
game_data = get_live_data()

# Export the game data to a file
if game_data:
    with open("test.json", "w") as file:
        json.dump(game_data, file, indent=4)
    print("Data exported to test.json")
else:
    print("No data available or game is not running.")
