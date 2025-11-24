class ServiceException(Exception):
    def __init__(self, *args, status_code=500):
        self.status_code = status_code
        super().__init__(*args)