import requests
from urllib3.util.retry import Retry
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter

from anylearn.config import AnylearnConfig


url_base = lambda :AnylearnConfig.cluster_address + '/api'


class RequestRetrySession(object):
    def __init__(
        self,
        retries=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE"],
        session=None,
    ):
        self.session = session or requests.session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def raise_for_status(res: requests.Response):
    http_error_msg = ''
    if isinstance(res.reason, bytes):
        try:
            reason = res.reason.decode('utf-8')
        except UnicodeDecodeError:
            reason = res.reason.decode('iso-8859-1')
    else:
        reason = res.reason
    
    if isinstance(res.content, bytes):
        try:
            content = res.content.decode('utf-8')
        except UnicodeDecodeError:
            content = res.content.decode('iso-8859-1')
    else:
        content = res.content

    if 400 <= res.status_code < 500:
        http_error_msg = u'%s: "%s" for url: %s' % (res.status_code, content, res.url)

    elif 500 <= res.status_code < 600:
        http_error_msg = u'%s: "%s" for url: %s' % (res.status_code, reason, res.url)

    if http_error_msg:
        raise HTTPError(http_error_msg, response=res)


def __request(method, *args, **kwargs):
    retries = kwargs.get('retries', 3)
    kwargs.pop('retries', None)
    with RequestRetrySession(retries=retries) as sess:
        res = sess.request(method, *args, **kwargs)
        raise_for_status(res)
        res.encoding = "utf-8"
        return res.json()


def __request_with_token(method, *args, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Authorization'] = "Bearer %s" % AnylearnConfig.token
    try:
        return __request(method, *args, **kwargs)
    except HTTPError as e:
        if e.response.status_code == 401 and AnylearnConfig.refresh_token:
            AnylearnConfig.cluster_relogin_by_token()
            return __request_with_token(method, *args, **kwargs)
        else:
            raise


def __request_with_secret_key(method, *args, secret_key, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Secret-Key'] = secret_key
    return __request(method, *args, **kwargs)


def get_with_token(*args, **kwargs):
    return __request_with_token('GET', *args, **kwargs)


def post_with_token(*args, **kwargs):
    return __request_with_token('POST', *args, **kwargs)


def post_with_secret_key(*args, secret_key, **kwargs):
    return __request_with_secret_key('POST', *args, secret_key=secret_key, **kwargs)


def delete_with_token(*args, **kwargs):
    return __request_with_token('DELETE', *args, **kwargs)


def put_with_token(*args, **kwargs):
    return __request_with_token('PUT', *args, **kwargs)


def patch_with_token(*args, **kwargs):
    return __request_with_token('PATCH', *args, **kwargs)
