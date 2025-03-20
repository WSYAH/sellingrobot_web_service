"""监控中心"""
import os
from fastapi import APIRouter
# 注意修改文件夹地址
from app.base import project_name
from config.config import all_data


def get_current_folder():
    current_file_name = os.path.abspath(os.path.realpath(__file__))
    current_dir_name = os.path.dirname(os.path.realpath(__file__))

    interface_class = current_dir_name.split(current_file_name[len(current_dir_name):][0])[-1]
    return interface_class


dir_name = get_current_folder()
router = APIRouter(prefix=f"/{dir_name}")
namespace = [project_name + ' -> ' + dir_name]
from app.base.utils.my_log import get_logger

logger = get_logger('llm')