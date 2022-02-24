from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from . import settings
from utils.logging import logger


def send_sms(phone, code, exp=2):
    ssender = SmsSingleSender(settings.APP_ID, settings.APP_KEY)
    params = [code, exp]
    try:
        result = ssender.send_with_param(86, phone, settings.TEMPLATE_ID, params, sign=settings.SMS_SIGN, extend="",
                                         ext="")
        if result['result'] == 0:
            return True
        else:
            logger.error('发送短信失败，失败原因为：%s' % result['errmsg'])
            return False
    except Exception as e:
        logger.error('发送短信失败，失败原因为：%s' % str(e))
        return False
