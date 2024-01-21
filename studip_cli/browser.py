import requests
import os
from dotenv import load_dotenv
import tempfile
from lxml import html
import base64
import sys

load_dotenv()
base_url = os.getenv("STUDIP_BASEURL")
temp_folder = os.path.join(tempfile.gettempdir(), "STUDIP_CLI")

def get_request(url_extension: str, params={}, headers={}) -> str:
    session = requests.session()
    session.cookies.set("Seminar_Session", read_session())
    for retry in range(3):
        response = session.get(base_url + "jsonapi.php/v1/" + url_extension, params=params, headers=headers)
        match response.headers["Content-Type"].split(";")[0]:
            case "text/html":
                session.cookies.set("Seminar_Session", fix_session())
            case _:
                return response.text
    return "[]"

def download_file(params: dict):
    session = requests.session()
    session.cookies.set("Seminar_Session", read_session())

    for retry in range(3):
        response = session.get(base_url + "sendfile.php", params=params)
        match response.headers["Content-Type"].split(";")[0]:
            case "text/html":
                session.cookies.set("Seminar_Session", fix_session())
            case _:
                with open(params["file_name"], "wb") as f:
                    f.write(response.content)

def post_request(url: str, params: dict, data: dict) -> str:
    return ""

def fix_session() -> str:
    wipe_sessions()
    new_cookie = read_session()
    return new_cookie

def wipe_sessions():
    dirlist = os.listdir(temp_folder)
    for file_name in dirlist:
        file_path = os.path.join(temp_folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            sys.exit("couldnt delete old sessions")

def read_session() -> str:
    dirlist = os.listdir(temp_folder)
    if len(dirlist) > 1:
        wipe_sessions()
        create_session()
        dirlist = os.listdir(temp_folder)
    elif len(dirlist) == 0:
        create_session()
        dirlist = os.listdir(temp_folder)
    session_file = [entry for entry in dirlist if os.path.isfile(os.path.join(temp_folder, entry))][0]
    cookie = ""
    with open(os.path.join(temp_folder, session_file), 'rb') as file:
        encoded_cookie = file.read()

        # Decode the Base64-encoded data
        cookie = base64.b64decode(encoded_cookie).decode("utf-8")
    return cookie

def create_session():

    login_name = os.getenv("STUDIP_LOGINNAME")
    login_secret = os.getenv("STUDIP_LOGINSECRET")

    data = {
        'loginname': login_name,
        'password': login_secret,
        'resolution': "1x1",
        'device_pixel_ratio': '1',
        'Login': '',
    }

    # Gather Base Session Cookies and Security Tokens

    # Create a session object
    session = requests.Session()

    # Gather Cookies
    cookies_response = session.get(base_url)

    # Parse HTML using lxml
    html_tree = html.fromstring(cookies_response.text)

    # Find CSRF token
    csrf_token = html_tree.xpath('//input[@name="security_token"]/@value')[0]
    data["security_token"] = csrf_token

    # Find login token
    login_token = html_tree.xpath('//input[@name="login_ticket"]/@value')[0]

    data["login_ticket"] = login_token

    # perform the login

    login_status = session.post(base_url, data=data).status_code
    if login_status != 200:
        sys.exit("Login unsuccesful")

    cookie = session.cookies["Seminar_Session"]

    # Specify a custom name for the temporary folder
    folder_name = 'STUDIP_CLI'

    # Create a temporary folder with the custom name
    temp_folder = os.path.join(tempfile.gettempdir(), folder_name)
    try:
        os.makedirs(temp_folder, exist_ok=True)
    except:
        sys.exit("Couldnt create tmp dir")
    # create base64 encoded session and timestamp
    session_string = cookie
    session_base64 = base64.b64encode(session_string.encode('utf-8'))

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(prefix="Seminar_Session-",mode='wb+', delete=False, dir=temp_folder) as temp_file:
            # Write to the file
            temp_file.write(session_base64)
    except:
        sys.exit('Couldnt write Session to tmp')
