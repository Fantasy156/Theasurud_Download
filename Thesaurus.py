from requests import get
from lxml import etree


def info(args):
    if type(args) is bool:
        return
    elif type(args) is list:
        node = args
    else:
        node = args.split()
    return node


def html(args):
    return etree.HTML(args)


class sogou(object):
    def __init__(self):
        self.api = 'https://pinyin.sogou.com'
        self.list_href = []
        self.__dict = {}

    def web(self, name: str, href: str):
        print(f'正在获取 {name} 分类')
        res = html(get(f'{self.api}{href}').text)
        node = res.xpath(
            '//div[@class="dict_category_list_title "]/a/text() | //div[@class="dict_category_list_title"]/a/text()')
        href = res.xpath(
            '//div[@class="dict_category_list_title "]/a/@href | //div[@class="dict_category_list_title"]/a/@href')

        if node and href:
            for name, href in zip(node, href):
                self.sort(name, href)
        return self.__dict

    def sort(self, name, href):
        if href in self.list_href:
            return
        self.list_href.append(href)
        print(f'正在获取 {name} 分类')

        res = html(get(f'{self.api}{href}').text)

        try:
            node = info(res.xpath(
                '//li//span//a/text()')[-1] or res.xpath(
                '//a[@class="citylist"]/text()'))

            href = info(res.xpath(
                '//li//span//a/@href')[-1] or res.xpath(
                '//a[@class="citylist"]/@href'))
        except IndexError:
            node = False
            href = False

        if node and href:
            for name, href in zip(node, href):
                self.sort(name, href)

        url = res.xpath(
            '//div[@class="dict_dl_btn"]/a/@href')
        name = res.xpath(
            '//div[@class="detail_title"]/a/text()')

        for i in range(len(name)):
            self.__dict[name[i]] = url[i]

    @property
    def main(self):
        name = '搜狗词库'
        href = '/dict/'
        return self.web(name=name, href=href)


sogou = sogou().main

if __name__ == "__main__":
    print(sogou)
