#this is my main entity agent file
import os
import getpass
from dotenv import load_dotenv



#helper function to set enviroment variables
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

#load the enviroment variable
load_dotenv()
_set_env("GOOGLE_API_KEY")


