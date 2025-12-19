#funktioner
#GET request och returnerar det i JSON
import requests
def get_url(url):
    try:
        response = requests.get(url, timeout=5) #skickar till url
        response.raise_for_status()
        return response.json() #här tolkas svaret i JSON-format
    except requests.exceptions.RequestException as e:
        print("Något gick fel vid GET-request: ", e)
        return None
    except ValueError:
        print("Svaret kunde ej tolkas i JSON!")
        return None

#Funktion för POST-request med headers och returnerar i JSON
def post_url(url, headers=None, data=None):
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Något gick fel vid POST-request", e)
        return None
    except ValueError:
        print("Svaret kunde ej tolkas i JSON!")
        return None
    
#grund-url för API
api_bas = "http://10.3.10.104:3000"


#PROGRAM

api_tokenresponse = post_url(api_bas + "/api/token") #anropar en token
if api_tokenresponse is None: #Meddelar användaren om att det inte hämtats någon token och avslutar programmet
    print("Token ej tillgänglig.") 
    exit()

token_value = api_tokenresponse["token"] #tar ut tokensträngen
if token_value is None:
    print("Token saknas.")
    exit()

print("Token:", token_value) #printar token

#skapar header med auth
headers = {"Authorization": f"Bearer {token_value}"}

token_verify = post_url(api_bas + "/api/verify",headers=headers) #post till verify
if token_verify is None: #kontrollerar ifall vi fått det vi efterfrågat, meddelar och avslutar vid fel.
    print("Misslyckad verifiering")
    exit()

print("Verifieringssvar: ", token_verify) #kontrollsvar

secretvalue = token_verify["secret"]
claim = token_verify["claimWithinMs"]
if secretvalue is None or claim is None:
    print("Nödvändig data saknas.")
    exit()

flagga = {"token": token_value, "secret": secretvalue}

flaggsvar = post_url(api_bas + "/api/flag", headers=headers, data=flagga)
if flaggsvar is None: #kontrollerar ifall vi fått det vi efterfrågat, meddelar och avslutar vid fel.
    print("Ingen flagga identifierad, avlutar program.")
    exit()

print("Flag response", flaggsvar) 