# Twitter-Bot-for-Reddit-Content-Automation
This project is a Python-based Twitter bot that automatically reposts submissions from specific subreddits to a designated Twitter account. The bot uses the Reddit API and Twitter API to fetch and post content, with scheduling managed by Windows Task Scheduler.

## Features
* **Automated Content Posting**: Fetches top submissions from a specified subreddit and reposts it to Twitter/X
* **Scheduled Posting**: Uses Windows Task Scheduler to execute bot posts periodically
* **Error Handling**: Implements basic error handling to manage API rate limits and other potential issues

## Technologies Used
* **Python**: Programming language used for bot script
* **Tweepy**: Python library for accessing the Twitter/X API
* **PRAW (Python Reddit API Wrapper)**: Python library for accessing the Reddit API
* **Windows Task Scheduler**: Used for scheduling the bot to run at specified times/intervals

## Installation
### Prerequisites
* Install Python 3
* Create a Twitter/X developer account and recieve your API keys (You can find instructions [here](https://developer.x.com/en/docs/x-api/getting-started/getting-access-to-the-x-api))
* Create a Reddit API application and recieve your API keys (That can be done [here](https://old.reddit.com/prefs/apps/))
### Steps
1. Clone the repository:
```
git clone https://github.com/soosv222/Twitter-Bot-for-Reddit-Content-Automation.git
cd Twitter-Bot-for-Reddit-Content-Automation
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Set up environment variables
   
    * Create a .env file in the project root and add your API keys:
    ```
    CONSUMER_KEY=your_twitter_api_key
    CONSUMER_SECRET=your_twitter_api_secret_key
    ACCESS_TOKEN=your_twitter_access_token
    ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
    CLIENT_ID=your_reddit_client_id
    CLIENT_SECRET=your_reddit_client_secret
    USER_AGENT=your_user_agent
    ```
## Usage
1. Run the bot manually:
```
python twitter_bot.py <subreddit name>
```
2. Run the bot on a schedule:
   
   * Find your python file path in the command prompt:
    ```
    where python
    ```
    * Create a batch file that will run your bot
    ```
    <python file path> </file/path/of/twitter_bot.py> <subreddit name>
    ```
    * Create a basic task in Windows task scheduler to run your .bat file at the desired intervals
