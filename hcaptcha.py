#!/usr/bin/python3

from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
from time import sleep


def test_api():
    access_token = 'access_token_here'
    # get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
    ita = ImageTyperzAPI(access_token)      # init imagetyperz api obj

    # check account balance
    balance = ita.account_balance()                       # get account balance
    print(f'Balance: {balance}')

    captcha_params = {
        'page_url': 'https://your-site.com',
        'sitekey': '8c7062c7-cae6-4e12-96fb-303fbec7fe4f',
        # 'invisible': '1',             # if invisible hcaptcha - optional

        # domain used in loading of hcaptcha interface, default: hcaptcha.com - optional
        # 'domain': 'hcaptcha.com',

        # extra parameters, useful for enterprise
        # submit userAgent from requests too, when this is used
        # 'HcaptchaEnterprise': {
        #    'rqdata': 'take value from web requests'
        # },

        # 'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
        # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
    }
    captcha_id = ita.submit_hcaptcha(captcha_params)  # submit captcha first, to get ID

    # check if it's still in progress (waiting to be solved), every 10 seconds
    print('Waiting for captcha to be solved ...')
    response = None
    while not response:  # while it's still in progress
        sleep(10)  # sleep for 10 seconds and recheck
        response = ita.retrieve_response(captcha_id)
    print(f'Response: {response}')


# main method
def main():
    try:
        test_api()     # test captcha API
    except Exception as ex:
        print(f'[!] Error occurred: {ex}')


if __name__ == "__main__":
    main()
