import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from DataLayer.admin import Admin
from DataLayer.volunteer import Volunteer
from util import *

class AuthenticationService:

    @staticmethod
    def redirect_url(self, user):
        # user = UserDataAccess.get_user(username, password)
        if user.is_admin:
            return "admin_main_page"
        else:
            return "volunteer_main_page"
        
        