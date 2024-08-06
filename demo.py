from Mental_Health.logger import logging
from Mental_Health.exception import MentalHealthException
import sys



try:
    a=2/0
except Exception as e:
    raise MentalHealthException(e,sys)