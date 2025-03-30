# pylogger_slack/slack.py
import os
import warnings
from typing import Any
from datetime import datetime

class SlackNotification:
    def __init__(self, webhook: Any = None, dev: bool = None):
        from pylogger_slack import CONFIG
        self._webhook = (webhook or 
                        CONFIG.get("slack_webhook_url") or 
                        os.getenv("SLACK_WEBHOOK"))
        self._dev = dev if dev is not None else CONFIG.get("dev", True)
        
        if not self._webhook and not self._dev:
            warnings.warn("Slack Webhook URL required in production mode")

    def notify(self, message: str):
        if self._dev:
            print(f"Slack notification (dev mode): {message}")
            return
            
        try:
            from slack_sdk import WebhookClient
            webhook = WebhookClient(self._webhook)
            response = webhook.send(
                text="custom trigger",
                blocks=[
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "Code Anomaly :expressionless:", "emoji": True}
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "*Type:*\nWebhook trigger"},
                            {"type": "mrkdwn", "text": f'*Timestamp:*\n{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'}
                        ]
                    },
                    {
                        "type": "section",
                        "text": {"type": "plain_text", "text": f"*Message*\n{message}"}
                    }
                ]
            )
            if response.status_code != 200:
                warnings.warn(f"Slack notification failed: {response.body}")
        except ImportError:
            warnings.warn("slack_sdk required for notifications: pip install slack-sdk")
        except Exception as e:
            warnings.warn(f"Slack notification failed: {e}")