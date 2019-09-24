# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector as mc

class SanxinPipeline(object):
    def __init__(self):
        self.conn = mc.connect(user='root', password='123456', host='127.0.0.1', port='3306', database='scrapy',
                               use_unicode=True)  # 创建数据库连接
        self.cur = self.conn.cursor()  # 创建数据库游标

    # 关闭数据库资源
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        sql = 'insert into samsung values (%s, %s, %s, %s, %s, %s, %s)'
        value_tuple = (
        item['phone_name'], float(item['price']), item['battery_life'], item['running_memory'], item['body_color'], item['front_pixel'], item['post_pixel'])
        self.cur.execute(sql, value_tuple)
        self.conn.commit()



