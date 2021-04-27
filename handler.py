import json


def send_email(event, context):
    from send_email import send_email
    event_json = json.loads(event["body"])

    recipient = event_json["recipient"]
    sender = event_json["sender"]
    subject = event_json["subject"]
    cc = event_json.get("cc", "")
    bcc = event_json.get("bcc", "")
    reply_to = event_json.get("reply_to", "")
    body = event_json["body"]
    html_body = event_json["html_body"]

    message_id = send_email(
        recipient=recipient,
        sender=sender,
        subject=subject,
        body=body,
        html_body=html_body,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to
    )

    response = {
        "statusCode": 200,
        "body": "Message: {} is sent successfully".format(message_id)
    }

    return response
