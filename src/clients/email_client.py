import json
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any


class EmailClient:
    """
    Loads SMTP credentials and address details from the config file. 
    Provides a send method for delivering plain text emails. 
    """

    def __init__(self, config_path: str = "email_config.json"):
        with open(config_path, "r") as f:
            self.cfg: Dict[str, Any] = json.load(f)

    def send(self, subject: str, body_md: str) -> None:
        """
        Send an email with the loaded configuration.

        Args:
            subject: Subject line for the email
            body_md: Body content to include in the email
        """
        msg = MIMEText(body_md, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = self.cfg["email_from"]
        msg["To"] = self.cfg["email_to"]

        with smtplib.SMTP(self.cfg["smtp_host"], self.cfg["smtp_port"]) as server:
            server.starttls()
            server.login(self.cfg["smtp_user"], self.cfg["smtp_pass"])
            server.sendmail(
                self.cfg["email_from"],
                [self.cfg["email_to"]],
                msg.as_string()
            )
