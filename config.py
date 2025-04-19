import os

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 安全配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB上传限制
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # 任务配置
    SCAN_TIMEOUT = 300  # 5分钟超时
    MAX_CONCURRENT_TASKS = 5
    
    # 弱口令爆破配置
    BRUTEFORCE_THREADS = 4
    COMMON_USERNAMES = ['admin', 'root', 'user', 'test']
    COMMON_PASSWORDS = ['password', '123456', 'admin', 'root']
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
