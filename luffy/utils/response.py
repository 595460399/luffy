from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=100, msg='成功', http_status=None, headers=None, exception=False, **kwargs):
        data = {
            'code': code,
            'msg': msg,
        }
        if kwargs:
            data.update(kwargs)
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)


