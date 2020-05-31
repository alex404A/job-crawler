import scrapy
import json
import re
from langdetect import detect
from datetime import datetime, timedelta

class XingSpider(scrapy.Spider):
    name = 'xing'

    start_urls = [
        'https://www.xing.com/jobs/api/search?keywords=full%20stack&location=Hamburg&radius=20&sort=date&limit=20&offset=0',
        'https://www.xing.com/jobs/api/search?keywords=Backend%20Developer&location=Hamburg&radius=20&sort=date&limit=20&offset=0',
        'https://www.xing.com/jobs/api/search?keywords=node.js%20developer&location=Hamburg&radius=20&sort=date&limit=20&offset=0',
        'https://www.xing.com/jobs/api/search?keywords=java%20developer&location=Hamburg&radius=20&sort=date&limit=20&offset=0',
    ]

    def parse(self, response):
        def is_expire(date_str):
            publish_time = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            expire_time = datetime.today() - timedelta(days=7)
            return publish_time < expire_time
        result = json.loads(response.text)
        current_page = result['meta']['currentPage']
        max_page = result['meta']['maxPage']
        count = result['meta']['count']
        if current_page < max_page:
            offset = current_page * (count // (max_page - 1))
            next_page = re.sub("offset=\d+", "offset=" + str(offset), response.url)
            yield scrapy.Request(next_page, callback=self.parse)

        for item in [x for x in result['items'] if not is_expire(x['activatedAt'])]:
            job_page = item['link']
            yield scrapy.Request(job_page, callback=self.parse_job)

    def parse_job(self, response):
        def is_friendly(jd):
            if jd is None or jd.strip() == '':
                return False
            return detect(jd) == 'en'
            # jd_in_lower = description.lower()
            # return 'english' in jd_in_lower or 'englisch' in jd_in_lower
        name = response.url.split('/')[-1].split('?')[0]
        description = ''.join(response.css('div[id=job-posting-description] *::text').getall()).strip()
        company = response.css('.fixed-top-bar h2::text').get()
        yield {
            'url': response.url,
            'company': company,
            'description': description,
            'name': name,
            'is_friendly': is_friendly(description)
        }
