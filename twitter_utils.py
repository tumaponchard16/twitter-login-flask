import oauth2
import constants

import urlparse

# Create a consumer, which uses CONSUMER_KEY, CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)

    # Use the client to perform request for the request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

    if response.status != 200:
        print("An error occurred getting the request token from twitter!")

    # Get the request token parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))


def get_oauth_verifier(request_token):
    # Ask the user to authorize the app and gives us the pin code
    print("Go to the following website in your browser: ")
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    return input("What is the PIN? ")


def get_access_token(request_token, oauth_verifier):
    # Create token object which contains the request token and the token verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)

    # Ask twitter for an access token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))