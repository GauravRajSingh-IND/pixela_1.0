import requests

"""
{'username': 'gauravrajsinghjobner101', 'token': 'grsmanohar007', 
'response': {'message': "Success. Let's visit https://pixe.la/@gauravrajsinghjobner101 , 
it is your profile page!", 'isSuccess': True}}
"""

class Pixela:

    def __init__(self):

        self.end_point = "https://pixe.la"
        self.USER = self.User()

    class User:

        def __init__(self):
            self.username_text = None
            self.password_text = None

        def create_new_user(self, token:str, username:str, agree_terms:str = "yes", not_minor:str= "yes") -> dict:
            """
            This function takes two arguments from the user and create a new account in pixela.
            :param token: this string will be used to authenticate the user, Validation rule: [ -~]{8,128}
            :param username: this string is the username which will be used in any user specific task,
                                Validation rule: [a-z][a-z0-9-]{1,32}
            :param agree_terms: default : yes, specify no if user don't accept the terms and condition.
            :param not_minor: default : yes, specify no if the user is a minor
            :return: dictionary which have all the information if user account is created or
                    information about the error
            """

            url = f"{Pixela().end_point}/v1/users"

            params = {
                "token":token,
                "username":username,
                "agreeTermsOfService":agree_terms,
                "notMinor":not_minor,

            }

            # post request and check the response.
            try:
                response = requests.post(url=url, json=params)
                response.raise_for_status()

                # set username and password.
                self.username_text = username
                self.password_text = token
                return {"username":self.username_text, "token":self.password_text, "response":response.json()}

            except requests.RequestException as e:
                print(f"error while creating the user: {e}")
                return {"error": e}

        def update_user_password(self, username:str, token:str, new_token:str) -> dict:
            """
            this function update the token/password of an existing user.
            :param username: username of the user
            :param token: current token of the user
            :param new_token: new token of the user
            :return: dict object containing information if the password is updated or not.
            """

            # assigning username.
            self.username_text = username
            self.password_text = token

            url = f"{Pixela().end_point}/v1/users/{self.username_text}"

            headers = {
                "X-USER-TOKEN":self.password_text,
            }

            params = {
                "newToken":new_token
            }

            # create a put request to change the user password.
            try:
                response = requests.put(url=url, json=params, headers=headers)
                response.raise_for_status()

                # assign new token to password variable.
                self.password_text = new_token

                return {"username": self.username_text, "token": self.password_text,
                        "response": response.json()}

            except requests.RequestException as e:
                return {"error": e}


