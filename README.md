# Reddit Sentiment Analysis Flask App
### by Rakeen Rouf

[![PythonCiCd](https://github.com/rmr327/cicd_python_template/actions/workflows/python_ci_cd.yml/badge.svg)](https://github.com/rmr327/cicd_python_template/actions/workflows/python_ci_cd.yml)

---
This repository contains a Flask web application that performs sentiment analysis on the latest posts from a user defined topic's subreddit using the Reddit API and the Hugging Face Transformers library.

## Features

- Retrieves the latest posts from a specified topic's subreddit using the Reddit API.
- Performs sentiment analysis on the retrieved posts using the Hugging Face Transformers library.
- Displays the sentiment analysis results in a user-friendly web interface.
- Generates a word cloud visualization based on the retrieved posts.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/repo-name.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```


## Usage

1. Run the Flask application:

   ```shell
   python reddit_sentiment_flask.py
   ```

2. Open your web browser and navigate to the locally hosted application.

3. Enter the name of the topic you want to analyze and click the "Get Sentiment Analysis" button.

4. The application will retrieve the latest posts from the specified topic's subreddit, perform sentiment analysis on them, and display the results along with a word cloud visualization.

## Dockerization and Hosting

This application has been Dockerized for easy deployment and scalability. The Docker image for this application has been uploaded to Docker Hub and hosted using Azure Container Registry.

The following steps where followed:

1. Build docker image (after loggin in to docket - docker login)
![Alt text](image-5.png)

2. Push the docker image from step 1 to dockerhub

![Alt text](image-6.png)
![Alt text](image-7.png)

3. Add the image to Azure Container Registry
![Alt text](image-8.png)

## Sample Usage for actionable and data driven recommendation

1. Positive Sentiment Example.

As we can see, as of Dec 10 5:05 pm, the public has a NEGATIVE sentiment on OpenAi. This makes sense, since they are known to be an unethical company. Avoid having long exposure.

![Alt text](image-1.png)

![Alt text](image.png)

1. Positive Sentiment Example.

As we can see, as of Dec 10 5:05 pm, the public has a POSITIVE sentiment on Anthropic. This makes sense, since they are known to be an ethical counter party to OpenAi. Avoid having long exposure.

![Alt text](image-2.png)

![Alt text](image-3.png)
