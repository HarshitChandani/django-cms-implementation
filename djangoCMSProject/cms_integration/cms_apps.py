from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class AuthenticationAppHook(CMSApp):
    app_name = "authentication",
    name = "Authentication Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["authentication.urls"]


apphook_pool.register(AuthenticationAppHook)
