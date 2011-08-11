from urlparse import urlparse, urlunparse
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from helpers import UrlHelper

__u = UrlHelper()
__filtered_tags = set(['document', 'html', 'head', 'body'])

def process(response):
    url = urlparse(response.geturl())
    dom = BeautifulSoup(response)
    _process_links(url, dom)
    _process_scripts(dom)
    _process_ids(dom)
    contents = dom.renderContents()
    #Useful for debugging
    #contents = dom.prettify()
    return contents


def _process_ids(dom):
    existing_ids = set()
    all_tags = dom.findAll(True)
    for tag in all_tags:
        _process_id(tag, existing_ids)

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _process_id(tag, existing_ids):
    if tag.name not in __filtered_tags:
        _generate_id(tag, existing_ids)


def _generate_id(tag, existing_ids):
    id = tag.get('id', None)
    if not id:
        parent = tag.parent
        id_builder = [tag.name]
        while parent.name not in __filtered_tags:
            id_builder.append(parent.name)
            parent = parent.parent
        id_builder.reverse()
        id = '-'.join(id_builder)
    while id in existing_ids:
        id = _increase_id(id)
    tag['id'] = id
    existing_ids.add(id)


def _increase_id(id):
    try:
        idx = id.rindex('_')
    except ValueError:
        return id + '_1'

    num = id[idx+1:]
    if not _is_int(num):
        return id + '_1'
    else:
        stripped = id[:idx]
        return stripped + '_' + str(int(num)+1)


def _process_scripts(dom):
    for script_tag in dom('script'):
        script_tag.extract()

    body = dom.html.body

    script = Tag(dom, 'script')
    script['type'] = 'text/javascript'
    handler = NavigableString('parent.uMon.iFrameLoaded();')
    script.append(handler)
    body.append(script)


def _process_links(request_url, dom):
    for link in dom('link'):
        type = link.get('type', 'text/css')
        if type == 'text/css':
            href = link.get('href', None) 
            if href:
                link['href'] = _process_link(href, request_url)
        else:
            link.extract()

    for a in dom('a'):
        href = a.get('href', None)
        if href:
            a['href'] = _process_link(href, request_url)


    for img in dom('img'):
        src = img.get('src', None)
        if src:
            img['src'] = _process_link(src, request_url)


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
