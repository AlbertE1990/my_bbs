from redis import Redis
import json
from random import sample,choice

# cache = Redis(host='127.0.0.1',port='6379')
#
# cache.set('username','albert',ex=30)

import enum
class GenderEnum(enum.Enum):
    MALE = 1
    FMALE = 2
    SECRET = 3
    UNKNOW = 4

print(GenderEnum(1))
print(GenderEnum['MALE'])
print(type(GenderEnum(1)))
email = 'yaho.1_q@yahoo.com'
login_email = 'mail.'+email.split('@')[-1]
print(login_email)



