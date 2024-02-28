import requests

class ApiWrapper:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, username, password, discord_id=None):
        url = f"{self.base_url}/create_user"
        data = {'username': username, 'password': password, 'discord_id': discord_id}
        response = requests.post(url, data=data)
        return response.text

    def send(self, recipient_id, token_id, amount):
        url = f"{self.base_url}/send"
        data = {'recipient_id': recipient_id, 'token_id': token_id, 'amount': amount}
        response = requests.post(url, data=data)
        
        if response.status_code == 404:
            return "Recipient doesn't exist", 404
        else:
            return response.text

# Example usage:
api_wrapper = ApiWrapper(base_url="http://127.0.0.1:5000")
create_user_response = api_wrapper.create_user(username="testuser", password="Amogus", discord_id="190")
print(create_user_response)

#send_response = api_wrapper.send(recipient_id="123", token_id="456", amount="100")
#print(send_response)
