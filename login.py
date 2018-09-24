from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

# Initialise database
Database.initialise(user='postgres', password='16redroses', host='localhost', database='learning')

user_email = input("Enter your email address: ")

user = User.load_from_db_by_email(user_email)

# If user does not exists in the database
if not user:
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first_name = input("Enter your first name? ")
    last_name = input("Enter your last name? ")

    # creating User object to save into the database
    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'],
                None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])
