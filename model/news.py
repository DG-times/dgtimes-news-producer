import json
from faker import Faker
import datetime as dt
from konlpy.tag import Kkma
from collections import Counter
import random

fake = Faker("ko_KR")

class News:
    
    def __init__(self,title,content, keyword) -> None:
        self.title = title
        self.content = content
        self.writer = fake.name()
        self.publisher = News.get_publisher()
        self.category = 1
        self.tag = News.make_tags(keyword)
        self.publishedDate = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mainUrl = "https://news.naver.com/"
        self.thumbnailUrl = News.get_thumbnail_url(self.publisher)
        self.keyword = keyword

    def get_publisher():
        publisher_list = ["전북일보", "충청일보", "경기일보", "강원일보", "부산일보", "경북일보", "전남일보", "영남일보", "한국일보", "중앙일보", "국민일보", "세계일보"]

        return random.choice(publisher_list)


    def get_thumbnail_url(publisher):
        if publisher == "전북일보":
            return "https://img3.yna.co.kr/photo/cms/2021/07/01/93/PCM20210701000193990_P4.jpg"
        elif publisher == "충청일보":
            return "https://pds.saramin.co.kr/company/logo/201902/27/pnkmo3_tqat-0_logo.jpg"
        elif publisher == "경기일보":
            return "https://t1.daumcdn.net/cfile/tistory/233FC0405889DFF826"
        elif publisher == "강원일보":
            return "https://allforyoung-homepage-maycan.s3.ap-northeast-2.amazonaws.com/uploads/post_photos/2020/12/02/%E3%85%87.jpg"
        elif publisher == "부산일보":
            return "https://2.bp.blogspot.com/-YstI0LU69oQ/Vzq-YipdMiI/AAAAAAAAEZA/ygAQy5lKsLoNPT05vTA0YAAas3VcsCtOgCLcB/w1200-h630-p-k-no-nu/%25EB%25B6%2580%25EC%2582%25B0%25EC%259D%25BC%25EB%25B3%25B4%2B%25EB%25A1%259C%25EA%25B3%25A0.png"
        elif publisher == "경북일보":
            return "http://www.kyongbuk.co.kr/image/logo/snslogo_20190326103650.png"
        elif publisher == "전남일보":
            return "https://www.jnilbo.com/assets/nwcms/custom/site/images/common/h_logo.png"
        elif publisher == "영남일보":
            return "https://culture.yeongnam.com/culture/poster/banner19.jpg"
        elif publisher == "한국일보":
            return "https://blog.kakaocdn.net/dn/dEwZkF/btqDDX56sPj/6cdg1P8IcjCep9T1B7DhGK/img.jpg"
        elif publisher == "중앙일보":
            return "http://www.journalist.or.kr/data/photos/cdn/20200728/art_1594191058.jpg"
        elif publisher == "국민일보":
            return "https://image.kmib.co.kr/images/company/img_kmib_meta.jpg"
        elif publisher == "세계일보":
            return "https://pds.saramin.co.kr/company/logo/201902/26/pnivec_x3ur-0_logo.jpg"
    
    def make_tags(keyword):

        tags_length = len(keyword) if len(keyword) < 3 else 3

        tags = ""
        for i in range(tags_length):
            tags = tags + " #" + keyword[i][0]
        
        return tags

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
