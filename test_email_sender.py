import os
import sys

# Add current dir to path
sys.path.append(os.getcwd())

from email_sender import send_moderation_report_email

def test_email():
    print("--- Testing Email Sender (Dry Run) ---")
    
    summary = {
        "sync_timestamp": "2026-02-25T12:00:00",
        "total_records_processed": 1500,
        "flagged_entities": 12,
        "false_positive_percentage": "0.8%",
        "execution_time_seconds": 45.5
    }
    
    # Check if credentials are set
    from config import SMTP_USER, SMTP_PASSWORD, EMAIL_RECIPIENTS
    
    print(f"SMTP User: {'Set' if SMTP_USER else 'NOT SET'}")
    print(f"SMTP Pass: {'Set' if SMTP_PASSWORD else 'NOT SET'}")
    print(f"Recipients: {EMAIL_RECIPIENTS}")
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("\nSkipping live send test due to missing credentials.")
        print("Generating HTML preview instead...")
        from email_sender import create_email_body
        html = create_email_body(summary)
        with open("email_preview.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Preview saved to email_preview.html")
        return

    print("\nAttempting to send test email...")
    result = send_moderation_report_email(summary)
    print(f"Result: {result}")

if __name__ == "__main__":
    test_email()
