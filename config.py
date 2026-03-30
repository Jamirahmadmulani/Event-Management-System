class Config:
    SECRET_KEY = "secretkey123"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/event_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False