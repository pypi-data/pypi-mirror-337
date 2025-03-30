# Audioscrape Python SDK

Official Python client library for the [Audioscrape](https://www.audioscrape.com) API. This library provides a clean, Pythonic interface to interact with Audioscrape's various endpoints for searching podcast transcriptions and managing notification subscriptions.

## Installation

```bash
pip install audioscrape-sdk
```

## Authentication

To use the Audioscrape API, you need an API key, which can be obtained from your Audioscrape dashboard.

```python
import audioscrape

client = audioscrape.Client(api_key="YOUR_API_KEY")
```

## Usage Examples

### Search API

Search for podcast segments that mention specific terms:

```python
# Basic search
results = client.search.search("machine learning AND neural networks")

# With pagination
results = client.search.search(
    query="machine learning AND neural networks", 
    limit=10, 
    offset=0
)

# Print the first result
if results["results"]:
    first_match = results["results"][0]
    print(f"Podcast: {first_match['podcast']['title']}")
    print(f"Episode: {first_match['episode']['title']}")
    print(f"Match: {first_match['matches'][0]['text']}")
```

### Notifications API

Create and manage search term notifications:

```python
# Create a notification
notification = client.notifications.create_notification(
    search_term="\"artificial intelligence\" AND ethics",
    webhook_url="https://your-webhook.com/endpoint",
    email_recipient="user@example.com"
)
print(f"Created notification with ID: {notification['id']}")

# List all notifications
notifications = client.notifications.list_notifications()
for notification in notifications:
    print(f"ID: {notification['id']}, Term: {notification['search_term']}")

# Delete a notification
client.notifications.delete_notification(notification_id=123)
```

## Advanced Query Syntax

Audioscrape supports advanced query syntax for more precise searches:

- `"exact phrase"` - Match exact phrases
- `term1 AND term2` - Both terms must be present
- `term1 OR term2` - Either term can be present
- `term1 NOT term2` or `term1 -term2` - Exclude content with second term
- `term*` - Wildcard matching (prefix search)
- `(term1 OR term2) AND term3` - Grouping for complex queries

## Error Handling

The SDK will raise exceptions for API errors:

```python
import requests
from audioscrape import Client

try:
    client = Client(api_key="YOUR_API_KEY")
    results = client.search.search("artificial intelligence")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
```

## License

This SDK is distributed under the MIT license.
