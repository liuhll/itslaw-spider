# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class ItslawSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.http.headers import Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    'Host': 'www.itslaw.com',
    "Content-Type": "application/json",
    "Referer":"https://www.itslaw.com"
}

class ItslawSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.headers = Headers(headers)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import requests,base64,json

class ItslawSpiderLoginMiddleware(object):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):
        if 'sessionId' not in request.cookies:
           loginApi = 'https://www.itslaw.com/api/v1/users/user/login/encryption'
           user_info = { 'userName': "1029765111@qq.com", 'password':str(base64.b64encode('Liuhl881208'.encode('utf-8')),'utf-8'), 'isAutoLogin': True }
           user_data = json.dumps(user_info)
           resp = requests.post(loginApi,data=user_data,headers = headers)
           if resp.status_code != 200:
              raise Exception('登录接口请求失败')
           resp_result = json.loads(resp.text)
           if resp_result['result']['code'] != 0:
              # todo 登录重试
              pass
           request.cookies['sessionId'] = resp.cookies['sessionId']
        return None            