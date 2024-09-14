import requests

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



