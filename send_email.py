import os
import boto3
from botocore.exceptions import ClientError


def send_email(recipient, sender, subject, cc, bcc, reply_to, body='', html_body=''):
    CHARSET = "UTF-8"

    client = boto3.client(
        "ses",
    )

    if html_body.strip() == '':
        message_body = {
            "Text": {
                "Charset": CHARSET,
                "Data": body,
            },
        }
    else:
        message_body = {
            "Html": {
                "Charset": CHARSET,
                "Data": html_body,
            },
            "Text": {
                "Charset": CHARSET,
                "Data": body,
            },
        }

    if recipient.strip() == "":
        recipient_list = []
    else:
        recipient_list = recipient.split(",")

    if cc.strip() == "":
        cc_list = []
    else:
        cc_list = cc.split(",")

    if bcc.strip() == "":
        bcc_list = []
    else:
        bcc_list = bcc.split(",")

    if reply_to.strip() == "":
        reply_to_list = []
    else:
        reply_to_list = reply_to.split(",")

    try:
        response = client.send_email(

            Destination={
                "ToAddresses": recipient_list,
                'CcAddresses': cc_list,
                'BccAddresses': bcc_list
            },
            Message={
                "Body": message_body,
                "Subject": {
                    "Charset": CHARSET,
                    "Data": subject,
                },
            },
            ReplyToAddresses=reply_to_list,
            Source=sender,
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return response["MessageId"]