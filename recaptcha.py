#!/usr/bin/python3

from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
from time import sleep

def test_api():
    access_token = 'access_token_here'
    # get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
    ita = ImageTyperzAPI(access_token)  # init imagetyperz api obj

    # check account balance
    balance = ita.account_balance()  # get account balance
    print('Balance: {}'.format(balance))  # print balance

    captcha_params = {
        'page_url' : 'https://your-site.com',
        'sitekey' : '7LrGJmcUABBAALFtIb_FxC0LXm_GwOLyJAfbbUCL',
    #     'type' : 1,                     # optional, 1 - normal recaptcha, 2 - invisible recaptcha, 3 - v3 recaptcha, default: 1
    #     #'v3_min_score' : .3,           # optional
    #     #'v3_action' : 'homepage',      # optional
    #     #'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
    #     #'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
    #     #'data-s': 'data-s-value-here'	# optional   # optional
    }
    captcha_id = ita.submit_recaptcha(captcha_params)  # submit captcha first, to get ID

    # check if it's still in progress (waiting to be solved), every 10 seconds
    print('Waiting for captcha to be solved ...')
    response = None
    while not response:  # while it's still in progress
        sleep(10)  # sleep for 10 seconds and recheck
        response = ita.retrieve_response(captcha_id)
    print('Response: {}'.format(response))  # print response of captcha

    # other examples
    # --------------------------------------------------------------------------------------
    # ita = ImageTypersAPI(access_token, 123)  # init imagetyperz api obj with access_token and affiliate id
    # ita = ImageTypersAPI(access_token, 123, 60)  # init imagetyperz api obj with access_token, affid and timeout
    # ita.set_user_password('your_username', 'your_password') # in case you want to use user & pass instead of token (not recommended)
    # ita.set_captcha_bad(4321)     # if captcha response is bad, use this

# main method
def main():
    try:
        test_api()  # test captcha API
    except Exception as ex:
        print('[!] Error occured: {}'.format(ex))

if __name__ == "__main__":
    main()
