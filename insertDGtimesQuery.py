import json
import createDGtimesTableORM as ct
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from konlpy.tag import Mecab

mecab = Mecab("C:\mecab\mecab-ko-dic")

engine = create_engine('mysql+pymysql://root:1234@localhost:3306/newdgtimes')

file_path = "C:/Users/akoho/Desktop/실습_6조/뉴스 자료/017.뉴스 기사 기계독해 데이터/01.데이터/1.Training/원천데이터/TS_unanswerable/TS_unanswerable.json"

keywords = set([])
keyword_all = set([])

news_Entity = ct.News()
keyword_Entity = ct.Keyword()
keywordMapping_Entity = ct.KeywordMapping()

select_news_id = ""
select_keyword_id = ""

with open(file_path, 'rt', encoding='UTF-8') as file:
    data = json.load(file)
    # print(type(data))

    # 테스트용으로 지울것
    count = 0
    count2 = 0

    for doc_data in data["data"]:
        # 테스트용으로 지울것
        count = count + 1

        title = doc_data["doc_title"]
        content = ""
        date = doc_data["created"]
        mainURL = "https://news.naver.com/"
        thumbnailURL = ""
        doc_source = doc_data["doc_source"]

        if doc_source == "전북일보":
            thumbnailURL = "https://img3.yna.co.kr/photo/cms/2021/07/01/93/PCM20210701000193990_P4.jpg"
        elif doc_source == "충청일보":
            thumbnailURL = "https://pds.saramin.co.kr/company/logo/201902/27/pnkmo3_tqat-0_logo.jpg"
        elif doc_source == "경기일보":
            thumbnailURL = "https://t1.daumcdn.net/cfile/tistory/233FC0405889DFF826"
        elif doc_source == "강원일보":
            thumbnailURL = "https://allforyoung-homepage-maycan.s3.ap-northeast-2.amazonaws.com/uploads/post_photos/2020/12/02/%E3%85%87.jpg"
        elif doc_source == "부산일보":
            thumbnailURL = "https://2.bp.blogspot.com/-YstI0LU69oQ/Vzq-YipdMiI/AAAAAAAAEZA/ygAQy5lKsLoNPT05vTA0YAAas3VcsCtOgCLcB/w1200-h630-p-k-no-nu/%25EB%25B6%2580%25EC%2582%25B0%25EC%259D%25BC%25EB%25B3%25B4%2B%25EB%25A1%259C%25EA%25B3%25A0.png"
        elif doc_source == "경북일보":
            thumbnailURL = "http://www.kyongbuk.co.kr/image/logo/snslogo_20190326103650.png"
        elif doc_source == "전남일보":
            thumbnailURL = "https://www.jnilbo.com/assets/nwcms/custom/site/images/common/h_logo.png"
        elif doc_source == "영남일보":
            thumbnailURL = "https://culture.yeongnam.com/culture/poster/banner19.jpg"
        elif doc_source == "한국일보":
            thumbnailURL = "https://blog.kakaocdn.net/dn/dEwZkF/btqDDX56sPj/6cdg1P8IcjCep9T1B7DhGK/img.jpg"
        elif doc_source == "중앙일보":
            thumbnailURL = "http://www.journalist.or.kr/data/photos/cdn/20200728/art_1594191058.jpg"
        elif doc_source == "국민일보":
            thumbnailURL = "https://image.kmib.co.kr/images/company/img_kmib_meta.jpg"
        elif doc_source == "세계일보":
            thumbnailURL = "https://pds.saramin.co.kr/company/logo/201902/26/pnivec_x3ur-0_logo.jpg"

        # print(doc_data["doc_title"])
        # print(doc_data["doc_source"])
        # print(doc_data["created"])
        title_keyword = mecab.pos(doc_data["doc_title"])
        print(title_keyword)
        for search_keyword in title_keyword:
            if search_keyword[1] == 'NNP' or search_keyword[1] == 'NNG':
                # print(search_keyword[0])
                keywords.add(search_keyword[0])
        paragraphs = doc_data["paragraphs"]
        for context in paragraphs:
            # 테스트용으로 지울것
            count2 = count2 + 1

            content = context["context"]
            context_keyword = mecab.pos(context["context"])
            for search_keyword in context_keyword:
                if search_keyword[1] == 'NNP' or search_keyword[1] == 'NNG':
                    # print(search_keyword[0])
                    keywords.add(search_keyword[0])
            # 테스트용으로 지울것
            # if count2 == 1:
            #     break
        stmt_new = db.insert(ct.News).values(title=title, content=content, main_url=mainURL, thumbnail_url=thumbnailURL, date=date)
        # print(stmt_new)
        compiled = stmt_new.compile()

        # 뉴스 데이터 삽입 시도
        # 뉴스 저장 완료후 매핑관계를 위한 news id가 필요
        # 예외처리 참고 자료
        # https://velog.io/@martinalee94/SQLAlchemy-try-except%EB%A1%9C-integrityerror-%EC%9E%A1%EA%B8%B0
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt_new)
                # 이 프로세서에는 commit이 필요없다고 하는데 왜일까..?
                # https://dev-qa.com/850554/how-solve-the-error-connection-object-has-attribute-commit
                # conn.commit()

        except IntegrityError as e:
            print("뉴스 테이블에 중복된 데이터가 있습니다.")
            # 중복되는 뉴스의 ID값 검색
            news_id = select(ct.News.id).where(ct.News.title == title)
            with engine.connect() as conn:
                for row in conn.execute(news_id):
                    select_news_id = row[0]
                    # print(row[0])

        # 키워드 데이터 저장 필요
        for keyword in keywords:
            stmt_keyword = db.insert(ct.Keyword).values(keyword=keyword)
            compiled = stmt_keyword.compile()
            try:
                with engine.connect() as conn:
                    result = conn.execute(stmt_keyword)

            except IntegrityError as e:
                print("키워드 테이블에 중복된 데이터가 있습니다.")
                # 중복되는 키워드의 ID값 검색
                keyword_id = select(ct.Keyword.id).where(ct.Keyword.keyword == keyword)
                with engine.connect() as conn:
                    for row in conn.execute(keyword_id):
                        select_keyword_id = row[0]
                        # print(row[0])

            # 연관 관계 매핑 방법?
            # keywordMapping_Entity.news_id = news_Entity
            # keywordMapping_Entity.keyword_id = keyword_Entity
            # 연관 관계 매핑 방법???
            # news_Entity.keyword_mapping.append(keywordMapping_Entity)
            # keyword_Entity.keyword_mapping.append(keywordMapping_Entity)

            # Insert.returning() - ??????
            # insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
            # print(insert_stmt)

            # 테스트용 코드 - 뉴스랑 키워드 다넣고, 다시 돌려서 매핑?
            # stmt_keywordMapping = db.insert(ct.KeywordMapping).values(news_id=select_news_id, keyword_id=select_keyword_id)

            compiled = stmt_keywordMapping.compile()
            with engine.connect() as conn:
                result = conn.execute(stmt_keywordMapping)

        keywords.clear()
        # 중복된 키워드가 있는경우 해당 키워드의 ID 조회 필요
        # 키워드 데이터 저장 완료후 매핑관계 필요

        # 테스트용으로 지울것
        if count == 10:
            break

conn.close()

print(keywords)
# stmt_new = db.insert(ct.News).values(title=doc_data["doc_title"], content='content', main_url='main_url',
#                                              thumbnail_url='thumbnail_url', date=doc_data["created"])

# SQL 표현식 구성
# stmt_new = db.insert(ct.News).values(title='title', content='content', main_url='main_url',thumbnail_url='thumbnail_url',date='20220101')
# stmt = db.insert(ct.Keyword).values(keyword='spongebob')
# print(stmt)
#
# compiled = stmt.compile()
# print(compiled.params)
#
# # 명령문 실행 - core방식
# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()