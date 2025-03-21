from datetime import datetime
from flask_mail import Message
from flask import render_template
def send_order_notification_email(mail, user_email, order, pickup_warehouse, delivery_warehouse):
    """Sends an email notification to the user about the created order."""
    # Format the email subject
    subject = f"Order Created - {order.id}"

    html_body = render_template('email/order_notification.html',
                               action="successfully created",
                               order_id=order.id,
                               pickup_warehouse=pickup_warehouse,
                               delivery_warehouse=delivery_warehouse,
                               status="Pending",
                               status_class="pending",
                               time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                               is_new_order=True)
    
    msg = Message(subject, recipients=[user_email], html=html_body)

    # Send the email
    mail.send(msg)


def send_order_update_notification(mail, user_email, order, changes):
    """Sends an email notification to the user about the updated order."""


    # Format the email subject
    subject = f"Order Updated - {order.id}"

    # Render the email body from the template
    body = render_template(
        'email/order_update_notification.html',
        order_id=order.id,
        changes=changes,
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    # Create the message
    msg = Message(subject, recipients=[user_email], html=body)


    # Send the email
    mail.send(msg)