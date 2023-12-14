from admin.mailing_list import Mailing_Clients

from main import app

with app.app_context():
    # Mailing_Clients().start_mailing_service()


    Mailing_Clients().send_confirmation_email('webcroz03@gmail.com', 'https://www.google.com/')
