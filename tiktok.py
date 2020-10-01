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
        'page_url': 'https://tiktok.com',
        # make sure `s_v_web_id` cookie is present
         'cookie_input': 's_v_web_id:verify_kd6243o_fd449FX_FDGG_1x8E_8NiQ_fgrg9FEIJ3f;tt_webid:612465623570154;tt_webid_v2:7679206562717014313;SLARDAR_WEB_ID:d0314f-ce16-5e16-a066-71f19df1545f;',
         # 'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
         # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
    }
    captcha_id = ita.submit_tiktok(captcha_params)  # submit captcha first, to get ID

    # check if it's still in progress (waiting to be solved), every 10 seconds
    print('Waiting for captcha to be solved ...')
    response = None
    while not response:  # while it's still in progress
        sleep(10)  # sleep for 10 seconds and recheck
        response = ita.retrieve_response(captcha_id)
    print('Response: {}'.format(response))  # print response of captcha

# main method
def main():
    try:
        test_api()  # test captcha API
    except Exception as ex:
        print('[!] Error occured: {}'.format(ex))

if __name__ == "__main__":
    main()
