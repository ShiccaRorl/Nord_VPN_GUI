import requests

def get_nordvpn_servers():
    url = "https://api.nordvpn.com/v1/servers/recommendations"
    response = requests.get(url)
    
    if response.status_code == 200:
        servers = response.json()
        for server in servers:
            print(f"Name: {server['name']}, Country: {server['country']}, Load: {server['load']}%")
    else:
        print(f"Failed to retrieve servers. Status code: {response.status_code}")

if __name__ == "__main__":
    get_nordvpn_servers()
