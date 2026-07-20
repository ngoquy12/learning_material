from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Elearning Content Factory API"
    API_V1_STR: str = "/api/v1"
    
    # MySQL Database Config
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "22121944"
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str = "elearning_agent_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    class Config:
        env_file = ".env" 
        extra = "ignore"

settings = Settings()
