#!/usr/bin/env python
"""
htmldiff.py
(C) Ian Bicking <ianb@colorstudy.com>

Finds the differences between two HTML files.  *Not* line-by-line
comparison (more word-by-word).

Command-line usage:
  ./htmldiff.py test1.html test2.html

Better results if you use mxTidy first.  The output is HTML.
"""

from difflib import SequenceMatcher
import re
import logging
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import cgi

def htmlEncode(s, esc=cgi.escape):
    return esc(s, 1)

commentRE = re.compile('<!--.*?-->', re.S)
tagRE = re.compile('<.*?>', re.S)
headRE = re.compile('<\s*head\s*>', re.S | re.I)


__logger = logging.getLogger('htmldiff')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info



class HTMLMatcher(SequenceMatcher):

    def __init__(self, source1, source2):
        SequenceMatcher.__init__(self, None, source1, source2)

    def set_seq1(self, a):
        SequenceMatcher.set_seq1(self, self.splitHTML(a))

    def set_seq2(self, b):
        SequenceMatcher.set_seq2(self, self.splitHTML(b))
        
    def splitTags(self, t):
        result = []
        pos = 0
        while 1:
            match = tagRE.search(t, pos=pos)
            if not match:
                result.append(t[pos:])
                break
            result.append(t[pos:match.start()])
            result.append(match.group(0))
            pos = match.end()
        return result

    def splitWords(self, t):
        return t.strip().split()

    def splitHTML(self, t):
        t = commentRE.sub('', t)
        r = self.splitTags(t)
        result = []
        for item in r:
            if item.startswith('<'):
                result.append(item)
            else:
                #result.extend(self.splitWords(item))
                result.append(' '.join(item.strip().split()))
        return result

    def htmlDiff(self, addStylesheet=False):
        opcodes = self.get_opcodes()
        a = self.a
        b = self.b
        out = StringIO()
        #print [o[0] for o in opcodes]
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                for item in a[i1:i2]:
                    out.write(item)
                    out.write(' ')
            if tag == 'delete' or tag == 'replace':
                self.textDelete(a[i1:i2], out)
            if tag == 'insert' or tag == 'replace':
                self.textInsert(b[j1:j2], out)
        html = out.getvalue()
        out.close()
        if addStylesheet:
            html = self.addStylesheet(html, self.stylesheet())
        return html

    def textDelete(self, lst, out):
        inSpan = False
        for item in lst:
            if item.startswith('<'):
                if inSpan:
                    out.write(self.endDeleteText())
                    inSpan = False
                out.write(self.formatDeleteTag(item))
            else:
                if not inSpan:
                    out.write(self.startDeleteText())
                    inSpan = True
                out.write(item)
                out.write(' ')
        if inSpan:
            out.write(self.endDeleteText())

    def textInsert(self, lst, out):
        inSpan = False
        for item in lst:
            if item.startswith('<'):
                if inSpan:
                    out.write(self.endInsertText())
                    inSpan = False
                out.write(self.formatInsertTag(item))
                out.write(item)
                out.write(' ')
            else:
                if not inSpan:
                    out.write(self.startInsertText())
                    inSpan = True
                out.write(item)
                out.write(' ')
        if inSpan:
            out.write(self.endInsertText())

    def stylesheet(self):
        return '''
ins { 
    background-color: #CCFF00; 
    color: #000000
}
del { 
    background-color: #FDC6C6;
    color: #000000
}
'''

    def addStylesheet(self, html, ss):
        match = headRE.search(html)
        if match:
            pos = match.end()
        else:
            pos = 0
        return ('%s<style type="text/css"><!--\n%s\n--></style>%s'
                % (html[:pos], ss, html[pos:]))

    def startInsertText(self):
        return '<ins>'
    def endInsertText(self):
        return '</ins> '
    def startDeleteText(self):
        return '<del>'
    def endDeleteText(self):
        return '</del> '
    def formatInsertTag(self, tag):
        return ''
    def formatDeleteTag(self, tag):
        return ''

class CharMatcher(SequenceMatcher):

    def __init__(self, source1, source2):
        SequenceMatcher.__init__(self, None, source1, source2, autojunk=False)


    def change_start_index(self):
        opcodes = self.get_opcodes()
        ret = 0
        for tag, i1, i2, j1, j2 in opcodes:
            if tag != 'equal':
                ret = j1
                break
        return ret



def htmldiff(source1, source2, addStylesheet=False):
    
    h = HTMLMatcher(source1, source2)
    return h.htmlDiff(addStylesheet)


def change_start_index(source1, source2):
    h = CharMatcher(source1, source2)
    return h.change_start_index()

