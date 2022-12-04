
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
import pickle


"""
Returns the subreddit name that passed through the commandline
"""
def get_commandline_argument(argv):

    subreddit = ''
    reddit_post = ''
    try:
        opts, args = getopt.getopt(argv, "s:", ["subreddit="])
    except getopt.GetoptError:
        print("reddit_script.py -s <subreddit>")
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-s", "--subreddit"):

            subreddit = arg

        elif opt in ("-r", "--reddit-post"):

            reddit_post = arg

    return subreddit, reddit_post

"""
Returns the JSON for the most popular post from a subreddit
"""
def get_most_popular_post(subreddit):

    url = "http://localhost:3000/subreddit/{}".format(subreddit)
    print("---url---")
    print(url)
    response = requests.get(url)

    return response.json()

"""
TODO: Returns the JSON for the reddit post
"""
def get_reddit_post_json(reddit_url):

    url = "http://localhost:3000/subreddit/{}".format(subreddit)
    print("---url---")
    print(url)
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

        if popular_post[key] != None:
            processed_string = process_string(popular_post[key])
            popular_post[key] = processed_string

    return popular_post

"""
Returns a voice over audio file of the post
"""
def generate_audio_files(processed_post):

    voiceover_audio_file_name = "temporary_audio.mp3"
    engine = pyttsx3.init()
    daniel_voice_id = "com.apple.speech.synthesis.voice.daniel"
    engine.setProperty('voice', daniel_voice_id)
    engine.save_to_file("{}. {}".format(processed_post['title'], processed_post['body']), voiceover_audio_file_name)
    engine.runAndWait()

    return voiceover_audio_file_name

"""
Retruns the standard selenium driver that is used throughout the script
"""
def get_selenium_driver():

    # Setup Selenium Driver
    firefox_options = FirefoxOptions()
    #firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    return driver

"""
Returns a screenshot of the reddit post
"""
def get_screenshot(processed_post):

    screenshot_file_name = "temporary_post_screenshot.png"
    # Setup Selenium Driver
    driver = get_selenium_driver()

    # Navigate to post page
    driver.get(processed_post['url'])

    # Get Post dimensions
    post_element_rect = driver.find_element(By.XPATH, "//div[starts-with(@class, '_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM  Post')]").rect

    # Take Screenshot
    driver.save_screenshot(screenshot_file_name)

    # Crop Image and save
    image = Image.open(screenshot_file_name)
    cropped_image = image.crop((post_element_rect['x'],
        post_element_rect['y'],
        post_element_rect['x'] + post_element_rect['width'],
        post_element_rect['y'] + post_element_rect['height']))

    cropped_image.save(screenshot_file_name)

    driver.close()

    return screenshot_file_name

"""
Returns a screenshot with an animated background
"""
def generate_tiktok_animated_image(screenshot_file):

    pixa_key = "25263112-b6025f15f3803b0cde64c695d"
    pixa_url = "https://pixabay.com/api/videos/?key={key}&q={keyword}".format(key=pixa_key, keyword="abstract")

    response = requests.get(pixa_url)

    return response
"""
Returns the screenshot with a blank background
"""
def generate_tiktok_image(screenshot_file):

    screenshot_file_name = "temporary_post_screenshot.png"
    screenshot_image = Image.open(screenshot_file)
    tiktok_image = Image.open("tiktok-template.png").copy()

    coordinates = (tiktok_image.width // 2 - screenshot_image.width // 2,
                    tiktok_image.height // 2 - screenshot_image.height // 2)

    tiktok_image.paste(screenshot_image, coordinates)

    tiktok_image.save(screenshot_file_name)

    return screenshot_file_name

"""
Returns a video with the screenshot being displayed and voiceover playing as the audio
"""
def generate_tiktok_video(tiktok_image, voiceover_audio_file):

    # The video name is the same as the caption because tiktok automatically makes the caption
    # the file's name and I could not figure out a way to programmatically change the caption
    # with Selenium. Might do it later
    video_name = "Like and follow for more! #aita #reddit #fyp.mp4"
    image_clip = ImageClip(tiktok_image)
    audio_clip = AudioFileClip(voiceover_audio_file)

    image_clip_with_audio = image_clip.set_audio(audio_clip)

    image_clip_with_audio.set_duration(audio_clip.duration).write_videofile(video_name, fps=24, audio=True)

    return video_name


"""
Returns TikTok cookies
"""

def get_tiktok_cookies():

    cookies_file_name = "tiktok_cookies.pkl"
    cookies_file = open(cookies_file_name, 'rb')
    cookies_list = pickle.load(cookies_file)

    return cookies_list


"""
Remove unnecessary fields from cookies
"""
def strip_cookies(cookies):

    stripped_cookies = []
    for cookie in cookies:

        stripped_cookie = {
            'name' : cookie['name'],
            'value' : cookie['value']
        }

        stripped_cookies.append(stripped_cookie)

    return stripped_cookies

"""
Save the TikTok cookies locally
"""
def save_tiktok_cookies(new_cookies):

    stripped_cookies = strip_cookies(new_cookies)
    cookies_file_name = "tiktok_cookies.pkl"

    with open(cookies_file_name, 'wb') as cookies_file:
        pickle.dump(stripped_cookies, cookies_file)

"""
Uploads the video to TikTok
"""
def upload_to_tiktok(tiktok_video_file):

    # Cookies for signing into TikTok
    cookies = get_tiktok_cookies()

    # Navigate to TikTok page from Selenium
    driver = get_selenium_driver()
    driver.get("https://www.tiktok.com")
    # Load cookies into browsing session
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.tiktok.com/upload?lang=en")

    # Get cookies and update them
    # TODO: Save the cookies to a file like pickle
    new_cookies = driver.get_cookies()
    save_tiktok_cookies(new_cookies)
    #print(new_cookies)

    time.sleep(3)

    # Switch to iframe
    driver.switch_to.frame(0)

    #Select file and upload it
    select_file_button = driver.find_element(By.XPATH, '//div[@id="root"]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/input')
    select_file_button.send_keys("/Users/odellblackmoniii/Projects/Reddit2TikTok/Reddit-2-TikTok/{}".format(tiktok_video_file))
    time.sleep(5)

    # Click post button and post
    post_button = driver.find_element(By.XPATH, "//button[text()[contains(., 'Post')]]")
    print(post_button)
    post_button.click()


def main(argv):

    subreddit, reddit_post = get_commandline_argument(argv)
    popular_post_json = get_most_popular_post(subreddit)
    print(popular_post_json)
    processed_popular_post = process_post_strings(popular_post_json)

    # Generate Audio files
    voiceover_audio_file = generate_audio_files(processed_popular_post)

    # Get Screenshot
    #screenshot_file = get_screenshot(processed_popular_post)

    # Past Screenshot to tiktok shaped image
    #tiktok_image = generate_tiktok_image(screenshot_file)

    # Combine Screenshot and Audio to create video
    tiktok_video_file = generate_tiktok_video(tiktok_image, voiceover_audio_file)

    print("TikTok video saved at the following location: {}".format(tiktok_video_file))

    #upload_to_tiktok(tiktok_video_file)

if __name__ == '__main__':

    main(sys.argv[1:])
    #print(generate_tiktok_animated_image("").json())
