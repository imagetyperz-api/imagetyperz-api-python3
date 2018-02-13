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
``` python
captcha_id = ita.submit_recaptcha(page_url, sitekey)        # submit captcha first, to get ID
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

**Submit recaptcha with proxy**

When a proxy is submitted with the recaptcha details, the workers will complete the captcha using
the provided proxy/IP.

``` python
captcha_id = ita.submit_recaptcha(page_url, sitekey, '12.34.56.78:1234')    # ip:port
```
Proxy with authentication is also supported
``` python
captcha_id = ita.submit_recaptcha(page_url, sitekey, '12.34.56.78:1234:user:password')
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
