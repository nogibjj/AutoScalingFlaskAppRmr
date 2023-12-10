"""Reddit API to get latest posts from a subreddit"""
import re
import requests
from transformers import pipeline
from flask import Flask, jsonify, render_template, request
from wordcloud import WordCloud

app = Flask(__name__)


class RedditAPI:
    """Reddit API to get latest posts from a subreddit"""

    def __init__(self, subreddit_name, mode="prod"):
        self.subreddit_name = subreddit_name
        self.posts_api_url = "https://www.reddit.com/r/{subreddit}/new.json"
        self.comments_api_url = (
            "https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        )

        if mode == "prod":
            self.reddit_document = self.get_posts()
        else:
            with open("data/reddit_document.txt", "r", encoding="utf-8") as f:
                self.reddit_document = f.read()

    def get_posts(self):
        """Get latest posts from a subreddit"""
        # Reddit API parameters for posts
        posts_params = {
            "sort": "new",
            "limit": 15,  # Adjust as needed, maximum is usually 100
        }

        # Make the API request for posts
        posts_response = requests.get(
            self.posts_api_url.format(subreddit=self.subreddit_name),
            params=posts_params,
            headers={"User-Agent": "YOUR_USER_AGENT"},
            timeout=10,  # Set a timeout value in seconds
        )

        # Check if the request for posts was successful (status code 200)
        reddit_document = ""
        if posts_response.status_code == 200:
            # Extract and print post titles
            posts = posts_response.json()["data"]["children"]
            for post in posts:
                post_id = post["data"]["id"]
                # reddit_document += "Post Title:"
                reddit_document += post["data"]["title"]  # + "\n"
                # reddit_document += "Post Body:"
                reddit_document += post["data"]["selftext"]  # + "\n"
                reddit_document += self.get_comments(post_id)

            # remove links and emojis from reddit document
            reddit_document = self.remove_links(reddit_document)

        wordcloud = WordCloud(width=800, height=400).generate(reddit_document)
        wordcloud.to_file(r'src/static/wordcloud.png')
        return reddit_document

    def remove_links(self, reddit_document):
        """Remove links and emojis from reddit document"""
        # remove links
        reddit_document = re.sub(r"http\S+", "", reddit_document)
        # remove emojis
        reddit_document = re.sub(r"\\x\S+", "", reddit_document)
        return reddit_document

    def get_comments(self, post_id):
        """Get comments from a post"""
        # Reddit API parameters for comments
        comments_params = {
            "sort": "new",
            "limit": 100,  # Adjust as needed, maximum is usually 100
        }

        # Make the API request for comments
        comments_response = requests.get(
            self.comments_api_url.format(
                subreddit=self.subreddit_name, post_id=post_id
            ),
            params=comments_params,
            headers={"User-Agent": "YOUR_USER_AGENT"},
            timeout=10,  # Set a timeout value in seconds
        )

        # Check if the request for comments was successful (status code 200)
        comment_bodies = ""
        if comments_response.status_code == 200:
            # Extract and concatenate comment bodies
            comments = comments_response.json()[1]["data"]["children"]
            for comment in comments:
                try:
                    # comment_bodies += "Comment:"
                    comment_bodies += comment["data"]["body"] + "\n"
                except KeyError:
                    continue

        return comment_bodies

    def get_sentiment(self):
        """Get sentiment of reddit document"""
        # Load sentiment analysis pipeline
        # this uses distilbert-base-uncased-finetuned-sst-2-english
        nlp = pipeline("sentiment-analysis")

        # Split the text into chunks of 1500 tokens
        max_length = 512
        chunks = [
            self.reddit_document[i : i + max_length]
            for i in range(0, len(self.reddit_document), max_length)
        ]

        # Analyze sentiment of each chunk and aggregate the results
        total_score = 0
        total_positive = 0
        total_negative = 0
        for chunk in chunks:
            result = nlp(chunk)
            score = result[0]["score"]
            total_score += score
            if result[0]["label"] == "POSITIVE":
                total_positive += score
            else:
                total_negative += score

        # Calculate average score and overall sentiment
        avg_score = total_score / len(chunks)
        overall_sentiment = (
            "POSITIVE" if total_positive > total_negative / 3 else "NEGATIVE"
        )

        return overall_sentiment, avg_score


@app.route('/', methods=['GET', 'POST'])
def index():
    """Get sentiment of reddit document"""
    print(21)
    
    if request.method == 'POST':
        print('22')
        topic = request.form.get('topic')
        print(topic)
        reddit_api = RedditAPI(topic, "prod")
        try:
            sentiment, avg_score = reddit_api.get_sentiment()
            return render_template('result.html', sentiment=sentiment, average_score=avg_score)
        except ZeroDivisionError:
            return render_template('error.html',
                                   error_message='No subreddit found for sentiment analysis'), 400
    
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
