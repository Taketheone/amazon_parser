# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import random
import os
import csv
from datetime import datetime
import time

class Keyword_to_listing():
    def __init__(self):
        #关键词列表，注意英文引号+英文逗号，爬取的资料保存在listing info文件夹下同名关键词文件夹里
        self.keyword_list = [
            "hands free dog leash",
        ]
        #爬取页数
        self.max_page = 3
        #每爬取一个网页后休息的时间秒数，爬取太快会导致爬虫被禁
        self.sleep_time = 0
        #下面的不用修改
        self.csv_file_name = ""
        self.picture_folder = ""
        self.picture_url = ""
        self.asin = ""
        self.listing_info_dict_list = []

    def download_soup_by_url(self, url):
        # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        headers_list = [
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
            {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
            {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
        ]
        headers = random.choice(headers_list)
        # print("headers: ", headers)
        china_proxies_list = [
            {'http:': 'http://123.56.169.22:3128'},
            {'http:': 'http://121.196.226.246:84'},
            {'http:': 'http://122.49.35.168:33128'},
            {'http:': 'http://124.238.235.135:81'},
            {'http:': 'http://121.40.199.105:80'},
            {'http:': 'http://202.99.99.123:80'},
            {'http:': 'http://61.153.67.110:9999'},
            {'http:': 'http://121.40.213.161:80'},
            {'http:': 'http://121.42.163.161:80'},
            {'http:': 'http://111.13.7.42:81'},
            {'http:': 'http://114.215.103.121:8081'},
            {'http:': 'http://175.11.157.195:80'}
        ]
        usa_proxies_list = [
            {'http:': 'http://40.140.245.109:8080'},
            {'http:': 'http://50.116.12.78:8118'},
            {'http:': 'http://69.85.70.37:53281'},
            {'http:': 'http://35.195.160.37:1244'},
            {'http:': 'http://104.131.122.164:8118'},
            {'http:': 'http://32.115.161.78:53281'},
            {'http:': 'http://165.227.7.51:80'},
            {'http:': 'http://72.169.78.49:87'},
            {'http:': 'http://52.24.67.217:80'},
            {'http:': 'http://209.159.156.199:80'},
            {'http:': 'http://198.35.55.147:443'},
            {'http:': 'http://97.72.129.36:87'},
            {'http:': 'http://152.160.35.171:80'},
            {'http:': 'http://191.96.51.224:8080'},
            {'http:': 'http://45.55.157.204:80'}
        ]
        # proxies = random.choice(usa_proxies_list)
        proxies = random.choice(china_proxies_list)
        # print("proxies: ", proxies)
        # r = requests.get(url, headers=headers)
        r = requests.get(url, headers=headers, proxies=proxies)
        # print("Downloading: r.status_code=", r.status_code)
        # print("url: ", url)
        if r.status_code != 200:
            headers = random.choice(headers_list)
            proxies = random.choice(china_proxies_list)
            r = requests.get(url, headers=headers, proxies=proxies)
            # print("Downloading: r.status_code=", r.status_code)

        # soup = BeautifulSoup(r.content, 'html.parser')
        soup = BeautifulSoup(r.text.encode(r.encoding).decode('utf-8'), 'html.parser')
        # soup = BeautifulSoup(r.read(), 'html.parser')
        # soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
        # soup = BeautifulSoup(r.content, 'html5lib')
        time.sleep(self.sleep_time)
        return soup

    def download_picture_by_url(self):
        print("start to download picture...")

        try:
            pic = requests.get(self.picture_url, timeout=10)
            picture_name = self.picture_folder + "/"+ str(self.asin) + '.jpg'
            with open(picture_name, 'wb') as fp:
                fp.write(pic.content)
            print("success to download picture")
        except requests.exceptions.ConnectionError:
            print("download picture failed!")
        print("***********************************")

    def dict_list_to_csv_file(self):
        print("start to write csv file...")
        headers = []
        for i in self.listing_info_dict_list[0]:
            headers.append(i)

        csv_folder = self.picture_folder
        csv_file_path = csv_folder + "/" + str(self.csv_file_name) + ".csv"

        try:
            with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(self.listing_info_dict_list)
                print("success to write csv file...")
        except:
            print("fail to write csv!")

        print("***********************************")

    def asin_to_listing_info(self):

        asin = self.asin
        print("asin: ", asin)

        url = "https://www.amazon.com/dp/" + asin
        print("url: ", url)

        soup = self.download_soup_by_url(url)

        brand = ""
        try:
            if soup.find(id="bylineInfo"):
                brand = soup.find(id="bylineInfo").get_text().strip()
            if soup.find(id="brand"):
                brand = soup.find(id="brand").get_text().strip()
        except:
            pass
        print("brand: ", brand)

        badge = ""
        try:
            if soup.find("a", class_="badge-link"):
               badge = " ".join(soup.find("a", class_="badge-link").get_text().strip().split())
        except:
            pass
        print("badge: ", badge)

        title = ""
        try:
            if soup.find(id="productTitle"):
                title = soup.find(id="productTitle").get_text().strip()
        except:
            pass
        print("title: ", title)

        variation_name = ""
        try:
            if soup.find(id="variation_pattern_name"):
                variation_name = soup.find(id="variation_pattern_name").find("span").get_text().strip()
                print("variation_pattern_name: ", variation_name)
            elif soup.find(id="variation_color_name"):
                variation_name = soup.find(id="variation_color_name").find("span").get_text().strip()
                print("variation_color_name: ", variation_name)
            elif soup.find(id="variation_size_name"):
                variation_name = soup.find(id="variation_size_name").find("span").get_text().strip()
                print("variation_size_name: ", variation_name)
            else:
                print("variation_name: ", variation_name)
        except:
            pass

        price = ""
        sale_price =""
        try:
            if soup.find(id="price"):
                price = soup.find(id="price").find("span").get_text().strip()
            if soup.find(id="priceblock_ourprice"):
                price = soup.find(id="priceblock_ourprice").get_text().strip()
            if soup.find(id="priceblock_saleprice"):
                sale_price = soup.find(id="priceblock_saleprice").get_text().strip()
        except:
            pass
        print("price: ", price)
        print("sale_price: ", sale_price)

        sold_by = ""
        try:
            if soup.find(id="merchant-info"):
                # print("soup.find(id='merchant-info').get_text().strip(): ", soup.find(id="merchant-info").get_text().strip())
                sold_by = " ".join(soup.find(id="merchant-info").get_text().strip().split())
        except:
            pass
        print("sold_by: ", sold_by)

        how_many_sellers = ""
        try:
            if soup.find(id="olp_feature_div"):
                how_many_sellers = soup.find(id="olp_feature_div").find("a").get_text().strip()
        except:
            pass
        print("how_many_sellers: ", how_many_sellers )

        bullets_list = []
        try:
            if  soup.find("div", id="feature-bullets"):
                bullets_contents = soup.find("div", id="feature-bullets").find_all("span", class_="a-list-item")
                print("bullets: ")
                for bullets_content in bullets_contents:
                    print(bullets_content.get_text().strip())
                    #toys
                    if bullets_content.span:
                        continue
                    bullets_list.append(bullets_content.get_text().strip())
        except:
            pass

        description = ""
        try:
            if soup.find(id="productDescription"):
                description = soup.find(id="productDescription").get_text()
            if soup.find(id="aplus"):
                description = soup.find(id="aplus").get_text()
            description = " ".join(description.split())
        except:
            pass
        print("description: ", description)

        salesrank = ""
        try:
            if soup.find(id="SalesRank"):
                salesrank = soup.find(id="SalesRank")
                salesrank = salesrank.get_text().strip()
                salesrank = re.search('#(\d|,)+', salesrank)
                salesrank = salesrank.group()
                salesrank = salesrank.replace(',', '')
                salesrank = salesrank.replace('#', '')
            #toys
            if soup.find(id="productDetails_detailBullets_sections1"):
                trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
                for tr in trs:
                    if tr.find("th").get_text().strip():
                        if tr.find("th").get_text().strip() == "Best Sellers Rank":
                            salesrank = tr.find("td").get_text().strip()
                            salesrank = re.search('#(\d|,)+', salesrank)
                            salesrank = salesrank.group()
                            salesrank = salesrank.replace(',', '')
                            salesrank = salesrank.replace('#', '')
        except:
            pass
        print("salesrank: ", salesrank)

        review_num = 0
        try:
            if soup.find(id="acrCustomerReviewText"):
                review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip()
        except:
            pass
        print("review_num: ", review_num)

        review_value = 0
        try:
            if soup.find(class_="arp-rating-out-of-text"):
                review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
                review_value = re.search('(.*?)\s', review_value)
                review_value = review_value.group()
                review_value = review_value.strip()
        except:
            pass
        print("review_value: ", review_value)

        qa_num = ""
        try:
            if soup.find(id="askATFLink"):
                qa_num = soup.find(id="askATFLink").get_text().split()[0].strip()
        except:
            pass
        print("qa_num: ", qa_num)

        picture_url = ""
        try:
            picture_urls_dict = dict()
            if soup.find("img", id="landingImage"):
                picture_urls = soup.find("img", id="landingImage")["data-a-dynamic-image"]
                picture_urls_dict = eval(picture_urls)
            picture_urls_list = []
            for key in picture_urls_dict.keys():
                picture_urls_list.append(key)
            picture_url = picture_urls_list[0]
        except:
            pass
        print("picture_url: ", picture_url)

        listing_info_dict = {
                             "asin": asin,
                             "url": url,
                             "brand": brand,
                             "badge": badge,
                             "title": title,
                             "variation_name": variation_name,
                             "price": price,
                             "sale_price": sale_price,
                             "sold_by": sold_by,
                             "how_many_sellers": how_many_sellers,
                             "bullets": bullets_list,
                             "description": description,
                             "salesrank": salesrank,
                             "review_num": review_num,
                             "review_value": review_value,
                             "qa_num": qa_num,
                             "picture_url": picture_url
                             }
        # print(listing_info_dict)
        return listing_info_dict

    def keyword_to_all_listing_asin_list(self):
        base_url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
        first_page_url = base_url + self.keyword

        pages_urls_list = []
        pages_urls_list.append(first_page_url)
        page = 1
        while page <= self.max_page:
            soup = self.download_soup_by_url(pages_urls_list[-1])
            try:
                if soup.find(id="pagnNextLink")["href"]:
                    next_page_url_part2 = soup.find(id="pagnNextLink")["href"]
                    next_page_url = "https://www.amazon.com" + next_page_url_part2
                    pages_urls_list.append(next_page_url)
                page = page + 1
            except:
                pass

            try:
                lis = soup.find_all("li", class_="s-result-item")
                for index, li in enumerate(lis):
                    try:
                        asin = li["data-asin"]
                        self.asin = asin

                        page_rank = "page" + str(page - 1) + "-" + str(index + 1)
                        print("page_rank: ", page_rank)

                        sponsored_or_natural_rank = "natural_rank"
                        try:
                            if li.find("h5").get_text().strip().split()[0]:
                                if li.find("h5").get_text().strip().split()[0] == "Sponsored":
                                    sponsored_or_natural_rank = "sponsored"
                                else:
                                    sponsored_or_natural_rank = "natural_rank"
                        except:
                            pass
                        print("sponsored_or_natural_rank: ", sponsored_or_natural_rank)

                        is_prime = ""
                        try:
                            if li.find("i", class_="a-icon-prime"):
                                is_prime  = "prime"
                        except:
                            pass
                        print("is_prime: ", is_prime)

                        listing_info_dict = self.asin_to_listing_info()
                        listing_info_dict["page_rank"] = page_rank
                        listing_info_dict["sponsored_or_natural_rank"] = sponsored_or_natural_rank
                        listing_info_dict["is_prime"] = is_prime
                        self.listing_info_dict_list.append(listing_info_dict)
                        try:
                            self.picture_url = listing_info_dict['picture_url']
                            self.download_picture_by_url()
                        except:
                            pass
                    except:
                        pass
            except:
                pass

    def get_listing_info(self):
        start_time = datetime.now()

        for keyword in self.keyword_list:
            self.keyword = keyword
            self.picture_folder = "listing info/" + keyword
            self.csv_file_name = keyword

            if not os.path.exists("listing info"):
                print("listing info folder does not exist, creating the folder...")
                os.mkdir("listing info")
                print("success to create listing info folder")
                print("***********************************")

            if not os.path.exists(self.picture_folder):
                print("picture folder does not exist, creating the folder...")
                os.mkdir(self.picture_folder)
                print("success to create picture folder")
                print("***********************************")

            self.keyword_to_all_listing_asin_list()
            self.dict_list_to_csv_file()

        end_time = datetime.now()
        how_many_seconds = end_time - start_time
        print(start_time)
        print(end_time)
        print(str(how_many_seconds.total_seconds()) + "seconds")

#main function
keyword_to_listing = Keyword_to_listing()
keyword_to_listing.get_listing_info()
