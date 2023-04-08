import smtplib
from grocery_list_actions import get_menu_items_week
from email.mime.text import MIMEText

def send_email(menu):

    sender = 'sender_email'
    receivers = ['receiver_1', 'receiver_2']

    msg = MIMEText(menu)
    msg['Subject'] = "Weekly Menu"
    msg['From'] = "Do-Not-Reply"
    msg['To'] = ', '.join(receivers)


    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("gmail_id", "super_secure_pass")
        s.sendmail(sender, receivers, msg.as_string())
        print ("Successfully sent email")
        #Terminating the session
        s.quit()
    except SMTPException:
        print ("Error: unable to send email")




if __name__ == "__main__":
    menu_list = get_menu_items_week()
    menu = f"""
    Saturday: {menu_list[0]}
    Sunday: {menu_list[1]}
    Monday: {menu_list[2]}
    Tuesday: {menu_list[3]}
    Wednesday: {menu_list[4]}
    Thursday: Takeout
    Friday: Leftovers
    """