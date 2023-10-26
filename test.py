from slack import WebClient
import re

# Initialize the Slack client with your bot's API token
slack_token = 'PLEDGE_BOT_API_TOKEN'
client = WebClient(token=slack_token)

# Define a dictionary to store pledge points for each user
pledge_points = {}

# Channel ID where pledge point changes are reported
channel_id = 'pledge-points'

# Get messages from the channel
response = client.conversations_history(channel=channel_id)

# Process each message
for message in response['messages']:
    user_id = message['user']
    text = message['text']

    # Use regular expressions to find pledge point changes
    changes = re.findall(r'[+-]\d+', text)

    # Update pledge points for the user
    for change in changes:
        change_value = int(change)
        if user_id not in pledge_points:
            pledge_points[user_id] = 0
        pledge_points[user_id] += change_value

# Display the total pledge points for each user
for user_id, total_points in pledge_points.items():
    user_info = client.users_info(user=user_id)
    user_name = user_info['user']['real_name']
    print(f'{user_name}: {total_points} points')
