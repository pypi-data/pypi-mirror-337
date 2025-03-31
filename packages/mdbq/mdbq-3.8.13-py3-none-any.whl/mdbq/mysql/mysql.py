# -*- coding:utf-8 -*-
import datetime
import re
import time
from functools import wraps
import warnings
import pymysql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
import logging
from mdbq.other import otk

warnings.filterwarnings('ignore')
"""
建表流程:
建表规范:
"""
logger = logging.getLogger(__name__)


def count_decimal_places(num_str):
    """ 计算小数位数, 允许科学计数法 """
    match = re.match(r'^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?$', str(num_str))
    if match:
        # 如果是科学计数法
        match = re.findall(r'(\d+)\.(\d+)[eE][-+]?(\d+)$', str(num_str))
        if match:
            if len(match[0]) == 3:
                if int(match[0][2]) < len(match[0][1]):
                    # count_int 清除整数部分开头的 0 并计算整数位数
                    count_int = len(re.sub('^0+', '', str(match[0][0]))) + int(match[0][2])
                    # 计算小数位数
                    count_float = len(match[0][1]) - int(match[0][2])
                    return count_int, count_float
        # 如果是普通小数
        match = re.findall(r'(\d+)\.(\d+)$', str(num_str))
        if match:
            count_int = len(re.sub('^0+', '', str(match[0][0])))
            count_float = len(match[0][1])
            return count_int, count_float  # 计算小数位数
    return 0, 0


class MysqlUpload:
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        if username == '' or password == '' or host == '' or port == 0:
            self.config = None
        else:
            self.config = {
                'host': self.host,
                'port': int(self.port),
                'user': self.username,
                'password': self.password,
                'charset': charset,  # utf8mb4 支持存储四字节的UTF-8字符集
                'cursorclass': pymysql.cursors.DictCursor,
            }
        self.filename = None

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    def keep_connect(self, _db_name, _config, max_try: int=10):
        attempts = 1
        while attempts <= max_try:
            try:
                connection = pymysql.connect(**_config)  # 连接数据库
                return connection
            except Exception as e:
                logger.error(f'{_db_name}: 连接失败，正在重试: {self.host}:{self.port}  {attempts}/{max_try} {e}')
                attempts += 1
                time.sleep(30)
        logger.error(f'{_db_name}: 连接失败，重试次数超限，当前设定次数: {max_try}')
        return None

    def cover_doc_dtypes(self, dict_data):
        """ 清理字典键值 并转换数据类型  """
        if not dict_data:
            logger.info(f'mysql.py -> MysqlUpload -> cover_dict_dtypes -> 传入的字典不能为空')
            return
        __res_dict = {}
        new_dict_data = {}
        for k, v in dict_data.items():
            k = str(k).lower()
            k = re.sub(r'[()\-，,$&~^、 （）\"\'“”=·/。》《><！!`]', '_', k, re.IGNORECASE)
            k = k.replace('）', '')
            k = re.sub(r'_{2,}', '_', k)
            k = re.sub(r'_+$', '', k)
            result1 = re.findall(r'编码|_?id|货号|款号|文件大小', k, re.IGNORECASE)
            result2 = re.findall(r'占比$|投产$|产出$|roi$|率$', k, re.IGNORECASE)
            result3 = re.findall(r'同比$|环比$', k, re.IGNORECASE)
            result4 = re.findall(r'花费$|消耗$|金额$', k, re.IGNORECASE)

            date_type = otk.is_valid_date(v)  # 判断日期时间
            int_num = otk.is_integer(v)  # 判断整数
            count_int, count_float = count_decimal_places(v)  # 判断小数，返回小数位数
            if result1:  # 京东sku/spu商品信息
                __res_dict.update({k: 'varchar(100)'})
            elif k == '日期':
                __res_dict.update({k: 'DATE'})
            elif k == '更新时间':
                __res_dict.update({k: 'TIMESTAMP'})
            elif result2:  # 小数
                __res_dict.update({k: 'decimal(10,4)'})
            elif date_type == 1:  # 纯日期
                __res_dict.update({k: 'DATE'})
            elif date_type == 2:  # 日期+时间
                __res_dict.update({k: 'DATETIME'})
            elif int_num:
                __res_dict.update({k: 'INT'})
            elif count_float > 0:
                if count_int + count_float > 10:
                    if count_float >= 6:
                        __res_dict.update({k: 'decimal(14,6)'})
                    else:
                        __res_dict.update({k: 'decimal(14,4)'})
                elif count_float >= 6:
                    __res_dict.update({k: 'decimal(14,6)'})
                elif count_float >= 4:
                    __res_dict.update({k: 'decimal(12,4)'})
                else:
                    __res_dict.update({k: 'decimal(10,2)'})
            else:
                __res_dict.update({k: 'varchar(255)'})
            new_dict_data.update({k: v})
        __res_dict.update({'数据主体': 'longblob'})
        return __res_dict, new_dict_data

    @try_except
    def doc_to_sql(self, db_name, table_name, dict_data, set_typ={}, remove_by_key=None, allow_not_null=False, filename=None, reset_id=False):
        """
        db_name:
        table_name:
        remove_by_key: 设置时先删除数据再插入，不设置则直接添加
        dict_data:
        set_typ:
        allow_not_null:
        filename:
        reset_id:
        """
        if not self.config:
            return
        if '数据主体' not in dict_data.keys():
            logger.info(f'dict_data 中"数据主体"键不能为空')
            return
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
            database_exists = cursor.fetchone()
            if not database_exists:
                # 如果数据库不存在，则新建
                sql = f"CREATE DATABASE `{db_name}` COLLATE utf8mb4_0900_ai_ci"
                cursor.execute(sql)
                connection.commit()
                logger.info(f"创建Database: {db_name}")

        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            # 1. 查询表, 不存在则创建一个空表
            sql = "SHOW TABLES LIKE %s;"  # 有特殊字符不需转义
            cursor.execute(sql, (table_name))
            if not cursor.fetchone():
                sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INT AUTO_INCREMENT PRIMARY KEY);"
                cursor.execute(sql)
                logger.info(f'创建 mysql 表: {table_name}')

            new_dict = {}
            [new_dict.update({k: v}) for k, v in dict_data.items() if k != '数据主体']
            # 清理列名中的非法字符
            dtypes, new_dict = self.cover_doc_dtypes(new_dict)
            if set_typ:
                # 更新自定义的列数据类型
                for k, v in dtypes.items():
                    # 确保传进来的 set_typ 键存在于实际的 df 列才 update
                    [dtypes.update({k: inside_v}) for inside_k, inside_v in set_typ.items() if k == inside_k]

            # 检查列
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;"
            cursor.execute(sql, (db_name, table_name))
            col_exist = [item['COLUMN_NAME'] for item in cursor.fetchall()]  # 已存在的所有列

            col_not_exist = [col for col in set_typ.keys() if col not in col_exist]  # 不存在的列
            # 不存在则新建列
            if col_not_exist:  # 数据表中不存在的列
                for col in col_not_exist:
                    #  创建列，需转义
                    if allow_not_null:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {set_typ[col]};"
                    else:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {set_typ[col]} NOT NULL;"
                    cursor.execute(sql)
                    logger.info(f"添加列: {col}({set_typ[col]})")  # 添加列并指定数据类型

                    if col == '日期':
                        sql = f"CREATE INDEX index_name ON `{table_name}`(`{col}`);"
                        logger.info(f"设置为索引: {col}({set_typ[col]})")
                        cursor.execute(sql)
            connection.commit()  # 提交事务

            if remove_by_key:
                # 删除数据
                se_key = ', '.join(remove_by_key)
                condition = []
                for up_col in remove_by_key:
                    condition += [f'`{up_col}` = "{dict_data[up_col]}"']
                condition = ' AND '.join(condition)
                sql = f"SELECT {se_key} FROM `{table_name}` WHERE {condition}"
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    sql = f'DELETE FROM `{table_name}` WHERE {condition};'
                    cursor.execute(sql)

            # 插入数据到数据库
            # 有数据格式错误问题，所以分开处理，将数据主体移到最后面用占位符
            logger.info(f'正在更新: mysql ({self.host}:{self.port}) {db_name}/{table_name} -> {filename}')
            if new_dict:
                cols = ', '.join(f"`{item}`" for item in new_dict.keys())  # 列名需要转义
                values = ', '.join([f'"{item}"' for item in new_dict.values()])  # 值要加引号
                cols = ', '.join([cols, '数据主体'])
                binary_data = dict_data['数据主体']
                sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({values}, %s)"
                cursor.execute(sql, binary_data)
            else:
                sql = f"""INSERT INTO `{table_name}` (数据主体) VALUES (%s);"""
                cursor.execute(sql, dict_data['数据主体'])

            if reset_id:
                pass
            connection.commit()

    @try_except
    def insert_many_dict(self, db_name, table_name, dict_data_list, icm_update=None, main_key=None, unique_main_key=None, index_length=100, set_typ=None, allow_not_null=False, cut_data=None):
        """
        插入字典数据
        dict_data： 字典
        main_key： 指定索引列, 通常用日期列，默认会设置日期为索引
        unique_main_key： 指定唯一索引列
        index_length: 索引长度
        icm_update: 增量更正，指定后 main_key 只用于检查/创建列，不能更新数据
        set_typ: {}
        allow_not_null: 创建允许插入空值的列，正常情况下不允许空值
        """
        if not self.config:
            return
        if icm_update:
            if main_key or unique_main_key:
                logger.info(f'icm_update/unique_main_key/unique_main_key 参数不能同时设定')
                return
        if not main_key:
            main_key = []
        if not unique_main_key:
            unique_main_key = []

        if not dict_data_list:
            logger.info(f'dict_data_list 不能为空 ')
            return
        dict_data = dict_data_list[0]
        if cut_data:
            if '日期' in dict_data.keys():
                try:
                    __y = pd.to_datetime(dict_data['日期']).strftime('%Y')
                    __y_m = pd.to_datetime(dict_data['日期']).strftime('%Y-%m')
                    if str(cut_data).lower() == 'year':
                        table_name = f'{table_name}_{__y}'
                    elif str(cut_data).lower() == 'month':
                        table_name = f'{table_name}_{__y_m}'
                    else:
                        logger.info(f'参数不正确，cut_data应为 year 或 month ')
                except Exception as e:
                    logger.error(f'{table_name} 将数据按年/月保存(cut_data)，但在转换日期时报错 -> {e}')

        # connection = pymysql.connect(**self.config)  # 连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
            database_exists = cursor.fetchone()
            if not database_exists:
                # 如果数据库不存在，则新建

                sql = f"CREATE DATABASE `{db_name}` COLLATE utf8mb4_0900_ai_ci"
                cursor.execute(sql)
                connection.commit()
                logger.info(f"创建Database: {db_name}")

        self.config.update({'database': db_name})  # 添加更新 config 字段
        # connection = pymysql.connect(**self.config)  # 重新连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            # 1. 查询表, 不存在则创建一个空表
            sql = "SHOW TABLES LIKE %s;"  # 有特殊字符不需转义
            cursor.execute(sql, (table_name))
            if not cursor.fetchone():
                sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INT AUTO_INCREMENT PRIMARY KEY);"
                cursor.execute(sql)
                logger.info(f'创建 mysql 表: {table_name}')

            # 根据 dict_data 的值添加指定的数据类型
            dtypes, dict_data = self.cover_dict_dtypes(dict_data=dict_data)  # {'店铺名称': 'varchar(100)',...}
            if set_typ:
                # 更新自定义的列数据类型
                for k, v in dtypes.items():
                    # 确保传进来的 set_typ 键存在于实际的 df 列才 update
                    [dtypes.update({k: inside_v}) for inside_k, inside_v in set_typ.items() if k == inside_k]

            # 检查列
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;"
            cursor.execute(sql, (db_name, table_name))
            col_exist = [item['COLUMN_NAME'] for item in cursor.fetchall()]  # 已存在的所有列
            col_not_exist = [col for col in dict_data.keys() if col not in col_exist]  # 不存在的列
            # 不存在则新建列
            if col_not_exist:  # 数据表中不存在的列
                for col in col_not_exist:
                    #  创建列，需转义
                    if allow_not_null:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]};"
                    else:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]} NOT NULL;"
                    # sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]} NOT NULL;"
                    # logger.info(sql)
                    cursor.execute(sql)
                    logger.info(f"添加列: {col}({dtypes[col]})")  # 添加列并指定数据类型

                    if col in main_key or col == '日期':
                        sql = f"CREATE INDEX index_name ON `{table_name}`(`{col}`);"
                        logger.info(f"设置为索引: {col}({dtypes[col]})")
                        cursor.execute(sql)
                    if col in unique_main_key:
                        if dtypes[col] == 'mediumtext':
                            sql = f"ALTER TABLE `{table_name}` ADD UNIQUE (`{col}`({index_length}))"
                        else:
                            sql = f"ALTER TABLE `{table_name}` ADD UNIQUE (`{col}`)"
                        cursor.execute(sql)
            connection.commit()  # 提交事务
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            # 处理插入的数据
            for dict_data in dict_data_list:
                # logger.info(dict_data)
                dtypes, dict_data = self.cover_dict_dtypes(dict_data=dict_data)  # {'店铺名称': 'varchar(100)',...}
                if icm_update:
                    """ 使用增量更新: 需确保 icm_update['主键'] 传进来的列组合是数据表中唯一，值不会发生变化且不会重复，否则可能产生覆盖 """
                    sql = 'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
                    cursor.execute(sql, (db_name, {table_name}))
                    columns = cursor.fetchall()
                    cols_exist = [col['COLUMN_NAME'] for col in columns]  # 数据表的所有列, 返回 list
                    update_col = [item for item in cols_exist if item not in icm_update and item != 'id']  # 除了主键外的其他列

                    # unique_keys 示例: `日期`, `余额`
                    unique_keys = ', '.join(f"`{item}`" for item in update_col)  # 列名需要转义
                    condition = []
                    for up_col in icm_update:
                        condition += [f'`{up_col}` = "{dict_data[up_col]}"']
                    condition = ' AND '.join(condition)  # condition值示例: `品销宝余额` = '2930.73' AND `短信剩余` = '67471'
                    sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE {condition}"
                    # logger.info(sql)
                    # sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE `创建时间` = '2014-09-19 14:32:33'"
                    cursor.execute(sql)
                    results = cursor.fetchall()  # results 是数据库取出的数据
                    if results:  # 有数据返回，再进行增量检查
                        for result in results:  # results 是数据库数据, dict_data 是传进来的数据
                            change_col = []  # 发生变化的列名
                            change_values = []  # 发生变化的数据
                            for col in update_col:
                                # 因为 mysql 里面有 decimal 数据类型，要移除末尾的 0 再做比较（df 默认将 5.00 小数截断为 5.0）
                                df_value = str(dict_data[col])
                                mysql_value = str(result[col])
                                if '.' in df_value:
                                    df_value = re.sub(r'0+$', '', df_value)
                                    df_value = re.sub(r'\.$', '', df_value)
                                if '.' in mysql_value:
                                    mysql_value = re.sub(r'0+$', '', mysql_value)
                                    mysql_value = re.sub(r'\.$', '', mysql_value)
                                if df_value != mysql_value:  # 传进来的数据和数据库比较, 有变化
                                    # logger.info(f'{dict_data['日期']}{dict_data['商品id']}{col} 列的值有变化，{str(dict_data[col])}  !=  {str(result[col])}')
                                    change_values += [f"`{col}` = \"{str(dict_data[col])}\""]
                                    change_col.append(col)
                            not_change_col = [item for item in update_col if item not in change_col]
                            # change_values 是 df 传进来且和数据库对比后，发生了变化的数据，值示例： [`品销宝余额` = '9999.0', `短信剩余` = '888']
                            if change_values:  # change_values 有数据返回，表示值需要更新
                                if not_change_col:
                                    not_change_values = [f'`{col}` = "{str(dict_data[col])}"' for col in not_change_col]
                                    not_change_values = ' AND '.join(
                                        not_change_values)  # 示例: `短信剩余` = '888' AND `test1` = '93'
                                    # logger.info(change_values, not_change_values)
                                    condition += f' AND {not_change_values}'  # 重新构建完整的查询条件，将未发生变化的列加进查询条件
                                change_values = ', '.join(f"{item}" for item in change_values)  # 注意这里 item 外面没有反引号
                                sql = "UPDATE `%s` SET %s WHERE %s" % (table_name, change_values, condition)
                                # logger.info(sql)
                                cursor.execute(sql)
                    else:  # 没有数据返回，则直接插入数据
                        # cols = ', '.join(f"`{item}`" for item in dict_data.keys())  # 列名需要转义
                        # # data.update({item: f"{data[item]}" for item in data.keys()})  # 全部值转字符, 不是必须的
                        # values = ', '.join([f'"{item}"' for item in dict_data.values()])  # 值要加引号
                        # sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({values});"
                        # cursor.execute(sql)

                        # 清理和验证列名
                        safe_columns = [f"`{escape_string(str(col))}`" for col in dict_data.keys()]
                        cols = ", ".join(safe_columns)
                        # 使用参数化查询
                        placeholders = ", ".join(["%s"] * len(dict_data))
                        sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders})"
                        # 转义值并作为参数传递
                        escaped_values = [escape_string(str(v)) if isinstance(v, str) else v for v in
                                          dict_data.values()]
                        cursor.execute(sql, tuple(escaped_values))

                    connection.commit()  # 提交数据库
                    continue

                # 构建 keys
                keys_data = ', '.join([f'`{str(item)}`' for item in dict_data.keys()])
                # 构建 values
                values_data = ', '.join(f'"{str(item)}"' for item in dict_data.values())
                # 构建其他键值，重复时要更新的其他键
                if main_key:
                    for col in main_key:
                        del dict_data[col]
                if unique_main_key:
                    for col in unique_main_key:
                        del dict_data[col]
                # 涉及列名务必使用反引号
                update_datas = ', '.join([f'`{k}` = VALUES(`{k}`)' for k, v in dict_data.items()])

                # 构建 sql
                sql = f"INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table_name, keys_data, values_data, update_datas)
                # logger.info(sql)
                cursor.execute(sql)
                connection.commit()  # 提交数据库
        connection.close()

    @try_except
    def dict_to_mysql(self, db_name, table_name, dict_data, icm_update=None, main_key=None, unique_main_key=None, index_length=100, set_typ=None, allow_not_null=False, cut_data=None):
        """
        插入字典数据
        dict_data： 字典
        main_key： 指定索引列, 通常用日期列，默认会设置日期为索引
        unique_main_key： 指定唯一索引列
        index_length: 索引长度
        icm_update: 增量更正，指定后 main_key 只用于检查/创建列，不能更新数据
        set_typ: {}
        allow_not_null: 创建允许插入空值的列，正常情况下不允许空值
        """
        if not self.config:
            return
        if icm_update:
            if main_key or unique_main_key:
                logger.info(f'icm_update/unique_main_key/unique_main_key 参数不能同时设定')
                return
        if not main_key:
            main_key = []
        if not unique_main_key:
            unique_main_key = []

        if cut_data:
            if '日期' in dict_data.keys():
                try:
                    __y = pd.to_datetime(dict_data['日期']).strftime('%Y')
                    __y_m = pd.to_datetime(dict_data['日期']).strftime('%Y-%m')
                    if str(cut_data).lower() == 'year':
                        table_name = f'{table_name}_{__y}'
                    elif str(cut_data).lower() == 'month':
                        table_name = f'{table_name}_{__y_m}'
                    else:
                        logger.info(f'参数不正确，cut_data应为 year 或 month ')
                except Exception as e:
                    logger.error(f'{table_name} 将数据按年/月保存(cut_data)，但在转换日期时报错 -> {e}')

        # connection = pymysql.connect(**self.config)  # 连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
            database_exists = cursor.fetchone()
            if not database_exists:
                # 如果数据库不存在，则新建
                sql = f"CREATE DATABASE `{db_name}` COLLATE utf8mb4_0900_ai_ci"
                cursor.execute(sql)
                connection.commit()
                logger.info(f"创建Database: {db_name}")

        self.config.update({'database': db_name})  # 添加更新 config 字段
        # connection = pymysql.connect(**self.config)  # 重新连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            # 1. 查询表, 不存在则创建一个空表
            sql = "SHOW TABLES LIKE %s;"  # 有特殊字符不需转义
            cursor.execute(sql, (table_name))
            if not cursor.fetchone():
                sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INT AUTO_INCREMENT PRIMARY KEY);"
                cursor.execute(sql)
                logger.info(f'创建 mysql 表: {table_name}')

            # 根据 dict_data 的值添加指定的数据类型
            dtypes, dict_data = self.cover_dict_dtypes(dict_data=dict_data)  # {'店铺名称': 'varchar(100)',...}
            if set_typ:
                # 更新自定义的列数据类型
                for k, v in dtypes.items():
                    # 确保传进来的 set_typ 键存在于实际的 df 列才 update
                    [dtypes.update({k: inside_v}) for inside_k, inside_v in set_typ.items() if k == inside_k]

            # 检查列
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;"
            cursor.execute(sql, (db_name, table_name))
            col_exist = [item['COLUMN_NAME'] for item in cursor.fetchall()]  # 已存在的所有列
            col_not_exist = [col for col in dict_data.keys() if col not in col_exist]  # 不存在的列
            # 不存在则新建列
            if col_not_exist:  # 数据表中不存在的列
                for col in col_not_exist:
                    #  创建列，需转义
                    if allow_not_null:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]};"
                    else:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]} NOT NULL;"
                    # sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]} NOT NULL;"
                    # logger.info(sql)
                    cursor.execute(sql)
                    logger.info(f"添加列: {col}({dtypes[col]})")  # 添加列并指定数据类型

                    if col in main_key or col == '日期':
                        sql = f"CREATE INDEX index_name ON `{table_name}`(`{col}`);"
                        logger.info(f"设置为索引: {col}({dtypes[col]})")
                        cursor.execute(sql)
                    if col in unique_main_key:
                        if dtypes[col] == 'mediumtext':
                            sql = f"ALTER TABLE `{table_name}` ADD UNIQUE (`{col}`({index_length}))"
                        else:
                            sql = f"ALTER TABLE `{table_name}` ADD UNIQUE (`{col}`)"
                        cursor.execute(sql)
            connection.commit()  # 提交事务
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            # 处理插入的数据
            if icm_update:
                """ 使用增量更新: 需确保 icm_update['主键'] 传进来的列组合是数据表中唯一，值不会发生变化且不会重复，否则可能产生覆盖 """
                sql = 'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
                cursor.execute(sql, (db_name, {table_name}))
                columns = cursor.fetchall()
                cols_exist = [col['COLUMN_NAME'] for col in columns]  # 数据表的所有列, 返回 list
                update_col = [item for item in cols_exist if item not in icm_update and item != 'id']  # 除了主键外的其他列

                # unique_keys 示例: `日期`, `余额`
                unique_keys = ', '.join(f"`{item}`" for item in update_col)  # 列名需要转义
                condition = []
                for up_col in icm_update:
                    condition += [f'`{up_col}` = "{dict_data[up_col]}"']
                condition = ' AND '.join(condition)  # condition值示例: `品销宝余额` = '2930.73' AND `短信剩余` = '67471'
                sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE {condition}"
                # logger.info(sql)
                # sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE `创建时间` = '2014-09-19 14:32:33'"
                cursor.execute(sql)
                results = cursor.fetchall()  # results 是数据库取出的数据
                if results:  # 有数据返回，再进行增量检查
                    for result in results:  # results 是数据库数据, dict_data 是传进来的数据
                        change_col = []  # 发生变化的列名
                        change_values = []  # 发生变化的数据
                        for col in update_col:
                            # 因为 mysql 里面有 decimal 数据类型，要移除末尾的 0 再做比较（df 默认将 5.00 小数截断为 5.0）
                            df_value = str(dict_data[col])
                            mysql_value = str(result[col])
                            if '.' in df_value:
                                df_value = re.sub(r'0+$', '', df_value)
                                df_value = re.sub(r'\.$', '', df_value)
                            if '.' in mysql_value:
                                mysql_value = re.sub(r'0+$', '', mysql_value)
                                mysql_value = re.sub(r'\.$', '', mysql_value)
                            if df_value != mysql_value:  # 传进来的数据和数据库比较, 有变化
                                # logger.info(f'{dict_data['日期']}{dict_data['商品id']}{col} 列的值有变化，{str(dict_data[col])}  !=  {str(result[col])}')
                                change_values += [f"`{col}` = \"{str(dict_data[col])}\""]
                                change_col.append(col)
                        not_change_col = [item for item in update_col if item not in change_col]
                        # change_values 是 df 传进来且和数据库对比后，发生了变化的数据，值示例： [`品销宝余额` = '9999.0', `短信剩余` = '888']
                        if change_values:  # change_values 有数据返回，表示值需要更新
                            if not_change_col:
                                not_change_values = [f'`{col}` = "{str(dict_data[col])}"' for col in not_change_col]
                                not_change_values = ' AND '.join(
                                    not_change_values)  # 示例: `短信剩余` = '888' AND `test1` = '93'
                                # logger.info(change_values, not_change_values)
                                condition += f' AND {not_change_values}'  # 重新构建完整的查询条件，将未发生变化的列加进查询条件
                            change_values = ', '.join(f"{item}" for item in change_values)  # 注意这里 item 外面没有反引号
                            sql = "UPDATE `%s` SET %s WHERE %s" % (table_name, change_values, condition)
                            # logger.info(sql)
                            cursor.execute(sql)
                else:  # 没有数据返回，则直接插入数据
                    # cols = ', '.join(f"`{item}`" for item in dict_data.keys())  # 列名需要转义
                    # # data.update({item: f"{data[item]}" for item in data.keys()})  # 全部值转字符, 不是必须的
                    # values = ', '.join([f'"{item}"' for item in dict_data.values()])  # 值要加引号
                    # sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({values});"
                    # cursor.execute(sql)

                    # 构建安全的INSERT语句
                    safe_keys = [f"`{escape_string(str(k))}`" for k in dict_data.keys()]
                    keys_data = ", ".join(safe_keys)
                    placeholders = ", ".join(["%s"] * len(dict_data))

                    # 使用参数化查询
                    sql = f"INSERT INTO `{table_name}` ({keys_data}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_datas}"
                    escaped_values = [escape_string(str(v)) if isinstance(v, str) else v for v in dict_data.values()]
                    cursor.execute(sql, tuple(escaped_values))

                connection.commit()  # 提交数据库
                connection.close()
                return

            # 构建 keys
            keys_data = ', '.join([f'`{str(item)}`' for item in dict_data.keys()])
            # 构建 values
            values_data = ', '.join(f'"{str(item)}"' for item in dict_data.values())
            # 构建其他键值，重复时要更新的其他键
            if main_key:
                for col in main_key:
                    del dict_data[col]
            if unique_main_key:
                for col in unique_main_key:
                    del dict_data[col]
            # 涉及列名务必使用反引号
            update_datas = ', '.join([f'`{k}` = VALUES(`{k}`)' for k, v in dict_data.items()])

            # 构建 sql
            sql = f"INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table_name, keys_data, values_data, update_datas)
            # logger.info(sql)
            cursor.execute(sql)
            connection.commit()  # 提交数据库
        connection.close()

    def cover_dict_dtypes(self, dict_data):
        """ 清理字典键值 并转换数据类型  """
        if not dict_data:
            logger.info(f'mysql.py -> MysqlUpload -> cover_dict_dtypes -> 传入的字典不能为空')
            return
        __res_dict = {}
        new_dict_data = {}
        for k, v in dict_data.items():
            k = str(k).lower()
            k = re.sub(r'[()\-，,$&~^、 （）\"\'“”=·/。》《><！!`]', '_', k, re.IGNORECASE)
            k = k.replace('）', '')
            k = re.sub(r'_{2,}', '_', k)
            k = re.sub(r'_+$', '', k)
            if str(v) == '':
                v = 0
            v = str(v)
            v = re.sub('^="|"$', '', v, re.I)
            v = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', str(v))  # 移除控制字符
            if re.findall(r'^[-+]?\d+\.?\d*%$', v):
                v = str(float(v.rstrip("%")) / 100)

            result1 = re.findall(r'编码|_?id|货号|款号|文件大小', k, re.IGNORECASE)
            result2 = re.findall(r'占比$|投产$|产出$|roi$|率$', k, re.IGNORECASE)
            result3 = re.findall(r'同比$|环比$', k, re.IGNORECASE)
            result4 = re.findall(r'花费$|消耗$|金额$', k, re.IGNORECASE)

            date_type = otk.is_valid_date(v)  # 判断日期时间
            int_num = otk.is_integer(v)  # 判断整数
            count_int, count_float = count_decimal_places(v)  # 判断小数，返回小数位数
            if result1:  # 京东sku/spu商品信息
                __res_dict.update({k: 'varchar(100)'})
            elif k == '日期':
                __res_dict.update({k: 'DATE'})
            elif k == '更新时间':
                __res_dict.update({k: 'TIMESTAMP'})
            elif result2:  # 小数
                __res_dict.update({k: 'decimal(10,4)'})
            elif date_type == 1:  # 纯日期
                __res_dict.update({k: 'DATE'})
            elif date_type == 2:  # 日期+时间
                __res_dict.update({k: 'DATETIME'})
            elif int_num:
                __res_dict.update({k: 'INT'})
            elif count_float > 0:
                if count_int + count_float > 10:
                    # if count_float > 5:
                    #     v = round(float(v), 4)
                    if count_float >= 6:
                        __res_dict.update({k: 'decimal(14,6)'})
                    else:
                        __res_dict.update({k: 'decimal(14,4)'})
                elif count_float >= 6:
                    __res_dict.update({k: 'decimal(14,6)'})
                elif count_float >= 4:
                    __res_dict.update({k: 'decimal(12,4)'})
                else:
                    __res_dict.update({k: 'decimal(10,2)'})
            else:
                __res_dict.update({k: 'varchar(255)'})
            new_dict_data.update({k: v})
        return __res_dict, new_dict_data

    def convert_df_dtypes(self, df: pd.DataFrame):
        """ 清理 df 的值和列名，并转换数据类型 """
        df = otk.cover_df(df=df)  # 清理 df 的值和列名
        [pd.to_numeric(df[col], errors='ignore') for col in df.columns.tolist()]
        dtypes = df.dtypes.to_dict()
        __res_dict = {}
        for k, v in dtypes.items():
            result1 = re.findall(r'编码|_?id|货号|款号|文件大小', k, re.IGNORECASE)
            result2 = re.findall(r'占比$|投产$|产出$|roi$|率$', k, re.IGNORECASE)
            result3 = re.findall(r'同比$|环比$', k, re.IGNORECASE)
            result4 = re.findall(r'花费$|消耗$|金额$', k, re.IGNORECASE)

            if result1:  # id/sku/spu商品信息
                __res_dict.update({k: 'varchar(50)'})
            elif result2:  # 小数
                __res_dict.update({k: 'decimal(10,4)'})
            elif result3:  # 小数
                __res_dict.update({k: 'decimal(12,4)'})
            elif result4:  # 小数
                __res_dict.update({k: 'decimal(12,2)'})
            elif k == '日期':
                __res_dict.update({k: 'date'})
            elif k == '更新时间':
                __res_dict.update({k: 'timestamp'})
            elif v == 'int64':
                __res_dict.update({k: 'int'})
            elif v == 'float64':
                __res_dict.update({k: 'decimal(10,4)'})
            elif v == 'bool':
                __res_dict.update({k: 'boolean'})
            elif v == 'datetime64[ns]':
                __res_dict.update({k: 'datetime'})
            else:
                __res_dict.update({k: 'varchar(255)'})
        return __res_dict, df

    @try_except
    def df_to_mysql(self, df, db_name, table_name, set_typ=None, icm_update=[], move_insert=False, df_sql=False, drop_duplicates=False,
                    filename=None, count=None, reset_id=False, allow_not_null=False, cut_data=None):
        """
        db_name: 数据库名
        table_name: 表名
        move_insert: 根据df 的日期，先移除数据库数据，再插入, df_sql, drop_duplicates, icm_update 都要设置为 False
        原则上只限于聚合数据使用，原始数据插入时不要设置

        df_sql: 这是一个临时参数, 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重，初创表大量上传数据的时候使用
        drop_duplicates: 值为 True 时检查重复数据再插入，反之直接上传，数据量大时会比较慢
        icm_update: 增量更新, 在聚合数据中使用，原始文件不要使用，设置此参数时需将 drop_duplicates 改为 False
                使用增量更新: 必须确保 icm_update 传进来的列必须是数据表中唯一主键，值不会发生变化，不会重复，否则可能产生错乱覆盖情况
        filename: 用来追踪处理进度，传这个参数是方便定位产生错误的文件
        allow_not_null: 创建允许插入空值的列，正常情况下不允许空值
        """
        if not self.config:
            return
        if icm_update:
            if move_insert or df_sql or drop_duplicates:
                logger.info(f'icm_update/move_insert/df_sql/drop_duplicates 参数不能同时设定')
                return
        if move_insert:
            if icm_update or df_sql or drop_duplicates:
                logger.info(f'icm_update/move_insert/df_sql/drop_duplicates 参数不能同时设定')
                return

        self.filename = filename
        if isinstance(df, pd.DataFrame):
            if len(df) == 0:
                logger.info(f'{db_name}: {table_name} 传入的 df 数据长度为0, {self.filename}')
                return
        else:
            logger.info(f'{db_name}: {table_name} 传入的 df 不是有效的 dataframe 结构, {self.filename}')
            return
        if not db_name or db_name == 'None':
            logger.info(f'{db_name} 不能为 None')
            return

        if cut_data:
            if '日期' in df.columns.tolist():
                try:
                    df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                    min_year = df['日期'].min(skipna=True).year
                    min_month = df['日期'].min(skipna=True).month
                    if 0 < int(min_month) < 10 and not str(min_month).startswith('0'):
                        min_month = f'0{min_month}'
                    if str(cut_data).lower() == 'year':
                        table_name = f'{table_name}_{min_year}'
                    elif str(cut_data).lower() == 'month':
                        table_name = f'{table_name}_{min_year}-{min_month}'
                    else:
                        logger.info(f'参数不正确，cut_data应为 year 或 month ')
                except Exception as e:
                    logger.error(f'{table_name} 将数据按年/月保存(cut_data)，但在转换日期时报错 -> {e}')
        # 清理 dataframe 非法值，并转换获取数据类型
        dtypes, df = self.convert_df_dtypes(df)
        if set_typ:
            # 更新自定义的列数据类型
            for k, v in dtypes.items():
                # 确保传进来的 set_typ 键存在于实际的 df 列才 update
                [dtypes.update({k: inside_v}) for inside_k, inside_v in set_typ.items() if k == inside_k]

        # connection = pymysql.connect(**self.config)  # 连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
            database_exists = cursor.fetchone()
            if not database_exists:
                # 如果数据库不存在，则新建
                sql = f"CREATE DATABASE `{db_name}` COLLATE utf8mb4_0900_ai_ci"
                cursor.execute(sql)
                connection.commit()
                logger.info(f"创建Database: {db_name}")

        self.config.update({'database': db_name})  # 添加更新 config 字段
        # connection = pymysql.connect(**self.config)  # 重新连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            # 1. 查询表, 不存在则创建一个空表
            sql = "SHOW TABLES LIKE %s;"  # 有特殊字符不需转义
            cursor.execute(sql, (table_name))
            if not cursor.fetchone():
                sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INT AUTO_INCREMENT PRIMARY KEY);"
                cursor.execute(sql)
                logger.info(f'创建 mysql 表: {table_name}')

            #  有特殊字符不需转义
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;"
            cursor.execute(sql, (db_name, table_name))
            col_exist = [item['COLUMN_NAME'] for item in cursor.fetchall()]
            cols = df.columns.tolist()
            col_not_exist = [col for col in cols if col not in col_exist]

            # 检查列，不存在则新建列
            if col_not_exist:  # 数据表中不存在的列
                for col in col_not_exist:
                    #  创建列，需转义
                    if allow_not_null:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]};"
                    else:
                        sql = f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` {dtypes[col]} NOT NULL;"
                    cursor.execute(sql)
                    logger.info(f"添加列: {col}({dtypes[col]})")  # 添加列并指定数据类型

                    # 创建索引
                    if col == '日期':
                        sql = f"SHOW INDEXES FROM `{table_name}` WHERE `Column_name` = %s"
                        cursor.execute(sql, (col))
                        result = cursor.fetchone()  # 检查索引是否存在
                        if not result:
                            cursor.execute(f"CREATE INDEX index_name ON `{table_name}`(`{col}`)")
            connection.commit()  # 提交事务

            if df_sql:
                logger.info(f'正在更新: mysql ({self.host}:{self.port}) {db_name}/{table_name}, {count}, {self.filename}')
                engine = create_engine(
                    f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{db_name}")  # 创建数据库引擎
                # df.to_csv('/Users/xigua/Downloads/mysql.csv', index=False, header=True, encoding='utf-8_sig')
                # df.to_excel('/Users/xigua/Downloads/mysql.xlsx', index=False, header=True, engine='openpyxl', freeze_panes=(1, 0))
                df.to_sql(
                    name=table_name,
                    con=engine,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
                if reset_id:
                    pass
                connection.commit()  # 提交事务
                connection.close()
                return

            # 5. 移除指定日期范围内的数据，原则上只限于聚合数据使用，原始数据插入时不要设置
            if move_insert and '日期' in df.columns.tolist():
                # 移除数据
                dates = df['日期'].values.tolist()
                # logger.info(dates)
                dates = [pd.to_datetime(item) for item in dates]  # 需要先转换类型才能用 min, max
                start_date = pd.to_datetime(min(dates)).strftime('%Y-%m-%d')
                end_date = (pd.to_datetime(max(dates)) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

                sql = f"DELETE FROM `{table_name}` WHERE {'日期'} BETWEEN '%s' AND '%s'" % (start_date, end_date)
                cursor.execute(sql)
                connection.commit()

                # 插入数据
                engine = create_engine(
                    f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{db_name}")  # 创建数据库引擎
                df.to_sql(
                    name=table_name,
                    con=engine,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
                return

            datas = df.to_dict(orient='records')
            for data in datas:
                # data 是传进来待处理的数据, 不是数据库数据
                # data 示例: {'日期': Timestamp('2024-08-27 00:00:00'), '推广费余额': 33299, '品销宝余额': 2930.73, '短信剩余': 67471}
                try:
                    cols = ', '.join(f"`{item}`" for item in data.keys())  # 列名需要转义
                    # data.update({item: f"{data[item]}" for item in data.keys()})  # 全部值转字符, 不是必须的
                    values = ', '.join([f'"{item}"' for item in data.values()])  # 值要加引号
                    condition = []
                    for k, v in data.items():
                        condition += [f'`{k}` = "{v}"']
                    condition = ' AND '.join(condition)  # 构建查询条件
                    # logger.info(condition)

                    if drop_duplicates:  # 查重插入
                        sql = "SELECT %s FROM %s WHERE %s" % (cols, table_name, condition)
                        # sql = f"SELECT {cols} FROM `{table_name}` WHERE `创建时间` = '2014-09-19 14:32:33'"
                        cursor.execute(sql)
                        result = cursor.fetchall()  # 获取查询结果, 有结果返回 list 表示数据已存在(不重复插入)，没有则返回空 tuple
                        # logger.info(result)
                        if not result:  # 数据不存在则插入
                            sql = f"INSERT INTO `{table_name}` ({cols}) VALUES (%s);" % (values)
                            # logger.info(sql)
                            cursor.execute(sql)
                        # else:
                        #     logger.info(f'重复数据不插入: {condition[:50]}...')
                    elif icm_update:  # 增量更新, 专门用于聚合数据，其他库不要调用
                        """ 使用增量更新: 需确保 icm_update['主键'] 传进来的列必须是数据表中唯一主键，值不会发生变化且不会重复，否则可能产生覆盖情况 """
                        sql = 'SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
                        cursor.execute(sql, (db_name, {table_name}))
                        columns = cursor.fetchall()
                        cols_exist = [col['COLUMN_NAME'] for col in columns]  # 数据表的所有列, 返回 list
                        update_col = [item for item in cols_exist if
                                      item not in icm_update and item != 'id']  # 除了主键外的其他列

                        # unique_keys 示例: `日期`, `余额`
                        unique_keys = ', '.join(f"`{item}`" for item in update_col)  # 列名需要转义
                        condition = []
                        for up_col in icm_update:
                            condition += [f'`{up_col}` = "{data[up_col]}"']
                        condition = ' AND '.join(condition)  # condition值示例: `品销宝余额` = '2930.73' AND `短信剩余` = '67471'
                        sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE {condition}"
                        # logger.info(sql)
                        # sql = f"SELECT {unique_keys} FROM `{table_name}` WHERE `创建时间` = '2014-09-19 14:32:33'"
                        cursor.execute(sql)
                        results = cursor.fetchall()  # results 是数据库取出的数据
                        if results:  # 有数据返回，再进行增量检查
                            for result in results:  # results 是数据库数据, data 是传进来的数据
                                change_col = []  # 发生变化的列名
                                change_values = []  # 发生变化的数据
                                for col in update_col:
                                    # 因为 mysql 里面有 decimal 数据类型，要移除末尾的 0 再做比较（df 默认将 5.00 小数截断为 5.0）
                                    df_value = str(data[col])
                                    mysql_value = str(result[col])
                                    if '.' in df_value:
                                        df_value = re.sub(r'0+$', '', df_value)
                                        df_value = re.sub(r'\.$', '', df_value)
                                    if '.' in mysql_value:
                                        mysql_value = re.sub(r'0+$', '', mysql_value)
                                        mysql_value = re.sub(r'\.$', '', mysql_value)
                                    if df_value != mysql_value:  # 传进来的数据和数据库比较, 有变化
                                        # logger.info(f'{data['日期']}{data['商品id']}{col} 列的值有变化，{str(data[col])}  !=  {str(result[col])}')
                                        change_values += [f"`{col}` = \"{str(data[col])}\""]
                                        change_col.append(col)
                                not_change_col = [item for item in update_col if item not in change_col]
                                # change_values 是 df 传进来且和数据库对比后，发生了变化的数据，值示例： [`品销宝余额` = '9999.0', `短信剩余` = '888']
                                if change_values:  # change_values 有数据返回，表示值需要更新
                                    if not_change_col:
                                        not_change_values = [f'`{col}` = "{str(data[col])}"' for col in not_change_col]
                                        not_change_values = ' AND '.join(
                                            not_change_values)  # 示例: `短信剩余` = '888' AND `test1` = '93'
                                        # logger.info(change_values, not_change_values)
                                        condition += f' AND {not_change_values}'  # 重新构建完整的查询条件，将未发生变化的列加进查询条件
                                    change_values = ', '.join(f"{item}" for item in change_values)  # 注意这里 item 外面没有反引号
                                    sql = "UPDATE `%s` SET %s WHERE %s" % (table_name, change_values, condition)
                                    # logger.info(sql)
                                    cursor.execute(sql)
                        else:  # 没有数据返回，则直接插入数据
                            sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({values});"
                            cursor.execute(sql)
                    else:
                        sql = f"INSERT INTO `{table_name}` ({cols}) VALUES (%s);" % (values)
                        cursor.execute(sql)
                except Exception as e:
                    pass

            if reset_id:
                pass
        connection.commit()  # 提交事务
        connection.close()

    @try_except
    def read_doc_data(self, table_name, db_name='pdf文件', column='文件名', filename=None, save_path='/Users/xigua/Downloads'):
        """
        db_name:
        table_name:
        column: 读取哪一列
        filename: 文件名称
        save_path: 保存位置
        """
        if not filename:
            logger.info(f'未指定文件名: filename')
            return
        # connection = pymysql.connect(**self.config)  # 连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        # try:
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
            database_exists = cursor.fetchone()
            if not database_exists:
                logger.info(f"Database {db_name} 数据库不存在")
                return
        self.config.update({'database': db_name})
        # connection = pymysql.connect(**self.config)  # 重新连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            # 1. 查询表
            sql = "SHOW TABLES LIKE %s;"  # 有特殊字符不需转义
            cursor.execute(sql, (table_name))
            if not cursor.fetchone():
                logger.info(f'{table_name} -> 数据表不存在')
                return

            # 读取数据
            condition = f'`{column}` = "{filename}"'
            sql = f"SELECT `{column}`, `数据主体` FROM `{table_name}` WHERE {condition}"
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                for result in results:
                    # 将二进制数据写入到文件
                    with open(os.path.join(save_path, filename), 'wb') as f:
                        f.write(result['数据主体'])
                        logger.info(f'写入本地文件: ({self.host}:{self.port}) {db_name}/{table_name} -> {os.path.join(save_path, filename)}')
        connection.close()

    def read_mysql(self, table_name, start_date, end_date, db_name='远程数据源', date_name='日期'):
        """ 读取指定数据表，可指定日期范围，返回结果: df """
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        df = pd.DataFrame()

        # connection = pymysql.connect(**self.config)  # 连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    logger.info(f"Database {db_name} 数据库不存在")
                    return df
                else:
                    logger.info(f'mysql 正在查询表: {table_name}, 范围: {start_date}~{end_date}')
        except:
            return df
        finally:
            connection.close()  # 断开连接

        before_time = time.time()
        # 读取数据
        self.config.update({'database': db_name})
        # connection = pymysql.connect(**self.config)  # 重新连接数据库
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        try:
            with connection.cursor() as cursor:
                # 获取指定日期范围的数据
                sql = f"SELECT * FROM `{db_name}`.`{table_name}` WHERE `{date_name}` BETWEEN '%s' AND '%s'" % (start_date, end_date)
                cursor.execute(sql)
                rows = cursor.fetchall()  # 获取查询结果
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(rows, columns=columns)  # 转为 df
        except Exception as e:
            logger.error(f'{e} {db_name} -> {table_name} 表不存在')
            return df
        finally:
            connection.close()

        if len(df) == 0:
            logger.info(f'database: {db_name}, table: {table_name} 查询的数据为空')
        else:
            cost_time = int(time.time() - before_time)
            if cost_time < 1:
                cost_time = round(time.time() - before_time, 2)
            logger.info(f'mysql ({self.host}) 表: {table_name} 获取数据长度: {len(df)}, 用时: {cost_time} 秒')
        return df

    def upload_pandas(self, update_path, db_name, days=None):
        """
        专门用来上传 pandas数据源的全部文件
        db_name: 数据库名: pandas数据源
        update_path: pandas数据源所在路径
        days: 更新近期数据，单位: 天, 不设置则全部更新
        """
        if days:
            today = datetime.date.today()
            start_date = pd.to_datetime(today - datetime.timedelta(days=days))
        else:
            start_date = pd.to_datetime('2000-01-01')

        root_files = os.listdir(update_path)
        for root_file in root_files:
            if '其他数据' in root_file or '年.csv' in root_file or '京东数据集' in root_file:
                continue  # 跳过的文件夹
            f_path = os.path.join(update_path, root_file)

            if os.path.isdir(f_path):
                for root, dirs, files in os.walk(f_path, topdown=False):
                    for name in files:
                        if name.endswith('.csv') and 'baidu' not in name:
                            df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                            if '日期' in df.columns.tolist():
                                df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else x)
                                df = df[df['日期'] >= start_date]
                            if len(df) == 0:
                                continue
                            self.df_to_mysql(df=df, db_name=db_name, table_name=root_file)
            elif os.path.isfile(f_path):
                if f_path.endswith('.csv') and 'baidu' not in f_path:
                    df = pd.read_csv(f_path, encoding='utf-8_sig', header=0, na_filter=False)
                    if '日期' not in df.columns.tolist():
                        df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else x)
                        df = df[df['日期'] >= start_date]
                    if len(df) == 0:
                        continue
                    table = f'{os.path.splitext(root_file)[0]}_f'  # 这里定义了文件表会加 _f 后缀
                    self.df_to_mysql(df=df, db_name=db_name, table_name=table)


class OptimizeDatas:
    """
    数据维护 删除 mysql 的冗余数据
    更新过程:
    1. 读取所有数据表
    2. 遍历表, 遍历列, 如果存在日期列则按天遍历所有日期, 不存在则全表读取
    3. 按天删除所有冗余数据(存在日期列时)
    tips: 查找冗余数据的方式是创建一个临时迭代器, 逐行读取数据并添加到迭代器, 出现重复时将重复数据的 id 添加到临时列表, 按列表 id 执行删除
    """
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port  # 默认端口, 此后可能更新，不作为必传参数
        self.charset = charset
        self.config = {
            'host': self.host,
            'port': int(self.port),
            'user': self.username,
            'password': self.password,
            'charset': self.charset,  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }
        self.db_name_lists: list = []  # 更新多个数据库 删除重复数据
        self.db_name = None
        self.days: int = 63  # 对近 N 天的数据进行排重
        self.end_date = None
        self.start_date = None
        self.connection = None

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    def keep_connect(self, _db_name, _config, max_try: int=10):
        attempts = 1
        while attempts <= max_try:
            try:
                connection = pymysql.connect(**_config)  # 连接数据库
                return connection
            except Exception as e:
                logger.error(f'{_db_name}连接失败，正在重试: {self.host}:{self.port}  {attempts}/{max_try} {e}')
                attempts += 1
                time.sleep(30)
        logger.error(f'{_db_name}: 连接失败，重试次数超限，当前设定次数: {max_try}')
        return None

    def optimize_list(self):
        """
        更新多个数据库 移除冗余数据
        需要设置 self.db_name_lists
        """
        if not self.db_name_lists:
            logger.info(f'尚未设置参数: self.db_name_lists')
            return
        for db_name in self.db_name_lists:
            self.db_name = db_name
            self.optimize()

    def optimize(self, except_key=['更新时间']):
        """ 更新一个数据库 移除冗余数据 """
        if not self.db_name:
            logger.info(f'尚未设置参数: self.db_name')
            return
        tables = self.table_list(db_name=self.db_name)
        if not tables:
            logger.info(f'{self.db_name} -> 数据表不存在')
            return

        # 日期初始化
        if not self.end_date:
            self.end_date = pd.to_datetime(datetime.datetime.today())
        else:
            self.end_date = pd.to_datetime(self.end_date)
        if self.days:
            self.start_date = pd.to_datetime(self.end_date - datetime.timedelta(days=self.days))
        if not self.start_date:
            self.start_date = self.end_date
        else:
            self.start_date = pd.to_datetime(self.start_date)
        start_date_before = self.start_date
        end_date_before = self.end_date

        logger.info(f'mysql({self.host}: {self.port}) {self.db_name} 数据库优化中(日期长度: {self.days} 天)...')
        for table_dict in tables:
            for key, table_name in table_dict.items():
                self.config.update({'database': self.db_name})  # 添加更新 config 字段
                self.connection = self.keep_connect(_db_name=self.db_name, _config=self.config, max_try=10)
                if not self.connection:
                    return
                with self.connection.cursor() as cursor:
                    sql = f"SELECT 1 FROM `{table_name}` LIMIT 1"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if not result:
                        logger.info(f'数据表: {table_name}, 数据长度为 0')
                        continue  # 检查数据表是否为空

                    cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")  # 查询数据表的列信息
                    columns = cursor.fetchall()
                    date_exist = False
                    for col in columns:  # 遍历列信息，检查是否存在类型为日期的列
                        if col['Field'] == '日期' and (col['Type'] == 'date' or col['Type'].startswith('datetime')):
                            date_exist = True
                            break
                    if date_exist:  # 存在日期列
                        sql_max = f"SELECT MAX(日期) AS max_date FROM `{table_name}`"
                        sql_min = f"SELECT MIN(日期) AS min_date FROM `{table_name}`"
                        cursor.execute(sql_max)
                        max_result = cursor.fetchone()
                        cursor.execute(sql_min)
                        min_result = cursor.fetchone()
                        # 匹配修改为合适的起始和结束日期
                        if self.start_date < pd.to_datetime(min_result['min_date']):
                            self.start_date = pd.to_datetime(min_result['min_date'])
                        if self.end_date > pd.to_datetime(max_result['max_date']):
                            self.end_date = pd.to_datetime(max_result['max_date'])
                        dates_list = self.day_list(start_date=self.start_date, end_date=self.end_date)
                        # dates_list 是日期列表
                        for date in dates_list:
                            self.delete_duplicate(table_name=table_name, date=date, except_key=except_key)
                        self.start_date = start_date_before  # 重置，不然日期错乱
                        self.end_date = end_date_before
                    else:  # 不存在日期列的情况
                        self.delete_duplicate2(table_name=table_name, except_key=except_key)
                self.connection.close()
        logger.info(f'mysql({self.host}: {self.port}) {self.db_name} 数据库优化完成!')

    def delete_duplicate(self, table_name, date, except_key=['更新时间']):
        datas = self.table_datas(db_name=self.db_name, table_name=str(table_name), date=date)
        if not datas:
            return
        duplicate_id = []  # 出现重复的 id
        all_datas = []  # 迭代器
        for data in datas:
            for e_key in except_key:
                if e_key in data.keys():  # 在检查重复数据时，不包含 更新时间 字段
                    del data[e_key]
            try:
                delete_id = data['id']
                del data['id']
                data = re.sub(r'\.0+\', ', '\', ', str(data))  # 统一移除小数点后面的 0
                if data in all_datas:  # 数据出现重复时
                    if delete_id:
                        duplicate_id.append(delete_id)  # 添加 id 到 duplicate_id
                        continue
                all_datas.append(data)  # 数据没有重复
            except Exception as e:
                logger.debug(f'{table_name} 函数: mysql - > OptimizeDatas -> delete_duplicate -> {e}')
        del all_datas

        if not duplicate_id:  # 如果没有重复数据，则跳过该数据表
            return

        try:
            with self.connection.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(duplicate_id))
                # 移除冗余数据
                sql = f"DELETE FROM `{table_name}` WHERE id IN ({placeholders})"
                cursor.execute(sql, duplicate_id)
                logger.debug(f"{table_name} -> {date.strftime('%Y-%m-%d')} before: {len(datas)}, remove: {cursor.rowcount}")
            self.connection.commit()  # 提交事务
        except Exception as e:
            logger.error(f'{self.db_name}/{table_name}, {e}')
            self.connection.rollback()  # 异常则回滚

    def delete_duplicate2(self, table_name, except_key=['更新时间']):
        with self.connection.cursor() as cursor:
            sql = f"SELECT * FROM `{table_name}`"  # 如果不包含日期列，则获取全部数据
            cursor.execute(sql)
            datas = cursor.fetchall()
        if not datas:
            return
        duplicate_id = []  # 出现重复的 id
        all_datas = []  # 迭代器
        for data in datas:
            for e_key in except_key:
                if e_key in data.keys():  # 在检查重复数据时，不包含 更新时间 字段
                    del data[e_key]
            delete_id = data['id']
            del data['id']
            data = re.sub(r'\.0+\', ', '\', ', str(data))  # 统一移除小数点后面的 0
            if data in all_datas:  # 数据出现重复时
                duplicate_id.append(delete_id)  # 添加 id 到 duplicate_id
                continue
            all_datas.append(data)  # 数据没有重复
        del all_datas

        if not duplicate_id:  # 如果没有重复数据，则跳过该数据表
            return

        try:
            with self.connection.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(duplicate_id))
                # 移除冗余数据
                sql = f"DELETE FROM `{table_name}` WHERE id IN ({placeholders})"
                cursor.execute(sql, duplicate_id)
                logger.info(f"{table_name} -> before: {len(datas)}, "
                      f"remove: {cursor.rowcount}")
            self.connection.commit()  # 提交事务
        except Exception as e:
            logger.error(f'{self.db_name}/{table_name}, {e}')
            self.connection.rollback()  # 异常则回滚

    def database_list(self):
        """ 获取所有数据库 """
        connection = self.keep_connect(_db_name=self.db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()  # 获取所有数据库的结果
        connection.close()
        return databases

    def table_list(self, db_name):
        """ 获取指定数据库的所有数据表 """
        connection = self.keep_connect(_db_name=self.db_name, _config=self.config, max_try=10)
        if not connection:
            return
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    logger.info(f'{db_name}: 数据表不存在!')
                    return
        except Exception as e:
            logger.error(f'002 {e}')
            return
        finally:
            connection.close()  # 断开连接

        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()  # 获取所有数据表
        connection.close()
        return tables

    def table_datas(self, db_name, table_name, date):
        """
        获取指定数据表的数据, 按天获取
        """
        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = self.keep_connect(_db_name=db_name, _config=self.config, max_try=10)
        if not connection:
            return
        try:
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM `{table_name}` WHERE {'日期'} BETWEEN '%s' AND '%s'" % (date, date)
                cursor.execute(sql)
                results = cursor.fetchall()
        except Exception as e:
            logger.error(f'001 {e}')
        finally:
            connection.close()
        return results

    def day_list(self, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        date_list = []
        while start_date <= end_date:
            date_list.append(pd.to_datetime(start_date.date()))
            start_date += datetime.timedelta(days=1)
        return date_list

    def rename_column(self):
        """ 批量修改数据库的列名 """
        """
        # for db_name in ['京东数据2', '推广数据2', '市场数据2', '生意参谋2', '生意经2', '属性设置2',]:
        #     s = OptimizeDatas(username=username, password=password, host=host, port=port)
        #     s.db_name = db_name
        #     s.rename_column()
        """
        tables = self.table_list(db_name=self.db_name)
        for table_dict in tables:
            for key, table_name in table_dict.items():
                self.config.update({'database': self.db_name})  # 添加更新 config 字段
                self.connection = self.keep_connect(_db_name=self.db_name, _config=self.config, max_try=10)
                if not self.connection:
                    return
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")  # 查询数据表的列信息
                    columns = cursor.fetchall()
                    columns = [{column['Field']: column['Type']} for column in columns]
                    for column in columns:
                        for key, value in column.items():
                            if key.endswith('_'):
                                new_name = re.sub(r'_+$', '', key)
                                sql = f"ALTER TABLE `{table_name}` CHANGE COLUMN {key} {new_name} {value}"
                                cursor.execute(sql)
                self.connection.commit()
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    pass
