from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  
  app_name: str = "airline-ops-assistant"
  log_level: str = "INFO"
  
  redis_host: str = 'localhost'
  redis_port: int = 6379
  redis_db: int = 0
  
  class Config:
    env_file = ".env"
    
settings = Settings()    
