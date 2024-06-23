

class Settings:
    API_V1_STR: str
    API_V2_STR: str
    ADMIN_STR: str
    BACKEND_CORS_ORIGINS: list

    def __init__(self):
        self.API_V1_STR: str = "/api/v1"
        self.API_V2_STR: str = "/api/v2"
        self.ADMIN_STR: str = "/api/admin"


settings = Settings()
