from urlparse import urlparse, urlunparse
from lxml import etree, html
from lxml.html import builder as E
from udammit import UnicodeDammit


__filtered_tags = set(['html', 'head', 'body'])
__parser = etree.HTMLParser(recover=True)

def process(response):
    url = urlparse(response.geturl())
    dammit = UnicodeDammit(response.read(), isHTML=True)
    dom = html.fromstring(dammit.unicode, base_url=url.geturl())

    _process_links(url, dom)
    _process_scripts(dom)
    _process_ids(dom)
    return etree.tostring(dom, method="html")


def _process_scripts(dom):
    script_tags = dom.cssselect('script')
    for script_tag in script_tags:
        script_tag.getparent().remove(script_tag)

    for el in dom.cssselect('*'):
        for ev in ('onload', 'onunload', 'onclick', 'onfocus', 'onblur'\
                'onchange', 'onsubmit', 'onmouseover', 'onerror'):
            if ev in el.attrib:
                del el.attrib[ev]

    script = E.SCRIPT('parent.uMon.iFrameLoaded();',type='text/javascript')
    body = dom.cssselect('body')[0]
    body.append(script)


def _process_links(request_url, dom):
    dom.make_links_absolute(request_url.geturl())

    for a in dom.cssselect('a'):
        a.attrib['href'] = '#'
    for f in dom.cssselect('form'):
        f.attrib['action'] = '#'
    for b in dom.cssselect('button[type="submit"], input[type="submit"]'):
        b.attrib['disabled'] = 'disabled'


def _process_ids(dom):
    existing_ids = set()
    all_tags = dom.cssselect('*')
    for tag in all_tags:
        _process_id(tag, existing_ids)


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _process_id(tag, existing_ids):
    if tag.tag not in __filtered_tags:
        _generate_id(tag, existing_ids)


def _generate_id(tag, existing_ids):
    id = tag.attrib.get('id', None)
    if not id:
        parent = tag.getparent()
        id_builder = [tag.tag]
        while parent.tag not in __filtered_tags:
            id_builder.append(parent.tag)
            parent = parent.getparent()
        id_builder.reverse()
        id = '-'.join(id_builder)
    while id in existing_ids:
        id = _increase_id(id)
    tag.attrib['id'] = id
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
