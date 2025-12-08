"""Slack and Email notification service for CI/CD pipeline."""

import os
import json
from typing import Dict, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationService:
    """Service for sending notifications via Slack and Email."""
    
    def __init__(self):
        """Initialize notification service."""
        self.slack_token = os.getenv('SLACK_BOT_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL', '#ci-cd-notifications')
        self.email_enabled = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_password = os.getenv('EMAIL_PASSWORD')
    
    def send_test_notification(self, message: str, status: str = 'info'):
        """Send a test notification."""
        self.send_slack_notification(message, status)
        if self.email_enabled:
            self.send_email_notification(message, status)
    
    def send_slack_notification(self, message: str, status: str = 'info'):
        """Send a notification to Slack.
        
        Args:
            message: The notification message
            status: 'success', 'failure', or 'info'
        """
        if not self.slack_token:
            print("Slack token not configured")
            return False
        
        try:
            client = WebClient(token=self.slack_token)
            
            # Color based on status
            color_map = {
                'success': '#36a64f',
                'failure': '#ff0000',
                'info': '#0099ff'
            }
            color = color_map.get(status, '#0099ff')
            
            # Create message
            response = client.chat_postMessage(
                channel=self.slack_channel,
                attachments=[
                    {
                        'color': color,
                        'title': f'To-Do App CI/CD - {status.upper()}',
                        'text': message,
                        'footer': 'Automated Notification',
                        'ts': int(__import__('time').time())
                    }
                ]
            )
            
            print(f"Slack notification sent successfully: {response['ts']}")
            return True
        
        except SlackApiError as e:
            print(f"Error sending Slack notification: {e}")
            return False
    
    def send_email_notification(self, message: str, status: str = 'info', recipients: Optional[list] = None):
        """Send a notification via email.
        
        Args:
            message: The notification message
            status: 'success', 'failure', or 'info'
            recipients: List of email addresses to send to
        """
        if not self.email_enabled or not self.email_from:
            print("Email notifications not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"To-Do App CI/CD - {status.upper()}"
            msg['From'] = self.email_from
            msg['To'] = ', '.join(recipients or [])
            
            # Create HTML content
            html = f"""
            <html>
                <body>
                    <h2>CI/CD Notification - {status.upper()}</h2>
                    <p>{message}</p>
                    <hr>
                    <p><small>This is an automated notification from the To-Do App CI/CD pipeline.</small></p>
                </body>
            </html>
            """
            
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            print(f"Email notification sent to {recipients}")
            return True
        
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
    
    def send_test_results(self, results: Dict):
        """Send test results notification.
        
        Args:
            results: Dictionary containing test results
        """
        passed = results.get('passed', 0)
        failed = results.get('failed', 0)
        skipped = results.get('skipped', 0)
        coverage = results.get('coverage', '0%')
        
        status = 'success' if failed == 0 else 'failure'
        
        message = f"""
        Test Results Summary
        ✅ Passed: {passed}
        ❌ Failed: {failed}
        ⏭️  Skipped: {skipped}
        📊 Coverage: {coverage}
        """
        
        self.send_slack_notification(message, status)
        if self.email_enabled:
            self.send_email_notification(message, status)
    
    def send_deployment_notification(self, app_name: str, version: str, status: str):
        """Send deployment notification.
        
        Args:
            app_name: Name of the application
            version: Version being deployed
            status: 'started', 'success', or 'failure'
        """
        status_emoji = {
            'started': '🚀',
            'success': '✅',
            'failure': '❌'
        }
        
        message = f"{status_emoji.get(status, '➡️')} Deployment {status.upper()}\n"
        message += f"App: {app_name}\nVersion: {version}"
        
        self.send_slack_notification(message, 'success' if status == 'success' else status)


if __name__ == "__main__":
    # Test the notification service
    service = NotificationService()
    service.send_test_notification("Test notification from To-Do App CI/CD", "info")
