import paypalrestsdk
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from local_mingle_backend import settings
from rest_framework.views import APIView
from event.models import Subscription
from rest_framework.response import Response
from payment.models import PaypalCustomer
from payment.serializers import PaypalCustomerSerializer
from rest_framework.pagination import PageNumberPagination

# *** paypal rest-sdk api settings start ***

paypal_api = paypalrestsdk.Api({
    "mode": 'sandbox',
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})
# *** paypal rest-sdk api settings end ***


class PaypalProductListCreateApi(APIView):

    def get(self, request):
        res = paypal_api.get("v1/catalogs/products")
        get_products = res.get('products', '')
        if not get_products:
            for product in settings.LOCAL_MINGLE_PRODUCT_LIST:
                data = {"name": product, "description": 'Get permitted insights as per product' f' {product} .'}
                create_product = paypal_api.post("/v1/catalogs/products", data)
                get_subscription = Subscription.objects.filter(name=create_product['name'])
                if get_subscription:
                    get_subscription.update(paypal_product_id=create_product['id'])
                else:
                    return Response({'error': 'subscription with the name' f'{create_product["name"]}' 'is not defined'})
        else:
            for product in get_products:
                get_subscription = Subscription.objects.filter(name=product['name'])
                if get_subscription:
                    get_subscription.update(paypal_product_id=product['id'])
                else:
                    return Response({'error': 'subscription with the name' f'{product["name"]}' 'is not defined'})
        return Response({'data': get_products})


class PaypalPlanListCreateApi(APIView):

    def get(self, request):
        res = paypal_api.get("/v1/billing/plans")
        get_plans = res.get('plans', '')
        if not get_plans:
            res = paypal_api.get("v1/catalogs/products")
            get_products = res.get('products', '')
            for product in get_products:
                if product['name'] == 'Silver':
                    data = {"product_id": product['id'], "name": "Silver",
                            "description": "Silver basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "MONTH", "interval_count": 1},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "20", "currency_code": "USD"}}
                                                }],
                            "payment_preferences": {"auto_bill_outstanding": 'true',
                                                    "setup_fee": {"value": "0", "currency_code": "USD"},
                                                    "setup_fee_failure_action": "CONTINUE",
                                                    "payment_failure_threshold": 3
                                                    },
                            }
                    create_plan = paypal_api.post("/v1/billing/plans", data)
                    get_subscription = Subscription.objects.filter(name=product['name'])
                    if get_subscription:
                        get_subscription.update(paypal_plan_id=create_plan['id'])
                    else:
                        return Response(
                            {'error': 'subscription with the name' f'{product["name"]}' 'is not defined'})

                elif product['name'] == 'Gold':
                    data = {"product_id": product['id'], "name": "Gold",
                            "description": "Gold basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "MONTH", "interval_count": 6},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "50", "currency_code": "USD"}}
                                                }],
                            "payment_preferences": {"auto_bill_outstanding": 'true',
                                                    "setup_fee": {"value": "0", "currency_code": "USD"},
                                                    "setup_fee_failure_action": "CONTINUE",
                                                    "payment_failure_threshold": 3
                                                    },
                            }
                    create_plan = paypal_api.post("/v1/billing/plans", data)
                    get_subscription = Subscription.objects.filter(name=product['name'])
                    if get_subscription:
                        get_subscription.update(paypal_plan_id=create_plan['id'])
                    else:
                        return Response(
                            {'error': 'subscription with the name' f'{product["name"]}' 'is not defined'})

                else:
                    data = {"product_id": product["id"], "name": "Platinum",
                            "description": "Platinum basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "YEAR", "interval_count": 1},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "60", "currency_code": "USD"}}
                                                }],
                            "payment_preferences": {"auto_bill_outstanding": 'true',
                                                    "setup_fee": {"value": "0", "currency_code": "USD"},
                                                    "setup_fee_failure_action": "CONTINUE",
                                                    "payment_failure_threshold": 3
                                                    },
                            }

                    create_plan = paypal_api.post("/v1/billing/plans", data)
                    get_subscription = Subscription.objects.filter(name=product["name"])
                    if get_subscription:
                        get_subscription.update(paypal_plan_id=create_plan["id"])
                    else:
                        return Response({'error': 'subscription with the name' f'{product["name"]}' 'is not defined'})
        else:
            for plan in get_plans:
                get_subscription = Subscription.objects.filter(name=plan['name'])
                if get_subscription:
                    get_subscription.update(paypal_plan_id=plan['id'])
                else:
                    return Response({'error': 'subscription with the name' f'{plan["name"]}' 'is not defined'})
        return Response({'data': get_plans})


class PaypalSubscriptionApi(APIView):

    def get(self, request, format=None):
        paypal_customer = PaypalCustomer.objects.all()
        serializer = PaypalCustomerSerializer(paypal_customer, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        subscription_id = request.data['subscription']
        if subscription_id:
            subscription = Subscription.objects.get(id=subscription_id)
            data = {'plan_id': subscription.paypal_plan_id}
            create_subscription = paypal_api.post("/v1/billing/subscriptions", data)
            serializer = PaypalCustomerSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                payment_link = None
                status = None
                serializer.save(paypal_subscription=create_subscription['id'],
                                status=create_subscription['status'])
                for links in create_subscription['links']:
                    if links['rel'] == 'approve':
                        payment_link = links
                status = create_subscription['status']
                return Response({'data': {'payment_link': payment_link, 'status': status}})


class GetPaypalPaymentStatus(APIView, PageNumberPagination):
    def get(self, request):
        user_id = request.query_params.get('user_id', '')
        if user_id != '':

            try:
                paypal = PaypalCustomer.objects.get(user_id=user_id)
                update_paypal_customer_status = PaypalCustomer.objects.filter(user_id=user_id)
                get_subscription = paypal_api.get("/v1/billing/subscriptions/" + paypal.paypal_subscription)
                update_paypal_customer_status.update(status=get_subscription['status'])
                page = self.paginate_queryset(update_paypal_customer_status, request)
                serializer = PaypalCustomerSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            except:
                return Response({'error': 'There is no paypal payment belonging to this user'})

        else:
            return Response({'error': 'Please pass user_id to get status of paypal payment'})

