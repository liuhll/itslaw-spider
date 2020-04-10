import scrapy,base64,json,logging,time
import urllib.parse
from itslaw_spider.utils.list_conditions import get_a_condition
from itslaw_spider.items import ItslawDetailSpiderItem
class ItslawSpider(scrapy.Spider):
    name = 'itslawspider'
    allowed_domains = ['www.itslaw.com']
    
    def start_requests(self):                
        yield self.list_requests(0,0)

    def list_requests(self,start_index,condition_index):
        list_api = 'https://www.itslaw.com/api/v1/caseFiles?startIndex=%d&countPerPage=20&sortType=2%s'
        condition = get_a_condition(condition_index)
        condition_val = ''
        for (k,v) in condition['value'].items():
            condition_val += '&conditions=%s'%(urllib.parse.quote(v))
        list_api = list_api%(start_index,condition_val)
        request_meta_data = {'totalCount': condition['totalCount'],'startIndex': start_index, 'conditionIndex': condition_index }
        return scrapy.Request(list_api, meta=request_meta_data, callback=self.parse_list)

    def parse_list(self,response):
        if response.status != 200:
            raise Exception('请求列表信息失败')
        response_text = json.loads(response.text)
        if response_text['result']['code'] != 0:
            raise Exception('获取列表信息失败,原因%s'%(response_text['result']['message']))
        judgements = response_text['data']['searchResult']['judgements']
        for judgement in judgements:
            yield self.detail_requests(judgement,response.request.cookies)
        get_judgements_list_count = len(judgements) # response_text['data']['searchResult']['totalCount']
        condition_total_count,start_index,condition_index = response.request.meta['totalCount'],response.request.meta['startIndex'],response.request.meta['conditionIndex']
        if get_judgements_list_count > 0:
            next_start_index = start_index + 20        
        else:
            next_start_index = 0
            condition_index += 1
        yield self.list_requests(next_start_index,condition_index)    


    def detail_requests(self,judgement,cookies):
        detail_api='https://www.itslaw.com/api/v1/detail?judgementId=%s'%(judgement['id'])
        return scrapy.Request(detail_api, cookies = cookies, callback=self.parse_detail)


    def parse_detail(self,response):
        if response.status != 200:
            raise Exception('请求裁判文书详情失败')
        response_text = json.loads(response.text)
        if response_text['result']['code'] != 0:
            raise Exception('获取裁判文书详情失败,原因%s'%(response_text['result']['message']))

        itslaw_detail = response_text['data']
        itslaw_detail_item = ItslawDetailSpiderItem(fullJudgement = itslaw_detail['fullJudgement'])
        return itslaw_detail_item
        
