# Time & System
import os
import time
from time import sleep
import shutil
import os.path
import datetime
from requests import requests

# Selenium
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Adlib
from Adlib.api import *
from Adlib.utils import *
from Adlib.utils import *
from Adlib.logins import *
from Adlib.virtaus import *
from Adlib.funcoes import *
from Adlib.funcoes import *
from Adlib.virtaus import *
from Adlib.integracao import *
from Adlib.apiConferirRg import *
from Adlib.apiValid import *
from Adlib.utils import meses
from Adlib.integracao import integracaoVirtaus
from Adlib.apiConferirRg import *
from Adlib.apiValid import *
from Adlib.utils import meses
from Adlib.integracao import integracaoVirtaus
from Adlib.integracao import *

# Telegram Tokens
tokenImportarDoc = '1930575882:AAH0bP6m7k2XeV6fH3Q9l2Z5Q3Q'
chatIdImportarDoc = '-1001272680219'
 
from Adlib.api import EnumBanco, EnumProcesso, putStatusRobo, EnumStatus

__all__ = [
    "os", "shutil", "time", "datetime", "requests", 'sleep',
    "webdriver", "Chrome", "Service", "Keys", "ChromeDriverManager", "ActionChains", "WebDriverWait",'NoSuchElementException',
    "setupDriver", "esperarElemento", "esperarElementos", "clickCoordenada", "aguardarDownload", "selectOption",
    "loginBMG", "loginVirtaus", "loginDaycoval", "assumirSolicitacao", "FiltrosSolicitacao", "getNumeroSolicitacao",
    "putStatusRobo", "EnumStatus", "EnumProcesso", "EnumBanco",
    "integracaoVirtaus", "getCredenciais", "mensagemTelegram",
    "tokenImportarDoc", "chatIdImportarDoc", "meses", 'loginFacta','loginC6','loginBMG', 'loginDaycoval', 'loginBanrisul', 'loginOle',
    'BeautifulSoup',
     'obterToken', 'verificarFraude', 'enviarDocumentos', 'finalizarSolicitacao'
]