import re
try:
    from hashlib import md5 as hash
except ImportError:
    # Compatibility with older versions of Python
    from md5 import new as hash

from django.conf import settings
from django.core.exceptions import SuspiciousOperation

class SignedCookiesMiddleware(object):
    regex = re.compile(r'(?:([0-9a-f]+):)?(.*)')
    def __init__(self, secret=settings.SECRET_KEY):
        self.secret = secret

    def get_digest(self, key, value):
        string = ':'.join([self.secret, key, value])
        return hash(string).hexdigest()

    def sign(self, key, unsigned_value):
        return '%s:%s' % (self.get_digest(key, unsigned_value), unsigned_value)

    def unsign(self, key, signed_value):
        signature, unsigned_value = self.regex.match(signed_value).groups()
        if not signature or self.get_digest(key, unsigned_value) != signature:
            raise SuspiciousOperation, "'%s' was not properly signed." % key
        return unsigned_value

    def process_request(self, request):
        for (key, signed_value) in request.COOKIES.items():
            try:
                request.COOKIES[key] = self.unsign(key, signed_value)
            except:
                # Invalid cookies should behave as if they were never sent
                del request.COOKIES[key]

    def process_response(self, request, response):
        for (key, morsel) in response.cookies.items():
            if morsel['max-age'] == 0:
                # Deleted cookies don't need to be signed
                continue
            response.set_cookie(key, self.sign(key, morsel.value),
                                max_age=morsel['max-age'],
                                expires=morsel['expires'],
                                path=morsel['path'],
                                domain=morsel['domain'],
                                secure=morsel['secure'])
        return response
