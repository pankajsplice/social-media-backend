import paypalrestsdk
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from local_mingle_backend import settings
from rest_framework.views import APIView
from event.models import Subscription
from rest_framework.response import Response
from payment.models import Customer
from payment.serializers import CustomerSerializer
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
                    return Response(
                        {'error': 'subscription with the name' f'{create_product["name"]}' 'is not defined'})
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
                if product['name'] == 'Bronze':
                    data = {"product_id": product['id'], "name": "Bronze",
                            "description": "Bronze basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "MONTH", "interval_count": 1},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "20.99", "currency_code": "USD"}}
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

                elif product['name'] == 'Silver':
                    data = {"product_id": product['id'], "name": "Silver",
                            "description": "Silver basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "MONTH", "interval_count": 3},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "45.99", "currency_code": "USD"}}
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
                    data = {"product_id": product["id"], "name": "Gold",
                            "description": "Gold basic plan", "status": "ACTIVE",
                            "billing_cycles": [{"frequency": {"interval_unit": "YEAR", "interval_count": 1},
                                                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                                                "pricing_scheme": {
                                                    "fixed_price": {"value": "64.99", "currency_code": "USD"}}
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

    # permission_classes = (AllowAny,)

    def get(self, request, format=None):
        paypal_customer = Customer.objects.filter(user_id=request.user.id, source='paypal')
        serializer = CustomerSerializer(paypal_customer, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_id = request.data.get('user', None)
        if user_id:
            try:
                paypal_customer = Customer.objects.get(user_id=user_id, source='paypal', status='ACTIVE')
                if paypal_customer.status == 'ACTIVE':
                    return Response({'info': "You have already subscribed"})
            except:
                subscription_id = request.data['subscription']
                source = request.data['source']
                if subscription_id:
                    subscription = Subscription.objects.get(id=subscription_id)
                    data = {'plan_id': subscription.paypal_plan_id}
                    create_subscription = paypal_api.post("/v1/billing/subscriptions", data)
                    serializer = CustomerSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        payment_link = None
                        status = None
                        serializer.save(user_id=user_id, third_party_subscription=create_subscription['id'],
                                        status=create_subscription['status'], source=source)
                        for links in create_subscription['links']:
                            if links['rel'] == 'approve':
                                payment_link = links
                        status = create_subscription['status']
                        return Response({'data': {'payment_link': payment_link, 'status': status}})
                else:
                    return Response({'error': "Need to pass subscription in payload"})

        else:
            return Response({'error': "Need to pass user in payload"})


class GetPaypalPaymentStatus(APIView, PageNumberPagination):

    # permission_classes = (AllowAny,)

    def get(self, request):
        user_id = request.query_params.get("user", None)
        if user_id:
            try:
                paypal = Customer.objects.get(user_id=user_id, source='paypal')
                update_paypal_customer_status = Customer.objects.filter(user_id=user_id)
                get_subscription = paypal_api.get("/v1/billing/subscriptions/" + paypal.third_party_subscription)
                update_paypal_customer_status.update(status=get_subscription['status'])
                page = self.paginate_queryset(update_paypal_customer_status, request)
                serializer = CustomerSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            except Exception as e:
                return Response({'error': 'There is no paypal payment for this user'})

        else:
            return Response({'error': 'Please add existing user id in query_params to get status of paypal payment'})


class CancelPaypalSubscription(APIView):
    def get(self, request):
        user_id = request.user.id
        if user_id:
            try:
                data = {"status": "CANCELLED"}
                paypal = Customer.objects.get(user_id=user_id, source='paypal')
                update_paypal_customer_status = Customer.objects.filter(user_id=user_id, source='paypal')
                cancel_subscription = paypal_api.patch("/v1/billing/subscriptions/" + paypal.third_party_subscription,
                                                       data)
                print(cancel_subscription)
                update_paypal_customer_status.update(status='CANCELLED')
                page = self.paginate_queryset(update_paypal_customer_status, request)
                serializer = CustomerSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            except Exception as e:
                return Response({'error': 'There is no paypal based subscription for this user'})

        else:
            return Response({'error': 'Please add existing user token to cancel the paypal subscription'})