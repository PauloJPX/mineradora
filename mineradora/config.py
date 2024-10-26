#    SECRET_KEY = 'sua_chave_secreta'
#    MYSQL_HOST = 'localhost'
#    MYSQL_USER = 'root'
#    MYSQL_PASSWORD = '@J2ptpaulo@'
#    MYSQL_DB = 'mineradora'


import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '@J2ptpaulo@')
    MYSQL_DB = os.getenv('MYSQL_DB', 'mineradora')
