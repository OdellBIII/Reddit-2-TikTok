
import sys
import getopt
import requests
import pyttsx3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from PIL import Image
from moviepy.editor import *
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
def get_screenshot(processed_post):

    # Setup Selenium Driver
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

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

if __name__ == '__main__':
    main(sys.argv[1:])
    """
    fake_dict = {'url' : "https://www.reddit.com/r/AmItheAsshole/comments/rwkyrt/Am I the asshole_for_refusing_to_leave_my_boyfriends_birthday/"}
    value = get_screenshot(fake_dict)
    tiktok_image = generate_tiktok_image(value)
    print(generate_tiktok_video(value, ))
    """
