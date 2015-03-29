import re

from .common import InfoExtractor

class ExashareIE(InfoExtractor):
    _VALID_URL = r'http://www\.exashare\.com/(?P<id>[\da-z0-9]{12})'
    
    _TESTS = [{
        'url': 'http://www.exashare.com/kd6t1pr6gmug',
        'md5': 'd5d4252f80ebeab4dc2d5ceaed1b7970',
        'info_dict': {
            'id': 'kd6t1pr6gmug',
            'ext': 'mp4',
            'title': 'wildlife sample video',
            'thumbnail': 'http://vs26.exashare.com:8777/i/05/00000/1cm4kdmtawjk.jpg',
        },
    }]

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
