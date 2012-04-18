class TIMJAPIError(Exception):
    """
    Generic API errors. 
    """
    def __init__(self, message, headers):
        self.args = ('TIMJ API Error: %s' % message,)
        self.headers = headers