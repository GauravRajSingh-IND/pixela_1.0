import requests

"""
{'username': 'dyodhi', 'token': 'grsmanohar', 
'response': {'message': "Success. Let's visit https://pixe.la/@dyodhi , it is your profile page!", 
'isSuccess': True}}
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

        def delete_account(self, username:str, token:str) -> dict:
            """
            This function let user delete there account by providing a valid username and token/password.
            :param username: username of the account which user wants to delete.
            :param token: token/password of the account which user wants to delete.
            :return: dictionary which have information about if the user account is deleted or not.
            """

            self.username_text = username
            self.password_text = token

            url = f"{Pixela().end_point}/v1/users/{self.username_text}"

            headers = {
                "X-USER-TOKEN":self.password_text
            }

            # request to delete the user account.
            try:
                response = requests.delete(url=url, headers=headers)
                response.raise_for_status()
                return {"username":self.username_text, "response":response.json()}
            except requests.RequestException as e:
                return {"error": e}

        def view_user_profile(self, username:str) -> dict:
            """
            This function will give html data of the user.
            :param username: username
            :return: dict object
            """

            self.username_text = username

            url = f"{Pixela().end_point}/@{self.username_text}"

            try:
                response =  requests.get(url)
                response.raise_for_status()
                return {"status":True, "response":response.text}

            except requests.RequestException as e:
                return {"status":False, "response":f"Error while fetching user profile: {e}"}

        def update_user_profile(self, username:str, token:str, displayName:str = None, gravatarIconEmail:str = None,
                                title:str = None, timezone:str = None, aboutURL:str = None, contributeURLs:str = None,
                                pinnedGraphID:str = None) -> dict:

            """
            This function update the information provided by the user.
            :param username: username of profile where update is required.
            :param token: token ID of the profile.
            :param displayName: The user's name for the display
            :param gravatarIconEmail:  This is the email address registered as an icon in Gravatar.
            :param title: The title of the user.
            :param timezone: Specify the user's time zone as TZ database name (not Time zone abbreviation).
            :param aboutURL: Users can only show one external link to this profile page.
            :param contributeURLs: It corresponds to 6 in the image above.
            :param pinnedGraphID: Users can pin one of their own graphs to their profile page.
            :return: dict object of status and response.
            """

            if not all([username, token]):
                raise "required values are missing, Please provide username and token"

            self.username_text = username
            self.password_text = token

            url = f"{Pixela().end_point}/@{self.username_text}"

            headers = {
                "X-USER-TOKEN":token
            }

            params_keys = ['displayName', 'gravatarIconEmail', 'title', 'timezone', 'aboutURL', 'contributeURLs', 'pinnedGraphID']
            params_values= [displayName, gravatarIconEmail, title, timezone, aboutURL, contributeURLs, pinnedGraphID]

            params = {}
            for num in range(len(params_keys)):

                if params_values[num]  is not None:
                    key = params_keys[num]

                    # add params key and value to params dict.
                    params[key] = params_values[num]

            try:
                response = requests.put(url=url, json=params, headers=headers)
                response.raise_for_status()
                return {"status": True, "response": response.json()}
            except requests.RequestException as e:
                return {"status": False, "response": e}

