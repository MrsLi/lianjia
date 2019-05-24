# coding=utf-8
from sqlalchemy import Column, String, create_engine,INT,Integer
from sqlalchemy.ext.declarative import declarative_base

#初始化数据库ORM连接（SQLAlchemy）

# 创建对象的基类:
Base = declarative_base()
# 定义UserFormInfo对象:
class UserFormInfo(Base):
    # 表的名字:
    __tablename__='sd_user_form_info'
    # 表的结构:
    id = Column(Integer,primary_key=True)
    user_id = Column(String(255),unique=True)  # 用户ID
    location_id = Column(String(255),unique=True)  # 地铁ID
    openid = Column(String(255),unique=True)  # 微信的openid
    rank = Column(String(255), unique=True)  #
    info = Column(String(255),unique=True)  # 配置信息
    type = Column(String(255),unique=True)  # 类型 1求租 2放租者
    status = Column(String(255),unique=True)  # 状态 1正常 2删除
    update_ts = Column(String(255),unique=True)  # 更新时间
    create_ts = Column(String(255),unique=True)  # 信息插入时间


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'sd_user'

    # 表的结构:
    id = Column(primary_key=True)
    openid = Column(String(255),unique=True)
    union_id = Column(String(255),unique=True)


# 定义Location对象:
class Location(Base):
    # 表的名字:
    __tablename__ = 'sd_location'

    # 表的结构:
    id = Column(primary_key=True)
    parent_id = Column(unique=True)
    name = Column(String(255),unique=True) #地名
    level = Column(String(255),unique=True)#等级
