from redis import Redis

cache = Redis(host='127.0.0.1',port='6379')

cache.set('username','albert',ex=30)