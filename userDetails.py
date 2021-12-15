class UserDetails:

    def __init__(self,username):
        self.user = username

    def username(self):
        if self.user.empty():
            return "user"
        else:
            return self.user


