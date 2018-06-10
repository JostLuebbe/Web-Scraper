import requests as re
from bs4 import BeautifulSoup as bs
from requests.exceptions import RequestException
from contextlib import closing


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(re.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

class SessionGoogle:
    def __init__(self, url_login, url_auth, login, pwd):
        self.ses = re.session()
        login_html = self.ses.get(url_login)
        soup_login = bs(login_html.content, 'html.parser').find('form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        # override the inputs without login and pwd:
        my_dict['Email'] = login
        my_dict['Passwd'] = pwd
        self.ses.post(url_auth, data=my_dict)

    def get(self, URL):
        return self.ses.get(URL).text


if __name__ == '__main__':
    url_login = "https://accounts.google.com/ServiceLogin"
    url_auth = "https://accounts.google.com/ServiceLoginAuth"
    #s = SessionGoogle(url_login, url_auth, 'jostluebbe@gmail.com', 'Tfh4H1D1E2M+1W!')
    #print(s.get("https://careers.google.com'"))
    with re.session() as s:
        login_html = s.get(url_login)
        soup_login = bs(login_html.content, 'html.parser').find('form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        # override the inputs without login and pwd:
        my_dict['Email'] = 'jostluebbe@gmail.com'
        my_dict['Passwd'] = 'Tfh4H1D1E2M+1W!'
        s.post(url_auth, data=my_dict)

        print(s.get("https://careers.google.com'"))

    # raw_html = simple_get('https://careers.google.com')
    # print(len(raw_html))
    #
    # html = bs(raw_html, 'html.parser')
    #
    # print(html.prettify())

    # no_html = simple_get('https://realpython.com/blog/nope-not-gonna-find-it')
    # print(no_html is None)
    #
    # raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
    # html = bs(raw_html, 'html.parser')
    # for i, li in enumerate(html.select('li')):
    #     print(i, li.text)