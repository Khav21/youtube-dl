import re

from .common import InfoExtractor

class ExashareIE(InfoExtractor):
    _VALID_URL = r'http://www\.exashare\.com/(?P<id>[\da-z0-9]{12})'

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)

        video_id = mobj.group('id')
        webpage_url = 'http://www.exashare.com/' + video_id
        webpage = self._download_webpage(webpage_url, video_id)

        # Log that we are starting to parse the page
        self.report_extraction(video_id)

        video_url = self._html_search_regex(r'file: "(.+?)"', webpage, u'video URL')
        title =  self._html_search_regex(r'<h4>([^<]+)</h4>', webpage, u'title')
        return [{
            'id':        video_id,
            'url':       video_url,
            'ext':       'mp4',
            'title':     title,
        }]
