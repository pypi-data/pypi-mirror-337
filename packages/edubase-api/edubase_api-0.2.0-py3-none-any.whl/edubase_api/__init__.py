import requests
from typing import Optional

class EduBaseApi:
    __address: str = 'https://vc.shspu.ru/release/current/api'

    def __init__(self, apikey: str) -> None:
        self.apikey = apikey

    def testkey_userkey(self) -> dict:
        return self.__do_request__(api_part='testkey', api_command='userkey')

    def getinfo_employee(self, login: Optional[str] = None, options: Optional[list[str]]=None) -> dict:
        login = '*' if not login else login
        params: dict[str,str] = {'login': login, 'options': options}
        return self.__do_request__(api_part='getinfo', api_command='employee', params=params)

    def getinfo_users(self) -> dict:
        return self.__do_request__(api_part='getinfo', api_command='users')

    def getinfo_studlist(self, year: Optional[str] = None, attrs: str = '') -> dict:
        year = '*' if not year else year
        params: dict[str,str] = {'year': year, 'attrs': attrs}
        return self.__do_request__(api_part='getinfo', api_command='studlist', params=params)

    def getinfo_checkpwd(self, login:str, pwd:str) -> dict:
        params: dict[str,str] = {'login':login, 'pwd':pwd}
        return self.__do_request__(api_part='getinfo', api_command='checkpwd', params=params)

    def getinfo_empcheckpwd(self, login:str, pwd:str) -> dict:
        params: dict[str, str] = {'login': login, 'pwd': pwd}
        return self.__do_request__(api_part='getinfo', api_command='empcheckpwd', params=params)

    def getinfo_studcheckpwd(self, login:str, pwd:str) -> dict:
        params: dict[str, str] = {'login': login, 'pwd': pwd}
        return self.__do_request__(api_part='getinfo', api_command='studcheckpwd', params=params)

    def setinfo_empsetpwd(self, login:str, oldpwd:str, newpwd:str) -> dict:
        params: dict[str,str] = {'login': login, 'oldpwd': oldpwd, 'newpwd': newpwd}
        return self.__do_request__(api_part='setinfo', api_command='empsetpwd', params=params)

    def setinfo_studsetpwd(self, login:str, oldpwd:str, newpwd:str) -> dict:
        params: dict[str,str] = {'login': login, 'oldpwd': oldpwd, 'newpwd': newpwd}
        return self.__do_request__(api_part='setinfo', api_command='studsetpwd', params=params)

    def crypto_verifysig(self, file_src, file_sig) -> dict:
        params: dict = {'file_src': file_src, 'file_sig': file_sig}
        return self.__do_request__(api_part='crypto', api_command='verifysig', params=params)

    def __do_request__(self, api_part, api_command, params: Optional[dict[str:str]]=None) -> dict:
        if params is None:
            params = {'apikey': ''}
        url = f'{self.__address}/{api_part}/{api_command}'
        params['apikey'] = self.__apikey
        req = requests.request(method='post', url=url, params=params)
        if not req.ok:
            return req
        res = req.json()
        if res['error'] != 0:
            return res
        return res
