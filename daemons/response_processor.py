from urlparse import urlparse, urlunparse
from BeautifulSoup import BeautifulSoup

def process(response):
    url = urlparse(response.geturl())
    dom = BeautifulSoup(response)
    _process_links(url, dom)
    contents = dom.renderContents()
    return contents


def _process_links(request_url, dom):
    for link in dom('link'):
        if link.get('type', 'text/css') == 'text/css':
            link['href'] = _process_link(link['href'], request_url)
        else:
            link.extract()
        
    for a in dom('a'):
        a['href'] = _process_link(a['href'], request_url)
      
    for img in dom('img'):
        img['src'] = _process_link(img['src'], request_url)


def _process_link(link_src, request_url):
    current_path = request_url.path
    url = urlparse(link_src)
    if not url.netloc:
        url = list(url)
        url[0] = request_url.scheme
        url[1] = request_url.netloc
        if not link_src.startswith('/'):
            url[2] = current_path + url[2]

    return urlunparse(url)
