from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(self, custom_resp: dict, status_code: int, detail: str = None):
        self.custom_resp = custom_resp
        super().__init__(status_code=status_code, detail=detail)
