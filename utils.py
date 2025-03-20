
import os
import re
import tiktoken
from config import *
import json
from cachetools import LRUCache, cached
from ruamel.yaml import YAML



# 确保一个进程只有一个类的实例，避免造成重复连接，比如conn这一类的类，避免重复连接数据库
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]

    return _singleton


def rmSpace(txt):
    txt = re.sub(r"([^a-z0-9.,\)>]) +([^ ])", r"\1\2", txt, flags=re.IGNORECASE)
    return re.sub(r"([^ ]) +([^a-z0-9.,\(<])", r"\1\2", txt, flags=re.IGNORECASE)


def findMaxDt(fnm):
    m = "1970-01-01 00:00:00"
    try:
        with open(fnm, "r") as f:
            while True:
                l = f.readline()
                if not l:
                    break
                l = l.strip("\n")
                if l == 'nan':
                    continue
                if l > m:
                    m = l
    except Exception as e:
        pass
    return m

  
def findMaxTm(fnm):
    m = 0
    try:
        with open(fnm, "r") as f:
            while True:
                l = f.readline()
                if not l:
                    break
                l = l.strip("\n")
                if l == 'nan':
                    continue
                if int(l) > m:
                    m = int(l)
    except Exception as e:
        pass
    return m


encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    try:
        return len(encoder.encode(string))
    except Exception:
        return 0


def truncate(string: str, max_len: int) -> str:
    """Returns truncated text if the length of text exceed max_len."""
    return encoder.decode(encoder.encode(string)[:max_len])


def is_english(texts):
    eng = 0
    if not texts: return False
    for t in texts:
        if re.match(r"[ `a-zA-Z.,':;/\"?<>!\(\)-]", t.strip()):
            eng += 1
    if eng / len(texts) > 0.8:
        return True
    return False


# 自己创建一个缓存目录
def get_home_cache_dir():
    dir = os.path.join(os.path.expanduser("~"),CACHE_NAME)
    try:
        os.mkdir(dir)
    except OSError as error:
        pass
    return dir

'''获取项目根目录，当前当然是我自己配置的根目录'''
def get_project_base_directory(*args):
    if args:
        return os.path.join(PROJECT_BASE_DIR, *args)
    
    return PROJECT_BASE_DIR

'''这一部分是用来加载json、yaml;配置文件的'''
if True:
    '''这一部分是用来加载json、yaml;配置文件的'''
    @cached(cache=LRUCache(maxsize=10))
    def load_json_conf(conf_path):
        if os.path.isabs(conf_path):
            json_conf_path = conf_path
        else:
            json_conf_path = os.path.join(get_project_base_directory(), conf_path)
        try:
            with open(json_conf_path) as f:
                return json.load(f)
        except BaseException:
            raise EnvironmentError(
                "loading json file config from '{}' failed!".format(json_conf_path)
            )


    def dump_json_conf(config_data, conf_path):
        if os.path.isabs(conf_path):
            json_conf_path = conf_path
        else:
            json_conf_path = os.path.join(get_project_base_directory(), conf_path)
        try:
            with open(json_conf_path, "w") as f:
                json.dump(config_data, f, indent=4)
        except BaseException:
            raise EnvironmentError(
                "loading json file config from '{}' failed!".format(json_conf_path)
            )


    def load_json_conf_real_time(conf_path):
        if os.path.isabs(conf_path):
            json_conf_path = conf_path
        else:
            json_conf_path = os.path.join(get_project_base_directory(), conf_path)
        try:
            with open(json_conf_path) as f:
                return json.load(f)
        except BaseException:
            raise EnvironmentError(
                "loading json file config from '{}' failed!".format(json_conf_path)
            )


    def load_yaml_conf(conf_path):
        if not os.path.isabs(conf_path):
            conf_path = os.path.join(get_project_base_directory(), conf_path)
        try:
            with open(conf_path) as f:
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)
        except Exception as e:
            raise EnvironmentError(
                "loading yaml file config from {} failed:".format(conf_path), e
            )


    def rewrite_yaml_conf(conf_path, config):
        if not os.path.isabs(conf_path):
            conf_path = os.path.join(get_project_base_directory(), conf_path)
        try:
            with open(conf_path, "w") as f:
                yaml = YAML(typ="safe")
                yaml.dump(config, f)
        except Exception as e:
            raise EnvironmentError(
                "rewrite yaml file config {} failed:".format(conf_path), e
            )


    def rewrite_json_file(filepath, json_data):
        with open(filepath, "w") as f:
            json.dump(json_data, f, indent=4, separators=(",", ": "))
        f.close()


    