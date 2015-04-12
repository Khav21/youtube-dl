# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..compat import (
    compat_urllib_parse,
    compat_urllib_request,
)
from ..utils import (
    ExtractorError,
    int_or_none,
)

class ExashareIE(InfoExtractor):
    _VALID_URL = r'http://www\.exashare\.com/(?P<id>[\da-z0-9]{12})'
    
    _TESTS = [{
        'url': 'http://www.exashare.com/kd6t1pr6gmug',
        'md5': '0891494ffb872a7786e12005dfa6e8f2',
        'info_dict': {
            'id': 'kd6t1pr6gmug',
            'ext': 'mp4',
            'title': 'wildlife sample video',
            'thumbnail': 'http://vs26.exashare.com:8777/i/05/00000/1cm4kdmtawjk.jpg',
        },
    }]
    
    _FILE_NOT_FOUND_REGEX = r'>(?:404 - )?File Not Found<'

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)

        video_id = mobj.group('id')
        webpage_url = 'http://www.exashare.com/' + video_id
        webpage = self._download_webpage(webpage_url, video_id)
        
        fields = dict(re.findall(r'''(?x)<input\s+
            type="hidden"\s+
            name="([^"]+)"\s+
            (?:id="[^"]+"\s+)?
            value="([^"]*)"
            ''', webpage))

        if fields['op'] == 'download1':
            countdown = int_or_none(self._search_regex(
                r'<span id="countdown_str">(?:[Ww]ait)?\s*<span id="cxc">(\d+)</span>\s*(?:seconds?)?</span>',
                webpage, 'countdown', default=None))
            if countdown:
                self._sleep(countdown, video_id)

            post = compat_urllib_parse.urlencode(fields)

            req = compat_urllib_request.Request(url, post)
            req.add_header('Content-type', 'application/x-www-form-urlencoded')

            webpage = self._download_webpage(req, video_id, 'Downloading video page')

        # Log that we are starting to parse the page
        self.report_extraction(video_id)

        video_url = self._html_search_regex(r'file: "(.+?)"', webpage, u'video URL')
        title =  self._html_search_regex(r'<h4>([^<]+)</h4>', webpage, u'title')
        thumbmail = self._html_search_regex(r'image: "(.+?)"', webpage, u'thumbnail')
        return [{
            'id':        video_id,
            'url':       video_url,
            'ext':       'mp4',
            'title':     title,
            'thumbnail': thumbmail,
        }]
