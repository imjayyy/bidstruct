
import stripe
from models.connection import stripe_customer 

secret_key = 'sk_test_51KD0MlAESz5yHcF4WSF2htUZGKmOCwWNLsOAd3mzlX4SIGnqkV6839xl1YL2dQPKwMUTVcycFMVcFFGU9EsyPRgV004xGNztBV'
publishable_key = "pk_test_51KD0MlAESz5yHcF4dVIQJ0u0ZCyRAdvpDB4o1nSjUQOipewZnqHcAyzC4KSgx8wEbbzKpvoLkYOsA3EugX1LGvI200N0maksuc"
price_id = 'price_1O2JXNAESz5yHcF4AYppHOIv'
endpoint_secret = 'whsec_NLPOlMKMzH8NBMAYmDNQLihgmHNGkLoE'


stripe_keys = {
    "secret_key": secret_key,
    "publishable_key": publishable_key,
    "price_id" : price_id,
    "endpoint_secret" : endpoint_secret
}

stripe.api_key = stripe_keys["secret_key"]
domain_url = 'http://localhost:5000/'


def checkout_function(domain_url, user_email, quantity):
    checkout_session = stripe.checkout.Session.create(
    client_reference_id=user_email,
    success_url="https://" + domain_url + "/sucess",
    cancel_url="https://" + domain_url + "/cancel",
    payment_method_types=["card"],
    mode="subscription",
    line_items=[
        {
            "price": stripe_keys["price_id"],
            "quantity" : quantity
        }
    ],
    custom_fields = [ {'key': "quantity",
                      "label" : {"custom": quantity, "type" : "custom"},
                      "type" : "text",
                      'text': {"maximum_length": None,
                               "minimum_length": None,
                            #    "value": str(quantity)
                                },
                    "optional" : True                      
                      }
                      
                      ]
    )
    return checkout_session


def get_products_list():
    RESPONSE = stripe.Product.search(
  query="active:'true'",
)
    
    for data in RESPONSE['data']:
        print(data['default_price'])
        price_deatils = stripe.Price.retrieve(data['default_price'])
        data["price_deatils"] = {
            'unit_amount' : price_deatils['unit_amount'],
            'unit_amount_decimal' : price_deatils['unit_amount_decimal']
            }


    return RESPONSE



def handle_checkout_session(session):
    # here you should fetch the details from the session and save the relevant information
    # to the database (e.g. associate the user with their subscription)
    stripe_customer.insert_one(session)
    print("Subscription was successful.")


def fetch_subscription_data(client_reference_id):
    customer = stripe_customer.find_one({"client_reference_id": client_reference_id})

    # if record exists, add the subscription info to the render_template method
    if customer:
        subscription = stripe.Subscription.retrieve(customer['subscription'])
        product = stripe.Product.retrieve(subscription.plan.product)
        context = {
            "subscription": subscription,
            "product": product,
        }
        return(context)

    else:
        context = {
            "subscription": None,
            "product": None,
        }
        return(context)


def get_all_customers():
    list_ = stripe.Subscription.list()
    return list_

def get_recent_transactions():
    return stripe.Invoice.list(limit=12)

    
