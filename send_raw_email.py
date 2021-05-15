def send_raw_email(recipient, sender, subject, cc, bcc, reply_to, body="", html_body="", attachment=""):
    import os
    import boto3
    from botocore.exceptions import ClientError
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

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

    # The full path to the file that will be attached to the email.
    ATTACHMENT = attachment

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = body

    if html_body is None or html_body.strip() == '':
        BODY_HTML = None
    else:
        BODY_HTML = html_body

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses')

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = subject
    msg['From'] = sender
    if recipient.strip() != "":
        msg['To'] = recipient
    if cc.strip() != "":
        msg['cc'] = cc
    if bcc.strip() != "":
        msg['bcc'] = bcc
    if reply_to.strip() != "":
        msg['reply-to'] = reply_to

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    if BODY_HTML:
        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg_body.attach(htmlpart)

    msg.attach(msg_body)

    # Define the attachment part and encode it using MIMEApplication.
    if attachment.strip() != "":
        att = MIMEApplication(open(ATTACHMENT, 'rb').read())
        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ATTACHMENT))
        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.

        # Add the attachment to the parent container.
        msg.attach(att)

    try:
        # Provide the contents of the email.
        response = client.send_raw_email(
            Source=sender,
            Destinations=recipient_list + cc_list + bcc_list,
            RawMessage={
                'Data': msg.as_string(),
            },
            # If you are not using config set
            # ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response["MessageId"]
