import pycurl
from urllib.parse import urlparse
from io import BytesIO

def get_pycurl(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36")
    c.setopt(c.HEADERFUNCTION, header_function)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.FAILONERROR, True)
    c.perform()
    c.close()
    return buffer.getvalue()


content_type = False
charset = ''
def header_function(header_line):
    global charset
    global content_type
    if content_type:
        return

    header_line = header_line.decode('iso-8859-1')

    if ':' not in header_line:
        return

    name, value = header_line.split(':', 1)
    name = name.strip().lower()

    if name == 'content-type':
        content_type = True
        value = value.lower()
        #print(value)
        if ';' not in value:
            if value.strip() != 'text/html':
                print("Not html!")
                return False
        else:
            ct, cs = value.split(';', 1)
            if ct.strip() != 'text/html':
                print("Not html!")
                return False
            cs = cs.strip()
            cs_name, cs_value = cs.split('=', 1)
            if cs_name == 'charset':
                charset = cs_value.strip()

class ArticleDownloadState(object):
    NOT_STARTED = 0
    FAILED = 1
    SUCCESS = 2

class Article(object):

    def __init__(self, url):
        self.url = url
        self.html = None
        self.download_state = ArticleDownloadState.NOT_STARTED


    def download(self):

        try:
            #print(self.url)
            response = get_pycurl(self.url)
            if charset != '':
                self.html = response.decode(charset)
            else:
                self.html = response.decode('utf-8')
            self.download_state = ArticleDownloadState.SUCCESS
            return True
        except Exception as e:
            self.download_state = ArticleDownloadState.FAILED
            if e.args[0] == 28:
                print("Timed Out ->" + self.url)
            #print(e)
            return False

if __name__ == '__main__':
    article = Article("https://vrgamecritic.com")
    article.download()
    print(article.html)
