"""Reddit API to get latest posts from a subreddit"""
import re
import requests
from transformers import pipeline


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
            "limit": 100,  # Adjust as needed, maximum is usually 100
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
                reddit_document += "Post Title:"
                reddit_document += post["data"]["title"] + "\n"
                reddit_document += "Post Body:"
                reddit_document += post["data"]["selftext"] + "\n"
                reddit_document += self.get_comments(post_id)

            # remove links and emojis from reddit document
            reddit_document = self.remove_links(reddit_document)

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
                    comment_bodies += "Comment:"
                    comment_bodies += comment["data"]["body"] + "\n"
                except KeyError:
                    continue

        return comment_bodies
   
    def get_answer(self, question):
        """Get answer from a question"""
        model_name = "deepset/roberta-base-squad2"
        nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
        qa_input = {
            'question': question,
            'context': self.reddit_document
        }
        res = nlp(qa_input)
        return res['answer']


if __name__ == "__main__":
    # Usage
    reddit_api = RedditAPI("lakers")
    doc_ = reddit_api.get_posts()
    S_ = "What is the public sentiment based of these reddit posts and comments?"
    print(reddit_api.get_answer(S_))
