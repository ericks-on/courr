from datetime import datetime
from flask_mail import Message
def send_order_notification_email(mail, user_email, order):
    """Sends an email notification to the user about the created order."""
    # Format the email subject
    subject = f"Order Created - {order.id}"

    # Format the email body
    body = f"""
    Dear Customer,

    Your order has been successfully created with the following details:

    Order ID: {order.id}
    Pickup Warehouse: {order.pickup}
    Delivery Warehouse: {order.delivery}
    Time Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Please take your package to the warehouse for further processing, such as measuring.

    Thank you for choosing our service.

    Best regards,
    Your Company Name
    """

    # Create the message
    msg = Message(subject, recipients=[user_email], body=body)

    # Send the email
    mail.send(msg)


def send_order_update_notification(mail, user_email, order, changes):
    """Sends an email notification to the user about the updated order."""
    # Format the email subject
    subject = f"Order Updated - {order.id}"

    # Format the email body
    body = f"""
    Dear Customer,

    Your order (ID: {order.id}) has been updated with the following changes:

    """

    # Add changes to the email body
    for key, value in changes.items():
        if key == 'status':
            body += f"Status: {value}\n"
        elif key == 'weight':
            body += f"Weight: {value} kg\n"
        elif key == 'dimensions':
            body += f"Dimensions: {value}\n"

    # Add timestamp
    body += f"\nTime of Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    # Add instructions or additional details
    body += """
    Please review the updated details and contact us if you have any questions.

    Thank you for choosing our service.

    Best regards,
    Your Company Name
    """

    # Create the message
    msg = Message(subject, recipients=[user_email], body=body)

    # Send the email
    mail.send(msg)