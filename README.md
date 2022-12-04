# Reddit-2-TikTok
This scripts posts the most trending post from a subreddit as a video on TikTok with voiceover capabilities

## Installation and Setup

### Clone the repository
`git clone https://github.com/OdellBIII/Reddit-2-TikTok.git`

### Activate the virtual environment
`source reddit2tiktok/bin/activate`

### Setting up NodeJS
The current version of this project requires a NodeJS server so please install NodeJS if you do not have it already
https://nodejs.org/en/download/

Once NodeJS is installed, you can start the node server
`node index.js`

### Executing the Script
You can run script using the following command
`python3 reddit_script.py -s <name_of_subreddit>`.

Replace "<name_of_subreddit>" wit the name of the subreddit you would like to turn into a video. The most popular post from the day will be selected and transformed into a video.

## Future Work
The function responsible for uploading the videos to TikTok was working at one point, but I believe the layout of the signin page changes. This function will have to be addressed to use the script fully
