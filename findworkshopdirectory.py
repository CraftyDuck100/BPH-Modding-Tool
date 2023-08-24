import dotenv, os
dotenv.load_dotenv()
if os.path.exists(("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/"):
    directory = (("/".join((os.path.abspath('./').split('common')[0]).split('\\'))) + "workshop/content/1970580/")
if directory: dotenv.set_key("./.env","WORKSHOP", directory)