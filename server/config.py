import os
class Config(object):
    # MySQL Config
    MYSQL_HOST = 'swortect.mysql.rds.aliyuncs.com'
    MYSQL_PORT = 3306
    MYSQL_USER = 'swortect'
    MYSQL_PASSWD = '1q2w3e4r'
    MYSQL_DB = 'wordcloud'
    MYSQL_PRE = 'hz_'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4&connect_timeout=10'
    SQLALCHEMY_POOL_RECYCLE = 60
    SQLALCHEMY_POOL_SIZE=100
    SQLALCHEMY_MAX_OVERFLOW=20
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO=True
    DEBUG = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS=[
        {
            'id':'job1',
            'func':'app.blue.stock.get_data:set_stock_daily',
            'args':(),
            'trigger':'cron',
            'hour':15,
            'minute':35
        }
    ]
    # ZINC Config
    ZINC_USER='swortect'
    ZINC_PWD='123456'
    ZINC_HOST='http://121.41.62.96:4080'
    CACHE_TYPE='simple'
    # MONGODB Config
    MONGO_URI = 'mongodb://'+os.environ.get('MONGO_USER', 'swortect')+':'+os.environ.get('MONGO_PWD', '123456')+'@'+os.environ.get('MONGO_HOST', '121.41.62.96')+':'+os.environ.get('MONGO_PORT', '27017')+'/'+os.environ.get('MONGO_DB', 'stock')+'?authSource=admin'
