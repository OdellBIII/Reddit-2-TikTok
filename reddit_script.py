
import sys
import getopt
import requests
import pyttsx3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from PIL import Image
from moviepy.editor import *
import time


"""
Returns the subreddit name that passed through the commandline
"""
def get_commandline_argument(argv):

    subreddit = ''
    try:
        opts, args = getopt.getopt(argv, "s:", ["subreddit="])
    except getopt.GetoptError:
        print("reddit_script.py -s <subreddit>")
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-s", "--subreddit"):

            subreddit = arg

    return subreddit

"""
Returns the JSON for the most popular post from a subreddit
"""
def get_most_popular_post(subreddit):

    url = "http://localhost:3000/subreddit/{}".format(subreddit)
    response = requests.get(url)

    return response.json()

"""
Returns a string stripped and replaced of unnecessary characters
"""
def process_string(str):

    processed_string = str
    # Come up with dictionary of common html codes
    html_codes = {'&amp;#39;' : "'",
                '&lt;!-- SC_OFF --&gt;&lt;div class="md"&gt;&lt;p&gt;' : '',
                '&lt;/p&gt;\n\n&lt;p&gt;' : '',
                '&amp;quot;' : '\"',
                '&lt;/p&gt;\n&lt;/div&gt;&lt;!-- SC_ON --&gt;' : '',
                'AITA' : 'Am I the asshole',
                'aita' : 'Am I the asshole'
                }

    for code in html_codes.keys():

        processed_string = processed_string.replace(code, html_codes[code])

    return processed_string

"""
Returns the passed in object with strings stripped of unnecessary characters
"""
def process_post_strings(popular_post):

    for key in popular_post.keys():

        processed_string = process_string(popular_post[key])
        popular_post[key] = processed_string

    return popular_post

"""
Returns a voice over audio file of the post
"""
def generate_audio_files(processed_post):

    engine = pyttsx3.init()
    daniel_voice_id = "com.apple.speech.synthesis.voice.daniel"
    engine.setProperty('voice', daniel_voice_id)
    engine.save_to_file("{}. {}".format(processed_post['title'], processed_post['body']), "temporary_audio.mp3")
    engine.runAndWait()

    return "temporary_audio.mp3"

"""
Returns a screenshot of the reddit post
"""

def get_selenium_driver():

    # Setup Selenium Driver
    firefox_options = FirefoxOptions()
    #firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    return driver

def get_screenshot(processed_post):

    # Setup Selenium Driver
    driver = get_selenium_driver()

    # Navigate to post page
    driver.get(processed_post['url'])

    # Get Post dimensions
    post_element_rect = driver.find_element(By.XPATH, "//div[starts-with(@class, '_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM  Post')]").rect

    # Take Screenshot
    driver.save_screenshot("temporary_post_screenshot.png")

    # Crop Image and save
    image = Image.open("temporary_post_screenshot.png")
    cropped_image = image.crop((post_element_rect['x'],
        post_element_rect['y'],
        post_element_rect['x'] + post_element_rect['width'],
        post_element_rect['y'] + post_element_rect['height']))

    cropped_image.save("temporary_post_screenshot.png")

    driver.close()

    return "temporary_post_screenshot.png"

"""
"""

def generate_tiktok_image(screenshot_file):

    screenshot_image = Image.open(screenshot_file)
    tiktok_image = Image.open("tiktok-template.png").copy()

    coordinates = (tiktok_image.width // 2 - screenshot_image.width // 2,
                    tiktok_image.height // 2 - screenshot_image.height // 2)

    tiktok_image.paste(screenshot_image, coordinates)

    tiktok_image.save("temporary_post_screenshot.png")

    return "temporary_post_screenshot.png"

"""
"""

def generate_tiktok_video(tiktok_image, voiceover_audio_file):

    image_clip = ImageClip(tiktok_image)
    audio_clip = AudioFileClip(voiceover_audio_file)

    image_clip_with_audio = image_clip.set_audio(audio_clip)

    image_clip_with_audio.set_duration(audio_clip.duration).write_videofile("tiktok-video.mp4", fps=24, audio=True)

    return "tiktok-video.mp4"

"""
"""

def upload_to_tiktok(tiktok_video_file):


    # Cookies
    cookies = [
        {
            "name": "ak_bmsc",
            "value": "65BC6866862DD3B0C3130631E8AA071F~000000000000000000000000000000~YAAQR9jPF/x6dmh9AQAAEfWoNw5gM2v+ZE1OeZwOVm3hFImMEZ1RvQ6QKUiSyCh7UgCxu4rLlBGjr5oImhNcbRRwUJMphuaWAJHxpx9BkkPlWjL8pXa0YSImDH9eKi5B2Rp7wcrGyXAyQpMW1Eq6AmvbTSyc+SEZTc9szCQR/j795EvJytHafzz0u2liBTqoko93cbNrPIvfyGXvGfh5UQgdHtoImiNpRXR8OQohJRhUm1A1wngAkBzot83ycnjcPNH/H/4mA3Yp/zVs/UGIzuozg96aHFnZYOVvPqoNBdsVwemgSMBXNQr+WvdPtm4Y8T4PgqYyNEvGkMqcZ1VSiu7XVGU1ijUPp7i1nnUA9T+4giNuZyaES9dmuhYpRosSqa5Fn3K6eu2L"
        },
        {
            "name": "MONITOR_DEVICE_ID",
            "value": "ae113eec-346c-4d45-827b-1028b5babd37"
        },
        {
            "name": "tta_attr_id",
            "value": "0.1641611479.7050667614040752130"
        },
        {
            "name": "_abck",
            "value": "C50CEC365D78612500C8D0BCD9392A90~-1~YAAQW9jPF1TAMC1+AQAAAfWhNwdVCT6vOXL4qLH57a+tU7EmzuU7aoIZZsZVz+tTEoBtUyZYb+8Sd3+29LXuFZCXuDzsxHIE8rIJzjc5K1I1CFRuWITTjj+Ke1p62kYrbnutNiF4L28y1aWvA0QqBI1JpgsQmmhItcJapAJIq9VN8g9hf6UEOLPhBYV7POhv9+eCkmEMCSZKmRvYizG1gT/0bssfY35plGr5dAyq76iLQhaCxedYrJhT7NZuWB+QZPxtWstBU8HFxFbfACjHB3F+QBsiZ1urgJ/oEY6lRf5P2aBDZW/BGD/S8wFpR6a6Jhp9Ut0Ufh2oGekJ5KQlyWHbaneKgBhyG79k5/n1VlRh9UUSSUmMRBtX3bg/jS2jmNHSUBGcnpHjZA==~-1~-1~-1"
        },
        {
            "name": "csrf_session_id",
            "value": "eebd7a74c0bf4a75ce381d30bee94614"
        },
        {
            "name": "tt_webid",
            "value": "7050667540180633094"
        },
        {
            "name": "msToken",
            "value": "ecVa9qk41b2dDxFmClWULoTSORIh1dY0PfdOXGXWDFyyAf5D0POj1Pj-QMNe03TUbheuvEJ82oXYNkVaWVTUdV6X9IYU8t36OJtwmE_fRO9ChNfoHYs6ppS0LIe_KNSdvlU="
        },
        {
            "name": "MONITOR_WEB_ID",
            "value": "7050667540180633094"
        },
        {
            "name": "custom_slardar_web_id",
            "value": "7050667540180633094"
        },
        {
            "name": "sid_guard",
            "value": "eb81ef9f6042d44fd03a55aa7bbd56b9%7C1641586307%7C5184000%7CTue%2C+08-Mar-2022+20%3A11%3A47+GMT"
        },
        {
            "name": "ttwid",
            "value": "1%7C-TilBAtzY2VZHin8b4eA3xgtzynvxW6wyX0B5APNUq0%7C1641611438%7C24d044f4964ca4933b2e6fce771fe0e2b57f4ff3a844c07401728abf6e97dcfb"
        },
        {
            "name": "uid_tt",
            "value": "7718c854a467430e1e648b289347c363b20b476f7a1439304db9abff6886724d"
        },
        {
            "name": "passport_csrf_token_default",
            "value": "4e0ab0cf9b6a001eec642bf100713034"
        },
        {
            "name": "s_v_web_id",
            "value": "verify_kv76655m_Bws1dOT7_rToQ_4A3f_BvhU_zi49F3DWE843"
        },
        {
            "name": "store-idc",
            "value": "maliva"
        },
        {
            "name": "ssid_ucp_v1",
            "value": "1.0.0-KGQ2OTNlMDRlYmZlODg4YWJmMDcxOTdhMjk1NzRkNjhmYzBkODRjMjIKIAiGiNzM3cyU7GEQg73ijgYYswsgDDCDveKOBjgBQOsHEAMaBm1hbGl2YSIgZWI4MWVmOWY2MDQyZDQ0ZmQwM2E1NWFhN2JiZDU2Yjk"
        },
        {
            "name": "__tea_cookie_tokens_1988",
            "value": "%257B%2522web_id%2522%253A%25227050559535869920815%2522%252C%2522timestamp%2522%253A1641611327220%257D"
        },
        {
            "name": "_tea_utm_cache_1988",
            "value": "{%22utm_source%22:%22sms%22%2C%22utm_medium%22:%22ios%22%2C%22utm_campaign%22:%22client_share%22}"
        },
        {
            "name": "bm_sz",
            "value": "F71C81731C493BCEB9D74B913ED61986~YAAQW9jPF1XAMC1+AQAAAfWhNw4HrD6nszaNljE6K65qpKTFuOpFwhmesdQ1YbX63mglTNeaIX/ltOfcVjUgMwoZQ/vFKvAbYKnKgYfgpe+oJbVEGzLCsS/pelMnBKVS8Ii1PYTJCrO6bC+rqSuhffvK21t3/sHrsOlrXx6hDUms5l23s8Erp6W2B6OD1HagX+5KVl6m/MPj/GR+F53TaaHqWOPsCBgmMs7iLJTzYMf6A8XkmqXIQ7SShHLzhGV0w+gViddH+n+PFi+HeQwUr002nDQ60m0xLEhWxNbTagaQ78Q=~3753285~4277043"
        },
        {
            "name": "cmpl_token",
            "value": "AgQQAPNSF-RO0rHmvMJRpd0_-xa5-w2Tv4fZYMLi7w"
        },
        {
            "name": "MONITOR_WEB_ID",
            "value": "44c9ba4d-4b38-4449-99e5-7288e4f83cb3"
        },
        {
            "name": "odin_tt",
            "value": "ea8c924a5c23e722b20971634abe9dbf0576f50f9942e9c8c615e71f6668bd939140be6dfeddc58b9f2ed575335935f0cfd958e4ee69212a9f27e941de246ef5"
        },
        {
            "name": "passport_csrf_token",
            "value": "4e0ab0cf9b6a001eec642bf100713034"
        },
        {
            "name": "passport_fe_beating_status",
            "value": "True"
        },
        {
            "name": "sessionid",
            "value": "eb81ef9f6042d44fd03a55aa7bbd56b9"
        },
        {
            "name": "sessionid_ss",
            "value": "eb81ef9f6042d44fd03a55aa7bbd56b9"
        },
        {
            "name": "sid_tt",
            "value": "eb81ef9f6042d44fd03a55aa7bbd56b9"
        },
        {
            "name": "sid_ucp_v1",
            "value": "1.0.0-KGQ2OTNlMDRlYmZlODg4YWJmMDcxOTdhMjk1NzRkNjhmYzBkODRjMjIKIAiGiNzM3cyU7GEQg73ijgYYswsgDDCDveKOBjgBQOsHEAMaBm1hbGl2YSIgZWI4MWVmOWY2MDQyZDQ0ZmQwM2E1NWFhN2JiZDU2Yjk"
        },
        {
            "name": "store-country-code",
            "value": "us"
        },
        {
            "name": "tt_csrf_token",
            "value": "_w25qJe1gY5tqSQP8ng_1PmA"
        },
        {
            "name": "tta_attr_id_mirror",
            "value": "0.1641611479.7050667614040752130"
        },
        {
            "name": "uid_tt_ss",
            "value": "7718c854a467430e1e648b289347c363b20b476f7a1439304db9abff6886724d"
        }
    ]
    # Navigate to TikTok page from Selenium
    driver = get_selenium_driver()
    driver.get("https://www.tiktok.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.tiktok.com/upload?lang=en")

    # Get cookies and update them

    new_cookies = driver.get_cookies()
    print(new_cookies)


    # Click email sign in button
    email_signin_button = driver.find_element(By.XPATH, "//div[text()[contains(., 'Use phone / email / username')]]")
    email_signin_button.click()
    time.sleep(3)

    # Switch to email sign in

    switch_to_email_button = driver.find_element(By.XPATH, "//a[text()[contains(., 'Log in with email or username')]]")
    switch_to_email_button.click()
    time.sleep(3)

    # Fill in information
    email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email or Username']")
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    login_button = driver.find_element(By.XPATH, "//button[text()[contains(., 'Log in')]]")

    email_input.send_keys("reddit.tiktokaita@gmail.com")
    password_input.send_keys("reddittiktokaita1!")
    time.sleep(3)
    login_button.click()


    # Upload
def main(argv):

    subreddit = get_commandline_argument(argv)
    popular_post = get_most_popular_post(subreddit)
    processed_popular_post = process_post_strings(popular_post)

    # Generate Audio files
    voiceover_audio_file = generate_audio_files(processed_popular_post)

    # Get Screenshot
    screenshot_file = get_screenshot(processed_popular_post)

    # Past Screenshot to tiktok shaped image

    tiktok_image = generate_tiktok_image(screenshot_file)

    # Combine Screenshot and Audio to create video

    tiktok_video_file = generate_tiktok_video(tiktok_image, voiceover_audio_file)

    print("TikTok video saved at the following location: {}".format(tiktok_video_file))

    upload_to_tiktok(tiktok_video_file)

if __name__ == '__main__':

    #main(sys.argv[1:])
    upload_to_tiktok("Nothing")
