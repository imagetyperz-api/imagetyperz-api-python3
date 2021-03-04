imagetyperz-api-python3 - Imagetyperz API wrapper
=========================================

imagetyperzapi3 is a super easy to use bypass captcha API wrapper for imagetyperz.com captcha service

## Installation
    git clone https://github.com/imagetyperz-api/imagetyperz-api-python3

## Usage

Simply require the module, set the auth details and start using the captcha service:

``` python
from imagetyperzapi3.imagetyperzapi import ImageTyperzAPI
```
Set access_token for authentication:

``` python
access_token = 'access_token_here'
# get access token from: http://www.imagetyperz.com/Forms/ClientHome.aspx
ita = ImageTyperzAPI(access_token)      # init imagetyperz api obj
```

Once you've set your authentication details, you can start using the API.

**Get balance**

``` python
balance = ita.account_balance()                       # get account balance
print ('Balance: {}'.format(balance))                 # print balance
```

## Solving
For solving a captcha, it's a two step process:
- **submit captcha** details - returns an ID
- use ID to check it's progress - and **get solution** when solved.

Each captcha type has it's own submission method.

For getting the response, same method is used for all types.


### Image captcha

``` python
captcha_id = ita.submit_image('captcha.jpg')
```
(with optional parameters)
```python
captcha_id = ita.solve_captcha('captcha.jpg', is_case_sensitive = False, is_phrase = False, digits_only = False, letters_only = True, is_math = False, min_length = 2, max_length = 10)
```
ID is used to retrieve solution when solved.

**Observation**
It works with URL instead of image file too, but authentication has to be done using token.

### reCAPTCHA

For recaptcha submission there are two things that are required.
- page_url (**required**)
- site_key (**required**)
- type (optional, defaults to 1 if not given)
  - `1` - v2
  - `2` - invisible
  - `3` - v3
  - `4` - enterprise v2
  - `5` - enterprise v3
- v3_min_score - minimum score to target for v3 recaptcha `- optional`
- v3_action - action parameter to use for v3 recaptcha `- optional`
- proxy - proxy to use when solving recaptcha, eg. `12.34.56.78:1234` or `12.34.56.78:1234:user:password` `- optional`
- user_agent - useragent to use when solve recaptcha `- optional` 
- data-s - extra parameter used in solving recaptcha `- optional`
- cookie_input - cookies used in solving reCAPTCHA - `- optional`

``` python
captcha_params = {
    'page_url' : 'example.com',
    'sitekey' : '6FDDs34g3321-3234fgfh23rv32fgtrrsv3c',
    #'type' : 2,                    # optional
    #'v3_min_score' : .3,           # optional
    #'v3_action' : 'homepage',      # optional
    #'proxy': '126.45.34.53:345',    # optional, or 126.45.34.53:123:joe:password
    #'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
    #'data-s': 'data-s-value-here'   # optional
    #'cookie_input': 'a=b;c=d'  # optional
}
captcha_id = ita.submit_recaptcha(captcha_params)
```
ID will be used to retrieve the g-response, once workers have 
completed the captcha. This takes somewhere between 10-80 seconds. 

Check **Retrieve response** 

### GeeTest

GeeTest is a captcha that requires 3 parameters to be solved:
- domain
- challenge
- gt

The response of this captcha after completion are 3 codes:
- challenge
- validate
- seccode

**Important**
This captcha requires a **unique** challenge to be sent along with each captcha.

```python
captcha_params = {
        'domain' :'https://your-site.com',
        'challenge': 'eea8d7d1bd1a933d72a9eda8af6d15d3',
        'gt': '1a761081b1114c388092c8e2fd7f58bc',
        # 'proxy': '126.45.34.53:345',    # or 126.45.34.53:123:joe:password
        # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'    # optional
}
captcha_id = ita.submit_geetest(captcha_params)
```

Optionally, you can send proxy and user_agent along.

### hCaptcha

Requires page_url and sitekey

```python
captcha_params = {
        'page_url': 'https://your-site.com',
        'sitekey': '8c7062c7-cae6-4e12-96fb-303fbec7fe4f',
        # 'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
        # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
    }
    captcha_id = ita.submit_hcaptcha(captcha_params)
```

### Capy

Requires page_url and sitekey

```python
captcha_params = {
    'page_url': 'https://your-site.com',
    'sitekey': 'Fme6hZLjuCRMMC3uh15F52D3uNms5c',
     # 'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
     # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
}
captcha_id = ita.submit_capy(captcha_params)  # submit captcha first, to get ID
```

### Tiktok

Requires page_url cookie_input

```python
captcha_params = {
    'page_url': 'https://tiktok.com',
     # make sure `s_v_web_id` cookie is present
     'cookie_input': 's_v_web_id:verify_kd6243o_fd449FX_FDGG_1x8E_8NiQ_fgrg9FEIJ3f;tt_webid:612465623570154;tt_webid_v2:7679206562717014313;SLARDAR_WEB_ID:d0314f-ce16-5e16-a066-71f19df1545f;',
     # 'proxy': '126.45.34.53:345',   # or 126.45.34.53:123:joe:password
     # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
}
captcha_id = ita.submit_tiktok(captcha_params)  # submit captcha first, to get ID
```

### FunCaptcha

Requires page_url, sitekey and s_url (source URL)

```python
captcha_params = {
    'page_url': 'https://your-site.com',
    'sitekey': '11111111-1111-1111-1111-111111111111',
    's_url': 'https://api.arkoselabs.com',
    # 'data': '{"a": "b"}',          # optional, extra funcaptcha data in JSON format
    # 'proxy': '12.34.56.78:321',    # optional, or 126.45.34.53:123:joe:password
    # 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',    # optional
}  
captcha_id = ita.submit_capy(captcha_params)  # submit captcha first, to get ID
```

## Retrieve response

Regardless of the captcha type (and method) used in submission of the captcha, this method is used
right after to check for it's solving status and also get the response once solved.

It requires one parameter, that's the **captcha ID** gathered from first step.

```python
response = ita.retrieve_response(captcha_id)
```

```python
# get a captcha_id first
captcha_id = ita.submit_recaptcha(captcha_params)  # submit captcha first, to get ID

# check if it's still in progress (waiting to be solved), every 10 seconds
print('Waiting for captcha to be solved ...')
response = None
while not response:  # while it's still in progress
    sleep(10)  # sleep for 10 seconds and recheck
    response = ita.retrieve_response(captcha_id)
print('Response: {}'.format(response))  # print response of captcha
```
The response is a JSON object that looks like this:
```json
{
  "CaptchaId": 176707908, 
  "Response": "03AGdBq24PBCbwiDRaS_MJ7Z...mYXMPiDwWUyEOsYpo97CZ3tVmWzrB", 
  "Cookie_OutPut": "", 
  "Proxy_reason": "", 
  "Recaptcha score": 0.0, 
  "Status": "Solved"
}
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

**Set captcha bad**

When a captcha was solved wrong by our workers, you can notify the server with it's ID,
so we know something went wrong.

``` python
ita.set_captcha_bad(captcha_id)
```

## Examples
Check root folder for examples, for each type of captcha.

## License
API library is licensed under the MIT License

## More information
More details about the server-side API can be found [here](http://imagetyperz.com)


<sup><sub>captcha, bypasscaptcha, decaptcher, decaptcha, 2captcha, deathbycaptcha, anticaptcha, 
bypassrecaptchav2, bypassnocaptcharecaptcha, bypassinvisiblerecaptcha, captchaservicesforrecaptchav2, 
recaptchav2captchasolver, googlerecaptchasolver, recaptchasolverpython, recaptchabypassscript</sup></sub>

