import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI =  "postgresql://postgres:Redl!ne36@192.168.72.1:5432/postgres"
    SQLALCHEMY_DATABASE_URI  = "postgresql://zqlwtpzposzmkg:110afc1b73f60388597a6059e2d67456e12dfcf16d843da5bb23d1383d780f15@ec2-44-198-82-71.compute-1.amazonaws.com:5432/d6hq85hpvlc5es"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
