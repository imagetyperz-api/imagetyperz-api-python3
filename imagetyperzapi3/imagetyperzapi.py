# Imagetyperz captcha API
# -----------------------
# requests lib
try:
    from requests import session
except:
    raise Exception('requests package not installed, try with: \'pip install requests\'')

import os, json
from base64 import b64encode
from urllib.parse import urlencode
from json import loads as json_loads

# endpoints
# -------------------------------------------------------------------------------------------
CAPTCHA_ENDPOINT = 'http://captchatypers.com/Forms/UploadFileAndGetTextNEW.ashx'
RECAPTCHA_SUBMIT_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadRecaptchaV1.ashx'
RECAPTCHA_ENTERPRISE_SUBMIT_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadRecaptchaEnt.ashx'
RECAPTCHA_RETRIEVE_ENDPOINT = 'http://captchatypers.com/captchaapi/GetRecaptchaText.ashx'
BALANCE_ENDPOINT = 'http://captchatypers.com/Forms/RequestBalance.ashx'
BAD_IMAGE_ENDPOINT = 'http://captchatypers.com/Forms/SetBadImage.ashx'
GEETEST_SUBMIT_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadGeeTest.ashx'
GEETEST_V4_SUBMIT_ENDPOINT = 'http://www.captchatypers.com/captchaapi/UploadGeeTestV4.ashx'
GEETEST_RETRIEVE_ENDPOINT = 'http://captchatypers.com/captchaapi/getrecaptchatext.ashx'
HCAPTCHA_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadHCaptchaUser.ashx'
CAPY_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadCapyCaptchaUser.ashx'
TIKTOK_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadTikTokCaptchaUser.ashx'
FUNCAPTCHA_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadFunCaptcha.ashx'
RETRIEVE_JSON_ENDPOINT = 'http://captchatypers.com/captchaapi/GetCaptchaResponseJson.ashx'
TASK_ENDPOINT = 'http://captchatypers.com/captchaapi/UploadCaptchaTask.ashx'
TASK_PUSH_ENDPOINT = 'http://captchatypers.com/CaptchaAPI/SaveCaptchaPush.ashx'

CAPTCHA_ENDPOINT_CONTENT_TOKEN = 'http://captchatypers.com/Forms/UploadFileAndGetTextNEWToken.ashx'
CAPTCHA_ENDPOINT_URL_TOKEN = 'http://captchatypers.com/Forms/FileUploadAndGetTextCaptchaURLToken.ashx'
RECAPTCHA_SUBMIT_ENDPOINT_TOKEN = 'http://captchatypers.com/captchaapi/UploadRecaptchaToken.ashx'
RECAPTCHA_RETRIEVE_ENDPOINT_TOKEN = 'http://captchatypers.com/captchaapi/GetRecaptchaTextToken.ashx'
BALANCE_ENDPOINT_TOKEN = 'http://captchatypers.com/Forms/RequestBalanceToken.ashx'
BAD_IMAGE_ENDPOINT_TOKEN = 'http://captchatypers.com/Forms/SetBadImageToken.ashx'
GEETEST_SUBMIT_ENDPOINT_TOKEN = 'http://captchatypers.com/captchaapi/UploadGeeTestToken.ashx'

# user agent used in requests
# ---------------------------
USER_AGENT = 'pythonAPI1.0'


# API class
# -----------------------------------------
class ImageTyperzAPI:
    def __init__(self, access_token, affiliate_id = 0, timeout = 120):
        self._access_token = access_token
        self._affiliate_id = affiliate_id

        # empty by default
        self._username = ''
        self._password = ''

        self._timeout = timeout
        self._session = session()       # init a new session

        self._headers = {               # use this user agent
            'User-Agent' : USER_AGENT
        }

    # set username and password
    def set_user_password(self, username, password):
        self._username = username
        self._password = password

    # solve normal captcha
    def submit_image(self, image_path, is_case_sensitive = False, is_math = False, is_phrase = False, digits_only = False, letters_only = False, min_length = 0, max_length = 0):
        data = {}
        # if username is given, do it with user otherwise token
        if self._username:
            data['username'] = self._username
            data['password'] = self._password
            url = CAPTCHA_ENDPOINT
            if not os.path.exists(image_path): raise Exception('captcha image does not exist: {}'.format(image_path))
            # read image/captcha
            with open(image_path, 'rb') as f:
                image_data = b64encode(f.read())
        else:
            if image_path.lower().startswith('http'):
                url = CAPTCHA_ENDPOINT_URL_TOKEN
                image_data = image_path
            else:
                url = CAPTCHA_ENDPOINT_CONTENT_TOKEN
                # check if image/file exists
                if not os.path.exists(image_path): raise Exception('captcha image does not exist: {}'.format(image_path))

                # read image/captcha
                with open(image_path, 'rb') as f:
                    image_data = b64encode(f.read())
            # set token
            data['token'] = self._access_token

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['iscase'] = 'true' if is_case_sensitive else None
        data['isphrase'] = 'true' if is_phrase else None
        data['ismath'] = 'true' if is_math else None

        # digits, letters, or both
        if digits_only: data['alphanumeric'] = '1'
        elif letters_only: data['alphanumeric'] = '2'

        # min, max length
        if min_length != 0: data['minlength'] = min_length
        if max_length != 0: data['maxlength'] = max_length

        data['file'] = image_data

        if self._affiliate_id: data['affiliateid'] = self._affiliate_id

        # make request with all data
        response = self._session.post(url, data=data,
                                      headers=self._headers,
                                      timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[0].strip())  # raise Ex
        return response_text.split('|')[0]

    # submit recaptcha to system
    def submit_recaptcha(self, d):
        page_url = d['page_url']
        sitekey = d['sitekey']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']       # if proxy, add it

        # check if page_url and sitekey are != None
        if not page_url: raise Exception('provide a valid page_url')
        if not sitekey: raise Exception('provide a valid sitekey')

        data = {}       # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
            url = RECAPTCHA_SUBMIT_ENDPOINT
        else:
            data['token'] = self._access_token
            url = RECAPTCHA_SUBMIT_ENDPOINT_TOKEN

        # check proxy and set dict (request params) accordingly
        if proxy:   # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['googlekey'] = sitekey
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']
        
        data['recaptchatype'] = 0
        if 'type' in d:
            data['recaptchatype'] = d['type']
            # enterprise
            if str(d['type']) == '4' or str(d['type']) == '5':
                url = RECAPTCHA_ENTERPRISE_SUBMIT_ENDPOINT
            if str(d['type']) == '5':
                data['enterprise_type'] = 'v3'
        if 'v3_action' in d: data['captchaaction'] = d['v3_action']
        if 'v3_min_score' in d: data['score'] = d['v3_min_score']
        if 'data-s' in d: data['data-s'] = d['data-s']
        if 'cookie_input' in d: data['cookie_input'] = d['cookie_input']
        # make request with all data
        response = self._session.post(url, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response
        
        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        return response_text

    # submit geetest captcha
    def submit_geetest(self, d):
        # check if page_url and sitekey are != None
        if 'domain' not in d: raise Exception('domain is missing')
        if 'challenge' not in d: raise Exception('challenge is missing')
        if 'gt' not in d: raise Exception('gt is missing')
        d['action'] = 'UPLOADCAPTCHA'
        # credentials and url
        if self._username:
            d['username'] = self._username
            d['password'] = self._password
            url = GEETEST_SUBMIT_ENDPOINT
        else:
            d['token'] = self._access_token
            url = GEETEST_SUBMIT_ENDPOINT_TOKEN

        # affiliate ID
        if self._affiliate_id: d['affiliateid'] = self._affiliate_id

        url = '{}?{}'.format(url, urlencode(d))
        # make request with all data
        response = self._session.post(url, data=d,
                                      headers=self._headers, timeout=self._timeout)
        response_text = '{}'.format(response.text)

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        return response_text

    # submit geetest captcha
    def submit_geetest_v4(self, d):
        # check if page_url and sitekey are != None
        if 'domain' not in d: raise Exception('domain is missing')
        if 'geetestid' not in d: raise Exception('geetestid is missing')
        d['action'] = 'UPLOADCAPTCHA'
        # credentials and url
        if self._username:
            d['username'] = self._username
            d['password'] = self._password
        else:
            d['token'] = self._access_token

        # affiliate ID
        if self._affiliate_id: d['affiliateid'] = self._affiliate_id

        url = '{}?{}'.format(GEETEST_V4_SUBMIT_ENDPOINT, urlencode(d))
        # make request with all data
        response = self._session.post(url, data=d,
                                      headers=self._headers, timeout=self._timeout)
        response_text = '{}'.format(response.text)

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        return response_text

    # submit hcaptcha
    def submit_hcaptcha(self, d):
        page_url = d['page_url']
        sitekey = d['sitekey']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']  # if proxy, add it

        # check if page_url and sitekey are != None
        if not page_url: raise Exception('provide a valid page_url')
        if not sitekey: raise Exception('provide a valid sitekey')

        data = {}  # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # check proxy and set dict (request params) accordingly
        if proxy:  # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['sitekey'] = sitekey  # just to make sure it's not sitekey that's required as input
        data['captchatype'] = 11
        if 'HcaptchaEnterprise' in d and d['HcaptchaEnterprise']:
            data['HcaptchaEnterprise'] = json.dumps(d['HcaptchaEnterprise'])
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']
        # invisible mode
        if 'invisible' in d:
            data['invisible'] = '1'

        # make request with all data
        response = self._session.post(HCAPTCHA_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        else:
            js = json_loads(response.text)
            response_text = js[0]['CaptchaId']
            return response_text

    # submit capy
    def submit_capy(self, d):
        page_url = d['page_url']
        sitekey = d['sitekey']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']  # if proxy, add it

        # check if page_url and sitekey are != None
        if not page_url: raise Exception('provide a valid page_url')
        if not sitekey: raise Exception('provide a valid sitekey')

        data = {}  # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # check proxy and set dict (request params) accordingly
        if proxy:  # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['sitekey'] = sitekey
        data['captchatype'] = 12
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']

        # make request with all data
        response = self._session.post(CAPY_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        else:
            js = json_loads(response.text)
            response_text = js[0]['CaptchaId']
            return response_text
            
    # submit task
    def submit_task(self, d):
        page_url = d['page_url']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']  # if proxy, add it

        # check if page_url and sitekey are != None
        if not page_url: raise Exception('provide a valid page_url')

        data = {}  # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # check proxy and set dict (request params) accordingly
        if proxy:  # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['variables'] = ''
        if d['variables']:
            data['variables'] = json.dumps(d['variables'])
        data['template_name'] = d['template_name']
        data['captchatype'] = 16
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']

        # make request with all data
        response = self._session.post(TASK_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        else:
            js = json_loads(response.text)
            response_text = js[0]['CaptchaId']
            return response_text

    # submit tiktok
    def submit_tiktok(self, d):
        page_url = d['page_url']
        cookie_input = ''
        if 'cookie_input' in d: cookie_input = d['cookie_input']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']  # if proxy, add it

        # check if page_url and sitekey are != None
        if not page_url: raise Exception('provide a valid page_url')

        data = {}  # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # check proxy and set dict (request params) accordingly
        if proxy:  # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['cookie_input'] = cookie_input
        data['captchatype'] = 10
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']

        # make request with all data
        response = self._session.post(TIKTOK_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        else:
            js = json_loads(response.text)
            return js[0]['CaptchaId']

    # submit capy
    def submit_funcaptcha(self, d):
        # check if page_url and sitekey are != None
        if 'page_url' not in d or not d['page_url']: raise Exception('provide a valid page_url')
        if 'sitekey' not in d or not d['sitekey']: raise Exception('provide a valid sitekey')
        page_url = d['page_url']
        sitekey = d['sitekey']

        # check for proxy
        proxy = None
        if 'proxy' in d: proxy = d['proxy']  # if proxy, add it

        data = {}  # create data obj here, we might need it for proxy

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # check proxy and set dict (request params) accordingly
        if proxy:  # if proxy is given, check proxytype
            # we have both proxy and type at this point
            data['proxy'] = proxy
            data['proxytype'] = 'HTTP'

        # init dict params  (request params)
        data['action'] = 'UPLOADCAPTCHA'
        data['pageurl'] = page_url
        data['sitekey'] = sitekey
        if 's_url' in d: data['surl'] = d['s_url']
        data['captchatype'] = 13
        if self._affiliate_id:
            data['affiliateid'] = self._affiliate_id

        if 'data' in d: data['data'] = d['data']
        # user agent
        if 'user_agent' in d: data['useragent'] = d['user_agent']

        # make request with all data
        response = self._session.post(FUNCAPTCHA_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        # -------------------------------------------------------------
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip())  # raise Ex
        else:
            js = json_loads(response.text)
            response_text = js[0]['CaptchaId']
            return response_text

    # use to retrieve captcha response
    def retrieve_response(self, captcha_id):
        # create params dict (multipart)
        data = {
            'action': 'GETTEXT',
            'captchaid': captcha_id
        }

        if self._username:
            data['username'] = self._username
            data['password'] = self._password
        else:
            data['token'] = self._access_token

        # make request with all data
        response = self._session.post(RETRIEVE_JSON_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)  # get text from response

        # check if we got an error
        if 'ERROR:' in response_text and response_text.split('|') != 2:
            raise Exception(response_text.split('ERROR:')[1].strip().split('"')[0])
        # load json
        try:
            js = json_loads(response_text)
            if not js[0]: return None
            status = js[0]['Status']
            if status.lower() == 'pending': return None
        except:
            raise Exception('invalid JSON response from server: {}.'
                            ' Make sure your input is correct and retry'.format(response_text))

        return json_loads(response_text)[0]  # return response

    # get account balance
    def account_balance(self):
        data = {}
        if self._username:
            url = BALANCE_ENDPOINT
            data["username"] = self._username
            data["password"] = self._password
        else:
            url = BALANCE_ENDPOINT_TOKEN
            data["token"] = self._access_token

        data["action"] = "REQUESTBALANCE"
        data["submit"] = "Submit"
        response = self._session.post(url, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)
        
        # check if we have an error
        if 'ERROR:' in response_text:
            raise Exception(response_text.split('ERROR:')[1].strip())                               # raise

        return '${}'.format(response_text)        # we don't, return balance

    # set captcha bad, if given id, otherwise set the last one
    def set_captcha_bad(self, captcha_id):
        data = {
            "action": "SETBADIMAGE",
            "imageid": captcha_id,
            "submit": "Submissssst"
        }

        if self._username:
            data["username"] = self._username
            data["password"] = self._password
            url = BAD_IMAGE_ENDPOINT
        else:
            data["token"] = self._access_token
            url = BAD_IMAGE_ENDPOINT_TOKEN

        # make request
        response = self._session.post(url, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)

        # check if we have an error
        if 'ERROR:' in response_text:
            raise Exception(response_text.split('ERROR:')[1].strip())                               # raise

        return response_text  # we don't, return balance

    # update task pushVariables
    def task_push_variables(self, captcha_id, variables):
        data = {
            "action": "GETTEXT",
            "captchaid": captcha_id,
            "pushVariables": json.dumps(variables)
        }

        if self._username:
            data["username"] = self._username
            data["password"] = self._password
        else:
            data["token"] = self._access_token

        # make request
        response = self._session.post(TASK_PUSH_ENDPOINT, data=data,
                                      headers=self._headers, timeout=self._timeout)
        response_text = str(response.text)

        # check if we have an error
        if 'ERROR:' in response_text:
            raise Exception(response_text.split('ERROR:')[1].strip())                               # raise

        return response_text
