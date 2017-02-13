import re


class VerificationText:
    def __init__(self):
        pass

    def email_verification(self, email):
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match is None:
            return False
        else:
            return True

    def html_remove(self, text):
        text = re.sub('<[^>]*>', '', text)
        return text
