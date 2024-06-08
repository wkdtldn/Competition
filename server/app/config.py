class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/your_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True