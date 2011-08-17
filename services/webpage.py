from services.storage import StorageService
from models.webpage import Webpage
from datetime import datetime
from util import normalize_url


contents = '''<html><head><title>Stuart Frankel's very small web site</title><meta name="verify-v1" content="1vLCRPR1SHmiCICnhWfD7jtpOOSHe79iILqzDkGBUg0="></head><body style="color: rgb(0, 0, 0); background-color: rgb(245, 204, 176); background-image: url(http://dustyfeet.com/images/gecback2.jpg);" alink="#db70db" link="red" vlink="#2f2f4f">
<br class=" selectable-element" id="br" title="CSS Selector: #br"><center class=" selectable-element" id="center" title="CSS Selector: #center">
<table border="8" class=" selectable-element" id="center-table" title="CSS Selector: #center-table"><tbody class=" selectable-element" id="center-table-tbody" title="CSS Selector: #center-table-tbody"><tr class=" selectable-element" id="center-table-tbody-tr" title="CSS Selector: #center-table-tbody-tr"><td bgcolor="#f5ccb0" class=" selectable-element" id="center-table-tbody-tr-td" title="CSS Selector: #center-table-tbody-tr-td">
      <h1 class=" selectable-element" id="center-table-tbody-tr-td-h1" title="CSS Selector: #center-table-tbody-tr-td-h1">My Small-But-Intense Home Page!</h1>
      </td>
    </tr></tbody></table></center>
<br class=" selectable-element" id="br_1" title="CSS Selector: #br_1"><br class=" selectable-element" id="br_2" title="CSS Selector: #br_2"><center class=" selectable-element" id="center_1" title="CSS Selector: #center_1">
<font size="5" class=" selectable-element" id="center-font" title="CSS Selector: #center-font"> elcome to my Small-But-Intense Home Page! There's not
much here yet, but at least I'm avoiding those obnoxious <a href="#" target="_top" class=" selectable-element" id="center-font-a" title="CSS Selector: #center-font-a">under construction</a> tags, so if
there's a
visible link it should give you something. </font></center>
<center class=" selectable-element" id="center_2" title="CSS Selector: #center_2">
<p class=" selectable-element" id="center-p" title="CSS Selector: #center-p"></p>
<font size="4" class=" selectable-element" id="center-font_1" title="CSS Selector: #center-font_1">24 August 2006. About The Barney Affair: This is my
little corner of the web, and the bullies can't have it. There's
nothing more to it than that. There's a NYTimes article about it <a href="#" class=" selectable-element" id="center-font-a_1" title="CSS Selector: #center-font-a_1">here</a>.<br class=" selectable-element" id="center-font-br" title="CSS Selector: #center-font-br"></font></center>
<center class=" selectable-element" id="center_3" title="CSS Selector: #center_3">
<table cellpadding="12" cellspacing="12" width="85%" class=" selectable-element" id="center-table_1" title="CSS Selector: #center-table_1"><!--<tr><td valign=top><font size="5"><a href="rescent.html">Upgrades</a></font></td></tr>--><tbody class=" selectable-element" id="center-table-tbody_1" title="CSS Selector: #center-table-tbody_1"><tr class=" selectable-element" id="center-table-tbody-tr_1" title="CSS Selector: #center-table-tbody-tr_1"><td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_1" title="CSS Selector: #center-table-tbody-tr-td_1"> <font size="5" class=" selectable-element" id="center-table-tbody-tr-td-font" title="CSS Selector: #center-table-tbody-tr-td-font"><a href="#" target="_top" class=" selectable-element" id="center-table-tbody-tr-td-font-a" title="CSS Selector: #center-table-tbody-tr-td-font-a">Dissertation</a></font></td>
      <td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_2" title="CSS Selector: #center-table-tbody-tr-td_2"> <font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_1" title="CSS Selector: #center-table-tbody-tr-td-font_1">The whole thing is here for
downloading; also the
abstract for reading online, if you're in a hurry. I'm accepting bids
for the movie rights.</font></td>
    </tr><tr class=" selectable-element" id="center-table-tbody-tr_2" title="CSS Selector: #center-table-tbody-tr_2"><td halign="right" valign="top" class=" selectable-element" id="center-table-tbody-tr-td_3" title="CSS Selector: #center-table-tbody-tr-td_3"><font size="5" class=" selectable-element" id="center-table-tbody-tr-td-font_2" title="CSS Selector: #center-table-tbody-tr-td-font_2"><a href="#" class=" selectable-element" id="center-table-tbody-tr-td-font-a_1" title="CSS Selector: #center-table-tbody-tr-td-font-a_1"> How to build a clavichord</a></font><br class=" selectable-element" id="center-table-tbody-tr-td-br" title="CSS Selector: #center-table-tbody-tr-td-br"><font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_3" title="CSS Selector: #center-table-tbody-tr-td-font_3"> &#160;&#160;&#160;&#160;&#160;&#160; </font></td>
      <td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_4" title="CSS Selector: #center-table-tbody-tr-td_4"><font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_4" title="CSS Selector: #center-table-tbody-tr-td-font_4">The story of my clavichord, made
by Owen Daly, after an 18th-century Portuguese model.</font></td>
    </tr><tr class=" selectable-element" id="center-table-tbody-tr_3" title="CSS Selector: #center-table-tbody-tr_3"><td halign="right" valign="top" class=" selectable-element" id="center-table-tbody-tr-td_5" title="CSS Selector: #center-table-tbody-tr-td_5"><font size="5" class=" selectable-element" id="center-table-tbody-tr-td-font_5" title="CSS Selector: #center-table-tbody-tr-td-font_5"><a href="#" class=" selectable-element" id="center-table-tbody-tr-td-font-a_2" title="CSS Selector: #center-table-tbody-tr-td-font-a_2">Evil</a></font></td>
      <td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_6" title="CSS Selector: #center-table-tbody-tr-td_6"><font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_6" title="CSS Selector: #center-table-tbody-tr-td-font_6">Bad odor</font></td>
    </tr><tr class=" selectable-element" id="center-table-tbody-tr_4" title="CSS Selector: #center-table-tbody-tr_4"><td halign="right" valign="top" class=" selectable-element" id="center-table-tbody-tr-td_7" title="CSS Selector: #center-table-tbody-tr-td_7"><font size="5" class=" selectable-element" id="center-table-tbody-tr-td-font_7" title="CSS Selector: #center-table-tbody-tr-td-font_7"><a href="#" class=" selectable-element" id="center-table-tbody-tr-td-font-a_3" title="CSS Selector: #center-table-tbody-tr-td-font-a_3">Warung Seniman</a> </font></td>
      <td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_8" title="CSS Selector: #center-table-tbody-tr-td_8"><font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_8" title="CSS Selector: #center-table-tbody-tr-td-font_8">Javanese recipes by a Javanese
musician. Recipes by Wakidi Dwijamartono; text by K. Emerson.</font></td>
    </tr><tr class=" selectable-element" id="center-table-tbody-tr_5" title="CSS Selector: #center-table-tbody-tr_5"><td halign="right" valign="top" class=" selectable-element" id="center-table-tbody-tr-td_9" title="CSS Selector: #center-table-tbody-tr-td_9"><font size="5" class=" selectable-element" id="center-table-tbody-tr-td-font_9" title="CSS Selector: #center-table-tbody-tr-td-font_9"><a href="#" class=" selectable-element" id="center-table-tbody-tr-td-font-a_4" title="CSS Selector: #center-table-tbody-tr-td-font-a_4">Spanish organ</a> </font></td>
      <td valign="top" class=" selectable-element" id="center-table-tbody-tr-td_10" title="CSS Selector: #center-table-tbody-tr-td_10"><font size="4" class=" selectable-element" id="center-table-tbody-tr-td-font_10" title="CSS Selector: #center-table-tbody-tr-td-font_10">Some practical information about
registration in Spanish Baroque Organ music.</font></td>
    </tr></tbody></table><br class=" selectable-element" id="center-br" title="CSS Selector: #center-br"><br class=" selectable-element" id="center-br_1" title="CSS Selector: #center-br_1"><a href="#" class=" selectable-element" id="center-a" title="CSS Selector: #center-a">e-mail me if you want</a></center>
<br class=" selectable-element" id="br_3" title="CSS Selector: #br_3"><br class=" selectable-element" id="br_4" title="CSS Selector: #br_4"><script type="text/javascript" class=" selectable-element" id="script" title="CSS Selector: #script">parent.uMon.iFrameLoaded();</script></body></html>'''

class WebpageService(StorageService):


    @classmethod
    def stub_data(cls):
        now = datetime.now()

        cls.insert(Webpage(
            'http://dustyfeet.com',
            contents,
            now))


    @classmethod
    def get_by_url(cls, url):
        url = normalize_url(url)
        lis = list(p for p in cls.get_all() if p.url == url)
        l = len(lis)
        assert l in [0, 1],\
                'More than one URL in the webpage storage service'
        if l == 1:
            return lis[0]
        return None




