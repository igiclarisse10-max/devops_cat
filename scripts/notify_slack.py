#!/usr/bin/env python3
"""
Slack notification script for CI pipeline
Sends test results and build status to Slack channel
"""

import json
import os
import sys
import argparse
from datetime import datetime
import requests


def send_slack_notification(status, message):
    """
    Send a notification to Slack
    
    Args:
        status (str): 'success' or 'failure'
        message (str): Custom message to include
    """
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        print("Warning: SLACK_WEBHOOK_URL environment variable not set")
        return False
    
    # Determine color based on status
    color = '#36a64f' if status == 'success' else '#ff0000'
    status_emoji = '✅' if status == 'success' else '❌'
    
    # Get GitHub context from environment
    repo = os.environ.get('GITHUB_REPOSITORY', 'Unknown Repository')
    branch = os.environ.get('GITHUB_REF', 'unknown branch').split('/')[-1]
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:8]
    actor = os.environ.get('GITHUB_ACTOR', 'Unknown User')
    workflow = os.environ.get('GITHUB_WORKFLOW', '')
    run_id = os.environ.get('GITHUB_RUN_ID')
    run_number = os.environ.get('GITHUB_RUN_NUMBER')
    run_url = None
    if repo and run_id:
        run_url = f"https://github.com/{repo}/actions/runs/{run_id}"
    
    # Build the Slack message
    fields = [
        {"title": "Repository", "value": repo, "short": True},
        {"title": "Branch", "value": branch, "short": True},
        {"title": "Commit", "value": f"`{commit_sha}`", "short": True},
        {"title": "Triggered by", "value": actor, "short": True},
        {"title": "Timestamp", "value": datetime.now().isoformat(), "short": False}
    ]

    if workflow:
        fields.insert(0, {"title": "Workflow", "value": workflow, "short": True})
    if run_number:
        fields.insert(1, {"title": "Run #", "value": run_number, "short": True})
    if run_url:
        # Add a clickable run link in the attachment
        attachment = {
            "color": color,
            "title": f"{status_emoji} CI Pipeline {status.upper()}",
            "title_link": run_url,
            "text": message,
            "fields": fields,
            "footer": "To-Do List App CI",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
        }
    else:
        attachment = {
            "color": color,
            "title": f"{status_emoji} CI Pipeline {status.upper()}",
            "text": message,
            "fields": fields,
            "footer": "To-Do List App CI",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
        }

    slack_message = {"attachments": [attachment]}
    
    # Send the message
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(slack_message),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✓ Slack notification sent successfully")
            return True
        else:
            print(f"✗ Failed to send Slack notification: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error sending Slack notification: {str(e)}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Send Slack notification for CI pipeline')
    parser.add_argument('--status', required=True, choices=['success', 'failure'],
                       help='Build status')
    parser.add_argument('--message', required=True, help='Message to send')
    
    args = parser.parse_args()
    
    success = send_slack_notification(args.status, args.message)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
