import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'https://m.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100'

def get_login_payload(session, user_email, user_password):
    """Retrieves hidden input fields from the login page to construct the login payload."""

    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, 'html.parser')

    hidden_fields = {
        'lsd': soup.find('input', {'name': 'lsd'})['value'],
        'jazoest': soup.find('input', {'name': 'jazoest'})['value'],
        'm_ts': soup.find('input', {'name': 'm_ts'})['value'],
        'li': soup.find('input', {'name': 'li'})['value']
    }

    login_payload = {
        **hidden_fields,  # Combine hidden fields with other login data
        "try_number": "0",
        "unrecognized_tries": "0",
        'email': user_email,
        'pass': user_password,
        "login": "Log in",
        "bi_xrwh": "0",
        "_fb_noscript": "true"
    }

    return login_payload

user_email = input("Enter your Email: ")
user_password = input("Enter your Pasword: ")

with requests.Session() as session:
    login_payload = get_login_payload(session, user_email, user_password)
    login_response = session.post(LOGIN_URL, data=login_payload)

    print(login_response.reason)
    print(login_response.status_code)

    home_page = session.get('https://m.facebook.com')
    home_soup = BeautifulSoup(home_page.text, 'html.parser')
    profile_url = home_soup.select_one("#header > div > a.bh.bf.bg")['href']
    print(profile_url)
