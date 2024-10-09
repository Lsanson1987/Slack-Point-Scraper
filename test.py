from slack import WebClient
from dotenv import load_dotenv
import re
import os

#load environment variables
load_dotenv()
    
to_format = response.choices[0]["message"]['content']
# Initialize the Slack client with your bot's API token
slack_token = os.getenv('SLACK_API_KEY')
client = WebClient(token=slack_token)

# Define a dictionary to store pledge points for each user
pledge_points = {}
# Channel ID where pledge point changes are reported
channel_id = 'C07NPQNJEH1'

# Get messages from the channel
response = client.conversations_history(channel=channel_id, limit=1000)

# Regular expression to match pledge points at the start of a message
pattern = re.compile(r'^[+-]?\s*\d+')

# Process each message
for message in response['messages']:
    user_id = message['user']
    text = message['text']

    # Check if the message starts with a pledge point change
    match = pattern.match(text)
    if match:
        change_value = int(match.group().replace(" ", "").replace("+", ""))
        if user_id not in pledge_points:
            pledge_points[user_id] = 0
        pledge_points[user_id] += change_value

# Sort users by total pledge points in descending order
sorted_users = sorted(pledge_points.items(), key=lambda x: x[1], reverse=True)

# Display the sorted list of users and their total pledge points
for user_id, total_points in sorted_users:
    user_info = client.users_info(user=user_id)
    user_name = user_info['user']['real_name']
    print(f'{user_name}: {total_points} points')


# Calculate and display the total amount of pledge points
total_pledge_points = sum(pledge_points.values())
print(f'Total Pledge Points: {total_pledge_points} points')
