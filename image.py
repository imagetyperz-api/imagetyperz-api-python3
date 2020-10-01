#!/usr/bin/python3

from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI

def test_api():
    access_token = 'access_token_here'
    # get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
    ita = ImageTyperzAPI(access_token)  # init imagetyperz api obj

    # check account balance
    balance = ita.account_balance()  # get account balance
    print('Balance: {}'.format(balance))  # print balance

    print('Waiting for captcha to be solved ...')
    # works with URL too, if authenticated using token
    captcha_id = ita.submit_image('captcha.jpg')
    # optional parameters for image captcha
    # captcha_id = ita.solve_captcha('captcha.jpg', is_case_sensitive = False, is_phrase = False, digits_only = False, letters_only = True, is_math = False, min_length = 2, max_length = 10)
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
