#!/usr/bin/env python3
"""
Email notification script for CI pipeline
Sends test results and build status via email
"""

import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email_notification(status, branch):
    """
    Send an email notification
    
    Args:
        status (str): 'success' or 'failure'
        branch (str): Git branch name
    """
    # Get email configuration from environment variables
    email_from = os.environ.get('EMAIL_FROM')
    email_password = os.environ.get('EMAIL_PASSWORD')
    email_to = os.environ.get('EMAIL_TO')
    
    # Use Gmail SMTP by default, but allow override
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    
    if not all([email_from, email_password, email_to]):
        print("Warning: Email configuration not complete. Set EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO")
        return False
    
    # Get GitHub context from environment
    repo = os.environ.get('GITHUB_REPOSITORY', 'Unknown Repository')
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:8]
    actor = os.environ.get('GITHUB_ACTOR', 'Unknown User')
    
    # Determine email content based on status
    is_success = status.lower() == 'success'
    subject_emoji = '✅' if is_success else '❌'
    subject = f"{subject_emoji} CI Pipeline {status.upper()} - {repo}"
    
    # Build email body
    if is_success:
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 5px; overflow: hidden;">
                    <div style="background-color: #36a64f; color: white; padding: 20px;">
                        <h2 style="margin: 0;">✅ CI Pipeline Passed</h2>
                    </div>
                    <div style="padding: 20px;">
                        <p><strong>Repository:</strong> {repo}</p>
                        <p><strong>Branch:</strong> {branch}</p>
                        <p><strong>Commit:</strong> <code>{commit_sha}</code></p>
                        <p><strong>Triggered by:</strong> {actor}</p>
                        <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
                        
                        <h3 style="color: #36a64f;">Test Results</h3>
                        <p>✅ All unit tests passed</p>
                        <p>✅ All integration tests passed</p>
                        <p>✅ Code coverage report generated</p>
                        
                        <p style="margin-top: 30px; color: #666; font-size: 12px;">
                            This is an automated message from the CI/CD pipeline.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
    else:
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 5px; overflow: hidden;">
                    <div style="background-color: #ff0000; color: white; padding: 20px;">
                        <h2 style="margin: 0;">❌ CI Pipeline Failed</h2>
                    </div>
                    <div style="padding: 20px;">
                        <p><strong>Repository:</strong> {repo}</p>
                        <p><strong>Branch:</strong> {branch}</p>
                        <p><strong>Commit:</strong> <code>{commit_sha}</code></p>
                        <p><strong>Triggered by:</strong> {actor}</p>
                        <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
                        
                        <h3 style="color: #ff0000;">Action Required</h3>
                        <p>One or more tests failed. Please review the build logs and fix the issues.</p>
                        
                        <p style="margin-top: 30px; color: #666; font-size: 12px;">
                            This is an automated message from the CI/CD pipeline.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        
        # Attach HTML body
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server and send email
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        
        if smtp_port == 465:
            # Use SSL
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(email_from, email_password)
                server.send_message(msg)
        else:
            # Use TLS
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_from, email_password)
                server.send_message(msg)
        
        print(f"✓ Email notification sent to {email_to}")
        return True
        
    except Exception as e:
        print(f"✗ Error sending email notification: {str(e)}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Send email notification for CI pipeline')
    parser.add_argument('--status', required=True, choices=['success', 'failure'],
                       help='Build status')
    parser.add_argument('--branch', default='main', help='Git branch name')
    
    args = parser.parse_args()
    
    success = send_email_notification(args.status, args.branch)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
