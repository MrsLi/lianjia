# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lianjia.mysqldb.SQLAlchemyDB import User,UserFormInfo,Location
import random,time,re
class LianjiaPipeline(object):
    def __init__(self):

        #本地数据库
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/sudi_zf?charset=utf8", max_overflow=5,
                               encoding='utf-8')


        # 生产数据库
        # engine = create_engine("mysql+pymysql://yunyudev:yuguodev@47.98.185.124:3306/sudi-zf?charset=utf8", max_overflow=5,
        #                        encoding='utf-8')
        # 创建DBSession类型:
        self.engine = engine

    def process_item(self, item, spider):
        DBsession = sessionmaker(bind=self.engine)
        session = DBsession()


        random_user_id = item['user_id']
        user = session.query(User).filter(User.id==random_user_id).first()
        location = session.query(Location).all()#type:list
        open_id = user.openid
        location_id=1

        info_location= item['location']#type:str

        for location_item in location:#type:Location
            info_location_split_list = info_location.split('&')
            for info_location_split_item in info_location_split_list:
                if info_location_split_item in location_item.name:
                    location_id = location_item.id

        type = '2'
        status = '1'

        random_time = random.randrange(1514736000,int(time.time()))
        room_pulsh_time = time.mktime(time.strftime(item['room_pulsh_time'], "%Y-%m-%d"))
        update_ts = room_pulsh_time
        create_ts = room_pulsh_time

        info =dict()
        split_str = item['room_type'].split('  ')
        split_str[0] =re.sub('室', '-', split_str[0])
        info['room_type'] =re.sub('厅', '-', split_str[0]).replace('卫','')

        zulin_str = item['chuzu_type']

        if zulin_str == '整租':
            info['sale_type'] = '1'
        elif zulin_str=='合租':
            info['sale_type']='2'
        else:
            info['sale_type']='1'

        info['price'] =item['totalPrice']

        info['limit'] = '1'
        info['wechat'] = item['brokerPhone']#微信号写成电话
        info['desc'] = item['title']
        info['imgs'] = item['imgList']

        if random_user_id <= 222:

            print('管道文件输出 info:'+str(info)+'random_user_id:'+str(random_user_id)+' open_id:'+open_id+' location_id:'+str(location_id))

            # 插入数据库
            userFormInfo  =UserFormInfo(user_id=random_user_id,location_id=location_id,openid=open_id,info=json.dumps(info),type=type,status=status,update_ts=update_ts,create_ts=create_ts)
            session.add(userFormInfo)
            session.commit()
            session.flush()
        return item


    def close_spider(self,spider):
        print("数据库关闭!")
