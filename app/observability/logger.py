import logging
from app.core.config import settings

logging.basicConfig(
  level= getattr(logging, settings.log_level.upper()),
  format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
  force= True
)

logger = logging.getLogger(settings.app_name)
logger.setLevel(getattr(logging, settings.log_level.upper()))