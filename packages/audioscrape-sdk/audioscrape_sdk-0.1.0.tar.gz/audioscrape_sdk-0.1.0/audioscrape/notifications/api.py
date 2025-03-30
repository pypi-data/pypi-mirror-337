class NotificationsAPI:
    """Client for accessing the Audioscrape Notifications API"""

    def __init__(self, client):
        """
        Initialize the Notifications API client.

        Args:
            client (Client): The Audioscrape client instance
        """
        self.client = client

    def create_notification(self, search_term, webhook_url=None, email_recipient=None):
        """
        Create a new notification for a search term.

        Args:
            search_term (str): The term to search for in new transcriptions
            webhook_url (str, optional): URL to receive webhook notifications
            email_recipient (str, optional): Email address to receive notifications

        Returns:
            dict: Created notification object
        """
        if not webhook_url and not email_recipient:
            raise ValueError(
                "At least one notification method (webhook_url or email_recipient) is required"
            )

        payload = {"search_term": search_term}

        if webhook_url:
            payload["webhook_url"] = webhook_url

        if email_recipient:
            payload["email_recipient"] = email_recipient

        return self.client.request("POST", "notifications", json=payload)

    def list_notifications(self):
        """
        Retrieve all notifications for the authenticated user.

        Returns:
            list: List of notification objects
        """
        return self.client.request("GET", "notifications")

    def delete_notification(self, notification_id):
        """
        Delete a specific notification.

        Args:
            notification_id (int): ID of the notification to delete

        Returns:
            dict: Empty dict on success (204 response)
        """
        return self.client.request("DELETE", f"notifications/{notification_id}")
