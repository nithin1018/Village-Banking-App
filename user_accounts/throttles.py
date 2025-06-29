from rest_framework.throttling import SimpleRateThrottle

class OTPThrottle(SimpleRateThrottle):
    scope = 'otp'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return f'otp_throttle_user_{request.user.pk}'
        return self.get_ident(request)

class TransactionThrottle(SimpleRateThrottle):
    scope = 'transaction'
    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f'transaction_throttle_user_{request.user.pk}'
        return None