import base64
import json
import os
import uuid


def send_email(event, context):
    from send_email import send_email
    from send_raw_email import send_raw_email

    event_json = json.loads(event["body"])

    recipient = event_json["recipient"]
    sender = event_json["sender"]
    subject = event_json["subject"]
    cc = event_json.get("cc", "")
    bcc = event_json.get("bcc", "")
    reply_to = event_json.get("reply_to", "")
    body = event_json["body"]
    html_body = event_json["html_body"]
    attachment_b64 = event_json.get("attachment_b64", "")
    file_name = event_json.get("file_name", "")

    abs_file_path = get_file_path(attachment_b64, file_name)

    if abs_file_path == "":
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
    else:
        message_id = send_raw_email(
            recipient=recipient,
            sender=sender,
            subject=subject,
            body=body,
            html_body=html_body,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachment=abs_file_path,
        )

    response = {
        "statusCode": 200,
        "body": "Message: {} is sent successfully".format(message_id)
    }

    if abs_file_path != "":
        os.system("rm -rf {}".format(abs_file_path))

    return response


def get_file_path(attachment_b64, file_name):
    abs_file_path = ""
    if attachment_b64 != "" and file_name != "":
        folder_name = uuid.uuid4()
        abs_folder_path = "/tmp/{}".format(folder_name)
        os.system("mkdir -p {}".format(abs_folder_path))
        abs_file_path = os.path.join(abs_folder_path, file_name)
        f = open(abs_file_path, "wb")
        f.write(base64.b64decode(attachment_b64.encode("utf-8")))
        f.close()

    return abs_file_path
