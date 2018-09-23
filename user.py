from database import CursorFromConnectionFromPool


class User:
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.email)

    # save data to database
    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                "INSERT INTO users (email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s)",
                (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))

    # Load data from database
    @classmethod
    def load_from_db_by_email(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
            user_data = cursor.fetchone()
            return cls(email=user_data[1],
                       first_name=user_data[2],
                       last_name=user_data[3],
                       oauth_token=user_data[4],
                       oauth_token_secret=user_data[5],
                       id=user_data[0])
