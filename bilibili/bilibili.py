import requests
import pandas as pd
from lxml import etree

class TeachInChina(object):
    # 拿到网址，传入爬取的页数
    def __init__(self, max_page):
        self.start_urls = ['https://search.bilibili.com/all?keyword=python&from_source=nav_suggest_new' \
                           '&page={}'.format(page) for page in range(1, max_page+1)]
    def get_data(self):
        for url in self.start_urls:
            res = requests.get(url)
            page = url.split('=')[-1]
            self.parse_data(res, page)
            print('成功爬取并保存第{}页数据!'.format(page))

    @staticmethod
    def parse_data(http_addr, page):
        if http_addr.status_code == 200:
            http_html = etree.HTML(http_addr.text)

            for i in range(1,21):
                # 标题
                title = http_html.xpath('normalize-space(//*[@class="video-item matrix"][{}]/a/attribute::title)'.format(i))
                # 观看
                watch_num = http_html.xpath('normalize-space(//*[@class="video-item matrix"][{}]/div[1]/div[3]/span[1]/text())'.format(i))
                # 弹幕
                barrage_num = http_html.xpath('normalize-space(//*[@class="video-item matrix"][{}]/div[1]/div[3]/span[2]/text())'.format(i))
                # 上传时间
                uptime = http_html.xpath('normalize-space(//*[@class="video-item matrix"][{}]/div[1]/div[3]/span[3]/text())'.format(i))
                # up主
                uper = http_html.xpath('normalize-space(//*[@class="video-item matrix"][{}]/div[1]/div[3]/span[4]/a/text())'.format(i))

                # 数据保存
                data = pd.DataFrame({'title': [title],'watch-num':[watch_num],'barrage_num':[barrage_num],'uptime':[uptime],'uper':[uper]})
                data.to_csv('bilibili.csv', index=False, mode='a', header=False)

        else:
            print('链接{}请求不成功!'.format(http_addr.url))

# 入口函数
if __name__ == '__main__':
    # 初始化JOB类
    job = TeachInChina(50)
    job.get_data()