# coding=utf-8
import requests
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lianjia.mysqldb.SQLAlchemyDB import User,UserFormInfo,Location
import pymysql
import random,time,re,os


def insert_data_to_sql(item):

    # 本地数据库
    # engine = create_engine("mysql+pymysql://root:root@localhost:3306/sudi_zf?charset=utf8", max_overflow=5,
    #                        encoding='utf-8')

    # 生产数据库
    engine = create_engine("mysql+pymysql://yunyudev:yuguodev@47.98.185.124:3306/sudi-zf?charset=utf8", max_overflow=5,
                           encoding='utf-8')
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    random_user_id = item['user_id']
    user = session.query(User).filter(User.id == random_user_id).first()
    location = session.query(Location).all()  # type:list
    open_id = user.openid
    location_id = 1

    info_location = item['location']  # type:str

    for location_item in location:  # type:Location
        info_location_split_list = info_location.split('&')
        for info_location_split_item in info_location_split_list:
            if info_location_split_item in location_item.name:
                location_id = location_item.id

    type = '2'
    status = '1'

    room_pulsh_time = item['room_pulsh_time']
    update_ts = room_pulsh_time
    create_ts = room_pulsh_time

    info = dict()
    split_str = item['room_type'].split('  ')
    split_str[0] = re.sub('室', '-', split_str[0])
    info['room_type'] = re.sub('厅', '-', split_str[0]).replace('卫', '')

    zulin_str = item['chuzu_type']

    if zulin_str == '整租':
        info['sale_type'] = '1'
    elif zulin_str == '合租':
        info['sale_type'] = '2'
    else:
        info['sale_type'] = '1'

    info['price'] = item['totalPrice']

    info['limit'] = '1'
    info['wechat'] = item['brokerPhone']  # 微信号写成电话
    info['desc'] = item['title']
    info['imgs'] = item['imgList']

    if random_user_id <= 222:
        print('管道文件输出 info:' + str(info) + 'random_user_id:' + str(
            random_user_id) + ' open_id:' + open_id + ' location_id:' + str(location_id)+'type:'+str(type)+'status:'+str(status)+'update_ts:'+str(update_ts))

        # 插入数据库
        userFormInfo = UserFormInfo(user_id=random_user_id, location_id=location_id, openid=open_id,
                                    rank='1',info=json.dumps(info), type=type, status=status, update_ts=update_ts,
                                    create_ts=create_ts)
        session.add(userFormInfo)
        session.commit()
        session.flush()

def get_random_proxy():
    '''随机从文件中读取proxy'''
    abs_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    while 1:
        with open(abs_path+'/lianjia/proxies.txt', 'r') as f:
            proxies = f.readlines()
        if proxies:
            break
        else:
            time.sleep(1)
    proxy = random.choice(proxies).strip()
    print("当前使用IP是：" + proxy)
    return proxy

def response_data():
    user_id = 110
    host = 'https://app.api.lianjia.com/Rentplat/v1/house/'
    # url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id=310000&condition=rt200600000002&offset=0&limit=30&scene=list' #合租
    url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id=310000&condition=rt200600000001'  # 整租
    url_phone = 'https://app.api.lianjia.com/Rentplat/v1/houses/'  # 电话


    for i in range(0, 5):
        # ip地址：端口号
        proxies = {'http': get_random_proxy()}

        response = requests.get(url=url + '&offset=' + str(i * 30) + '&limit=' + str(30 * (i + 1)),proxies=proxies,verify=False)
        lianjia_data = json.loads(response.text)
        lianjia_list = lianjia_data['data']['list']

        for lianjia in lianjia_list:

            proxies = {'http': get_random_proxy()}
            response_detail = requests.get(url=host + 'detail?house_code=' + lianjia['house_code'],proxies=proxies, verify=False)
            lianjia_details_dic = json.loads(response_detail.text)

            lianjiaItem = dict()
            user_id += 1
            if user_id > 222:
                exit()
            else:
                lianjia_base_info = lianjia_details_dic['data']['base_info']
                lianjiaItem['user_id'] = user_id

                # 标题
                lianjiaItem['title'] = lianjia_base_info['house_title']

                # 发布时间
                push_time = lianjia_base_info['meta_info'][0]['desc']
                try:
                    if push_time.find('天前') >= 0:
                        push_time = int(time.time()) - (int(push_time.replace('天前', '')) * 86400)
                    elif push_time.find('个月前') >= 0:
                        push_time = int(time.time()) - (int(push_time.replace('个月前', '')) * 30 * 86400)
                except:
                    push_time = int(time.time())
                lianjiaItem['room_pulsh_time'] = push_time+random.randint(60,43200)

                # 屋内图片
                lianjia_house_picture_list = lianjia_details_dic['data']['house_picture']
                imgDict = list()
                for lianjia_house_picture in lianjia_house_picture_list:
                    imgDict.append(lianjia_house_picture['house_picture_url'])
                lianjiaItem['imgList'] = imgDict
                lianjiaItem['totalPrice'] = lianjia_base_info['monthly_rent_price']
                if len(lianjia_details_dic['data']['location']['subway']) > 0:
                    lianjiaItem['location'] = lianjia_details_dic['data']['location']['subway'][0]['name']
                else:
                    lianjiaItem['location'] = ""
                lianjiaItem['room_type'] = lianjia_base_info['layout']
                lianjiaItem['chuzu_type'] = "整租"

                house_code = lianjia_details_dic['data']['base_info']['house_code']
                response_phone = requests.get(url=url_phone + 'brokers?house_codes=' + house_code + '&ucid=' +
                                                  lianjia_details_dic['data']['recommend_agents']['list'][0][
                                                      'agent_ucid'],proxies=proxies,verify=False)
                phone_dic = json.loads(response_phone.text)
                lianjiaItem['brokerPhone'] = phone_dic['data'][house_code][house_code]['tp_number']

                insert_data_to_sql(lianjiaItem)


if __name__ == '__main__':
    response_data()
    #get_random_proxy()




