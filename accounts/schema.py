from drf_spectacular.extensions import OpenApiAuthenticationExtension


class SignedTokenAuthenticationScheme(OpenApiAuthenticationExtension):

    target_class = 'accounts.authentication.SignedTokenAuthentication'

    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'SignedToken',
            'description': 'Enter the access_token returned by Login API (without Bearer prefix)',
        }