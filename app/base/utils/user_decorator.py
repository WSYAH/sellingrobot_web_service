import traceback
from bson import ObjectId
from fastapi import Header, Request

from app.base.utils import logger
from app.base.utils.base_utils import err_response
from app.base.utils.redis_utils import get_redis_data
from exceptions import CustomHTTPException
from app.base.utils.form_regex_utils import FormRegexUtils

# def validate_user_token_permission(request: Request,
#                                          token: str = Header(..., convert_underscores=True,
#                                                              regex=FormRegexUtils.token)):
#     """
#     依赖注入根据token对普通用户进行身份认证和权限认证
#     :param url: 请求路径
#     :param model_name: 模块名
#     :param parser:
#     :return:
#     """
#     url = request.url.path
#     user = get_redis_data(key=token)
#     if user is None:
#         raise CustomHTTPException(err_response('您已下线，请重新登录！'), 200)
#     user = eval(user)
#     url_list = user['user_permission']['url_list']
#     if url not in url_list:
#         raise CustomHTTPException(err_response('无访问权限'), 200)


def validate_user_token_permission(request: Request):
    """
    先将该方法注释掉，如果以后用到token验证将注释打开切换即可
    """
    pass

def validate_user_token(token: str = Header(..., convert_underscores=True, regex=FormRegexUtils.token)):
    """
    依赖注入根据token对普通用户进行身份认证
    :param parser:
    :return:
    """
    user = get_redis_data(key=token)
    if user is None:
        raise CustomHTTPException(err_response('您已下线，请重新登录！'), 200)
    return token



def validate_admin_token(token: str = Header(..., convert_underscores=True, regex=FormRegexUtils.token)):
    """
    对被装饰的方法根据token对管理者进行身份认证
    :param parser:
    :return:
    """

    user = get_redis_data(key=token)
    if user is None:
        raise CustomHTTPException(err_response('您已下线，请重新登录！'), 200)
    user = eval(user)
    if user.get('role') != 'admin':
        raise CustomHTTPException(err_response('该用户无操作权限'), 200)



def validate_common_error(modle_logger):
    """
    对接口进行统一异常处理
    :param modle_logger: 模块日志logger
    :return:
    """
    pass
    # try:
    #     return function(*args, **kw)
    # except Exception:
    #     modle_logger.error(traceback.format_exc())
    #     return err_response()
