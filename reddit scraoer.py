import praw
import csv
import os
import time
from datetime import datetime  # Import datetime for timestamp conversion

# Initialize Reddit client
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent=''
)

# Prompt user for input keyword and number of posts
keyword = input("Enter the keyword to search for: ")
num_posts = int(input("Enter the number of posts to scrape: "))

# Initialize a list to store the scraped data
scraped_data = []

# Define the CSV file name
csv_filename = 'reddit_scraped_data.csv'

# Check if the file exists to determine the starting post number
if os.path.isfile(csv_filename):
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        # Read the last line
        last_line = None
        for last_line in reader:
            pass
        if last_line:
            # Continue numbering from the last post number
            post_number = int(last_line[0]) + 1
        else:
            post_number = 1
else:
    post_number = 1

# Initialize posts fetched count
posts_fetched = 0

# Search Reddit for the keyword in all subreddits
while posts_fetched < num_posts:
    for submission in reddit.subreddit('all').search(keyword, limit=100):  # Fetch in chunks of 100
        if posts_fetched >= num_posts:
            break
        
        # Extract the necessary data
        title = submission.title
        body = submission.selftext
        score = submission.score
        num_comments = submission.num_comments
        # Convert the timestamp to a readable format
        created_time = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        
        # Append the data to the list
        scraped_data.append([post_number, title, body, score, num_comments, created_time])
        
        # Increment post number and posts fetched count
        post_number += 1
        posts_fetched += 1
    
    # Introduce a delay to avoid hitting Reddit API rate limits
    time.sleep(2)  # Adjust sleep time if necessary

# Check if the file exists to determine whether to write headers
file_exists = os.path.isfile(csv_filename)

# Write the data to a CSV file (appending)
with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row only if the file didn't exist
    if not file_exists:
        writer.writerow(['Post Number', 'Title', 'Body', 'Score', 'Number of Comments', 'Timestamp'])
    
    # Write the scraped data
    writer.writerows(scraped_data)

print(f"{posts_fetched} posts have been scraped successfully! The results have been appended to '{csv_filename}'.")
