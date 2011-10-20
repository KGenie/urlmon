import urllib2, datetime, logging
from traceback import format_exc
from controllable import ControllableDaemon
from models.webpage_version import WebpageVersion
from urlparse import urlparse, urlunparse
from lxml import etree, html
from lxml.html.clean import Cleaner
from util import normalize_url, is_int
from helpers import UrlHelper

u = UrlHelper()
__logger = logging.getLogger('daemons.controllable.webpage')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

class WebpageDaemon(ControllableDaemon):

    def __init__(self):
        ControllableDaemon.__init__(self)
       

    def process_message(self, message):
        debug('Preparing to make a web request')
        ret = None
        try:
            ret = self.__fetch(*message)
        except Exception as e:
            error('Error ocurred while fetching web page: %s', format_exc(e))
        else:
            debug('Webpage successfully fetched and stored')
        return ret



    def __fetch(self, url, current_selector):
        request = urllib2.Request(normalize_url(url))
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0')
        debug('Making request to %s...' % url)
        response = urllib2.urlopen(request)
        debug('Response obtained, processing the page for storage')
        body_dom = get_processed_dom(response)
        if current_selector:
            body_dom = select_content(body_dom, current_selector)
        body = etree.tostring(body_dom, method='html', pretty_print=True)

        page = WebpageVersion(url, body, datetime.datetime.now())
        return page


    def fetch(self, url, current_selector=None):
        return self.send((url, current_selector), get_response=True)

           

DAEMON = WebpageDaemon()




# Page processing code

def highlight_selected(body_dom, current_selector):
    if current_selector != 'body':
        body_dom.head.append(html.fromstring(
        '''<link rel="stylesheet" href="../static/css/frame.css"
        type="text/css" />''')) 



def select_content(body_dom, current_selector):
    if current_selector != 'body':
        for tag in body_dom.cssselect(current_selector):
            classes = tag.attrib.get('class', '')
            classes += ' selected-element'
            tag.attrib['class'] = classes

    return body_dom


__filtered_tags = set(['html', 'head', 'body'])
       

def get_processed_dom(response):
    url = urlparse(response.geturl())
    dom = html.fromstring(response.read(), base_url=url.geturl())
    clean_html(dom)

    _process_links(url, dom)
    _process_scripts(dom)
    _process_selectable_elements(dom)
    _process_ids(dom)

    return dom


def _process_selectable_elements(dom):
    all_tags = dom.cssselect('body *')
    for tag in all_tags:
        classes = tag.attrib.get('class', '')
        classes += ' selectable-element'
        tag.attrib['class'] = classes


def _process_scripts(dom):
    body = dom.body.attrib['onload'] =\
            'parent.uMon.iFrameLoaded();' 


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
    all_tags = dom.cssselect('.selectable-element')
    for tag in all_tags:
        _process_id(tag, existing_ids)


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
    #tag.attrib['title'] = 'CSS Selector: #%s' % id
    existing_ids.add(id)


def _increase_id(id):
    try:
        idx = id.rindex('_')
    except ValueError:
        return id + '_1'

    num = id[idx+1:]
    if not is_int(num):
        return id + '_1'
    else:
        stripped = id[:idx]
        return stripped + '_' + str(int(num)+1)


class UMonCleaner(Cleaner):
    #scripts = True
    javascript = False
    #comments = True
    #style = False
    links = False 
    meta = False
    page_structure = False
    #processing_instructions = True
    #embedded = False
    #frames = True
    forms = False
    #annoying_tags = True
    #remove_tags = None
    #allow_tags = None
    #remove_unknown_tags = True
    #safe_attrs_only = False
    #add_nofollow = False
    #host_whitelist = ()
    #whitelist_tags = set(['iframe', 'embed'])

clean_html = UMonCleaner()
