#!/usr/bin/python3

# Imagetyperz captcha API test (python 3)
# -------------------------------------------
from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
from time import sleep

# solve captcha
def test_api():
    access_token = 'access_token_here'
    # get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
    ita = ImageTyperzAPI(access_token)      # init imagetyperz api obj

    # legacy way, will get deprecated at some point
    # ita.set_user_password('your_username', 'your_password')

    # check account balance
    # ---------------------------
    balance = ita.account_balance()                       # get account balance
    print ('Balance: {}'.format(balance))                 # print balance

    # solve image captcha
    # --------------------
    # works with URL as well, if authenticated with token
    print ('Solving captcha ...')
    captcha_text = ita.solve_captcha('captcha.jpg')
    print ('Captcha text: {}'.format(captcha_text))

    # solve recaptcha
    # check: http://www.imagetyperz.com/Forms/recaptchaapi.aspx on how to get page_url and googlekey
    # -----------------------------------------------------------------------------------------------
    page_url = 'http://your_site_here.com'
    sitekey = 'your_sitekey_here'
    captcha_id = ita.submit_recaptcha(page_url, sitekey)        # submit captcha first, to get ID

    # check if it's still in progress (waiting to be solved), every 10 seconds
    print ('Waiting for recaptcha to be solved ...')
    while ita.in_progress():    # while it's still in progress
        sleep(10)               # sleep for 10 seconds and recheck

    recaptcha_response = ita.retrieve_recaptcha(captcha_id)           # captcha_id is optional, if not given, will use last captcha id submited
    print ('Recaptcha response: {}'.format(recaptcha_response))         # print google response

    # other examples
    # --------------------------------------------------------------------------------------
    # ita = ImageTypersAPI(access_token, 123)  # init imagetyperz api obj with access_token and affiliate id
    # ita = ImageTypersAPI(access_token, 123, 60)  # init imagetyperz api obj with access_token, affid and timeout
    # ita.set_user_password('your_username', 'your_password') # in case you want to use user & pass instead of token (not recommended)
    
    # submit recaptcha with proxy (checks API docs for more info)
    # captcha_id = ita.submit_recaptcha(page_url, sitekey, '127.0.0.1:1234')
    # captcha_id = ita.submit_recaptcha(page_url, sitekey, '127.0.0.1:1234:user:pass')		# proxy with authentication
    # print (ita.was_proxy_used(captcha_id))        # tells if proxy submitted (if any) was used or not, and if not used, reason

    # print (ita.captcha_id)               # get last captcha solved id
    # print (ita.captcha_text)       	   # get last captcha solved text

    # print (ita.recaptcha_id)             # get last recaptcha solved id
    # print (ita.recaptcha_response)       # get last recaptcha solved response

    # print (ita.set_captcha_bad(captcha_id))        # set last captcha as bad, or set it by using ID
    # print (ita.error)                    # get the last error encountered

# main method
def main():
    try:
        test_api()     # test captcha API
    except Exception as ex:
        print ('[!] Error occured: {}'.format(ex))

if __name__ == "__main__":
    main()
