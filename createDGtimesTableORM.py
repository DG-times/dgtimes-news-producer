from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import registry, relationship

# DGtimes 실전
# ORM 객체 선언하기
engine = create_engine('mysql+pymysql://root:1234@localhost:3306/newdgtimes')

# registry 객체 생성
mapper_registry = registry()

# registry 객체에 MetaData가 포함되어있음
print(mapper_registry.metadata)

Base = mapper_registry.generate_base()

class Keyword(Base):
    __tablename__ = 'keyword'  # 데이터베이스에서 사용할 테이블 이름입니다.
    id = Column(Integer, primary_key=True)
    keyword = Column(String(255),nullable=False, unique=True)
    keyword_mapping = relationship("KeywordMapping", back_populates="keyword")
    __table_args__ = (UniqueConstraint('keyword', name='_keyword_uc'),)
    def __repr__(self):
       return f"Keyword(id={self.id!r}, keyword={self.keyword!r})"

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    content = Column(String(2000), nullable=False)
    main_url = Column(String(255), nullable=False)
    thumbnail_url = Column(String(500), nullable=False)
    date = Column(Date, nullable=False)
    keyword_mapping = relationship("KeywordMapping", back_populates="news") # lazy='dynamic'
    # Unique키 설정
    # http://daplus.net/python-%EC%97%AC%EB%9F%AC-%EC%97%B4%EC%97%90%EC%84%9C-%EA%B3%A0%EC%9C%A0-%ED%95%9C-sqlalchemy/
    __table_args__ = (UniqueConstraint('title', name='_title_uc'),)
    def __repr__(self):
        return f"News(id={self.id!r}, title={self.title!r}, content={self.content!r}, main_url={self.main_url!r}, thumbnail_url={self.thumbnail_url!r}, date={self.date!r})"

class KeywordMapping(Base):
    __tablename__ = 'keyword_mapping'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    news = relationship("News", back_populates="keyword_mapping")
    keyword_id = Column(Integer, ForeignKey('keyword.id'))
    keyword = relationship("Keyword", back_populates="keyword_mapping")
    def __repr__(self):
        return f"KeywordMapping(id={self.id!r})"

mapper_registry.metadata.create_all(engine)
Base.metadata.create_all(engine)