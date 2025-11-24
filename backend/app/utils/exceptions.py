class JWTException(Exception):
    pass

class AbsenceJWTExc(JWTException):
    pass

class AbsenceAccessJWTExc(AbsenceJWTExc):
    pass

class AbsenceRefreshJWTExc(AbsenceJWTExc):
    pass

class TimeExpireJWTExc(JWTException):
    pass

class TimeExpireAccessJWTExc(JWTException):
    pass

class TimeExpireRefreshJWTExc(JWTException):
    pass

class AbsenceUserFromJWTExc(JWTException):
    pass