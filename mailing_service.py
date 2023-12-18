from admin.mailing_list import Mailing_Clients

from main import app

with app.app_context():
    mailing_service = Mailing_Clients()
    mailing_service.get_all_portal_data()
    mailing_service.start_mailing_service()


