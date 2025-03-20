import os


def get_current_folder():
    current_file_name = os.path.abspath(os.path.realpath(__file__))
    current_dir_name = os.path.dirname(os.path.realpath(__file__))

    db_name = current_dir_name.split(current_file_name[len(current_dir_name):][0])[-1]
    return db_name


project_name = get_current_folder()

"""
此文件记录config.yaml公共变量，某一项目的config.yaml在对应项目目录中赋予变量
"""
import pymongo

from config.config import all_data, version

project_version = version.split("_")[-1]

target_data = all_data
data = all_data['version_config']

# mongo 配置
mongodb_ip = data.get('mongodb')['mongo_ip']
mongodb_user = data.get('mongodb')['username']
mongodb_pwd = data.get('mongodb')['password']
mongodb_port = data.get('mongodb')['port']
db_name = data.get('mongodb')['table']
auth = data.get('mongodb')['auth']
myclient = pymongo.MongoClient(f"mongodb://{mongodb_user}:{mongodb_pwd}@{mongodb_ip}:{mongodb_port}/?authSource={auth}"
                               f"&readPreference=primary&appname=MongoDB%20Compass&ssl=false", connect=False)
mydb = myclient[db_name]
# mongo collections
TEST_TABLE = data.get('mongodb')['tb_paramter']


