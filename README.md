imagetyperz-api-python3 - Imagetyperz API wrapper
=========================================

imagetyperzapi3 is a super easy to use bypass captcha API wrapper for imagetyperz.com captcha service

## Installation
    pip install imagetyperzapi3

or
    
    git clone https://github.com/imagetyperz-api/imagetyperz-api-python3

## Usage
    # make sure you've changed access_key, page_url, etc in main.py
    python3 main.py  

## How to use?

Simply require the module, set the auth details and start using the captcha service:

``` python
from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
```
Set access_token or username and password (legacy) for authentication

``` python
access_token = 'access_token_here'
# get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
ita = ImageTyperzAPI(access_token)      # init imagetyperz api obj
```
```python
# legacy way, will get deprecated at some point
#ita.set_user_password('your_username', 'your_password')
```
Once you've set your authentication details, you can start using the API

**Get balance**

``` python
balance = ita.account_balance()                       # get account balance
print ('Balance: {}'.format(balance))                 # print balance
```

**Submit image captcha**

``` python
ita.solve_captcha('captcha.jpg', case_sensitive=False)
```
**Works with both files and URLs**
``` python
ita.solve_captcha('http://abc.com/your_captcha.jpg')   
```
**Submit recaptcha details**

For recaptcha submission there are two things that are required.
- page_url
- site_key
- type - can be one of this 3 values: `1` - normal, `2` - invisible, `3` - v3 (it's optional, defaults to `1`)
- v3_min_score - minimum score to target for v3 recaptcha `- optional`
- v3_action - action parameter to use for v3 recaptcha `- optional`
- proxy - proxy to use when solving recaptcha, eg. `12.34.56.78:1234` or `12.34.56.78:1234:user:password` `- optional`
- user_agent - useragent to use when solve recaptcha `- optional` 

``` python
recaptcha_params = {
    'page_url' : 'example.com',
    'sitekey' : '6FDDs34g3321-3234fgfh23rv32fgtrrsv3c',
    'type' : 3,                     # optional, 1 - normal recaptcha, 2 - invisible recaptcha, 3 - v3 recaptcha, default: 1
    'v3_min_score' : .3,           # optional
    'v3_action' : 'homepage',      # optional
    'proxy': '126.45.34.53:345',    # or 126.45.34.53:123:joe:password
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'    # optional
}
captcha_id = ita.submit_recaptcha(recaptcha_params)
```
This method returns a captchaID. This ID will be used next, to retrieve the g-response, once workers have 
completed the captcha. This takes somewhere between 10-80 seconds.

**Retrieve captcha response**

Once you have the captchaID, you check for it's progress, and later on retrieve the gresponse.

The ***in_progress()*** method will tell you if captcha is still being decoded by workers.
Once it's no longer in progress, you can retrieve the gresponse with ***retrieve_recaptcha(captcha_id)***  

``` python
# check if it's still in progress (waiting to be solved), every 10 seconds
while ita.in_progress():    # while it's still in progress
	sleep(10)               # sleep for 10 seconds and recheck

recaptcha_response = ita.retrieve_recaptcha(captcha_id)           # captcha_id is optional, if not given, will use last captcha id submited
print ('Recaptcha response: {}'.format(recaptcha_response))         # print google response
```

## Other methods/variables

**Affiliate id**

The constructor accepts a 2nd parameter, as the affiliate id. 
``` python
ita = ImageTyperzAPI(access_token, 123)     # 123 is the affid
```

**Requests timeout**

As a 3rd parameter in the constructor, you can specify a timeout for the requests (in seconds)
``` python
ita = ImageTyperzAPI(access_token, 123, 60)  # sets timeout to 60 seconds
```

**Get details of proxy for recaptcha**

In case you submitted the recaptcha with proxy, you can check the status of the proxy, if it was used or not,
and if not, what the reason was with the following:

``` python
print (ita.was_proxy_used(captcha_id))
```

**Set captcha bad**

When a captcha was solved wrong by our workers, you can notify the server with it's ID,
so we know something went wrong.

``` python
ita.set_captcha_bad(captcha_id)
```

## Examples
Check main.py

## License
API library is licensed under the MIT License

## More information
More details about the server-side API can be found [here](http://imagetyperz.com)


<sup><sub>captcha, bypasscaptcha, decaptcher, decaptcha, 2captcha, deathbycaptcha, anticaptcha, 
bypassrecaptchav2, bypassnocaptcharecaptcha, bypassinvisiblerecaptcha, captchaservicesforrecaptchav2, 
recaptchav2captchasolver, googlerecaptchasolver, recaptchasolverpython, recaptchabypassscript</sup></sub>

