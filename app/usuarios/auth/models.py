from app.common.error_handling import LoginNotFound, ForbiddenError, EmptyMessage
from app.usuarios.models import Usuario
from app.validator.models import TokenBlacklist


class Login():

    status: str
    token: str
    account = None

    def __init__(self, status, token, account):
        self.status = status
        self.token = token
        self.account = account

    @classmethod
    def logout_method(self, jti: str):
        token = TokenBlacklist.filter_first(jti=jti)
        token.revoked = True
        token.update()
        raise EmptyMessage
    
    @classmethod
    def login_method(self, data: dict):
        try:
            username = data['username']
            password = data['password']
        except:
            raise LoginNotFound()
        user = Usuario.filter_first(username=username)
        if user and user.check_password(user.password, password):
            auth_token = TokenBlacklist.encode_auth_token_extended(user.id)
            if auth_token:
                login = Login(
                    status='Susses',
                    token=auth_token,
                    account=user
                )
            return login
        else:
            raise LoginNotFound()