from rest_framework.views import APIView
import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from payment.models import Customer
from event.models import Subscription
from payment.serializers import CustomerSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateProductApi(APIView):

    def get(self, *args, **kwargs):
        product = ['Silver', 'Gold', 'Platinum']
        get_product = stripe.Product.list(limit=3)
        if get_product.is_empty:
            for prod in product:
                stripe.Product.create(name=prod)
            get_product = stripe.Product.list(limit=3)
        get_price = stripe.Price.list(limit=3)
        if get_price.is_empty:
            for data in get_product.data:
                if data.name == 'Silver':
                    stripe.Price.create(
                        unit_amount=1500,
                        currency="usd",
                        recurring={"interval": "month", "interval_count": 1},
                        product=data.id,
                    )
                if data.name == 'Gold':
                    stripe.Price.create(
                        unit_amount=5000,
                        currency="usd",
                        recurring={"interval": "month", "interval_count": 6},
                        product=data.id,
                    )
                if data.name == 'Platinum':
                    stripe.Price.create(
                        unit_amount=6000,
                        currency="usd",
                        recurring={"interval": "year"},
                        product=data.id,
                    )
        return Response({'data': get_product.data})


class GetStripePriceApi(APIView):
    def get(self, *args, **kwargs):
        get_price = stripe.Price.list(limit=3)
        product = []
        data = {}
        for price in get_price:
            data['product_id'] = price.product
            data['price_id'] = price.id
            product.append(data.copy())
        print(product)
        for prod in product:
            individual_prod = stripe.Product.retrieve(prod.get('product_id'))
            individual_price = stripe.Price.retrieve(prod.get('price_id'))
            if individual_prod.name == 'Silver':
                subscription = Subscription.objects.filter(name='Silver')
                if subscription:
                    for subscription_instance in subscription:
                        if subscription_instance.stripe_product_id is None or subscription_instance.stripe_price_id is None:
                            Subscription.objects.update(id=subscription.id, stripe_product_id=individual_prod.id,
                                                        stripe_price_id=individual_price.id)
                else:
                    Subscription.objects.create(name='Silver', price=15.00, validity=1,
                                                stripe_product_id=individual_prod.id,
                                                stripe_price_id=individual_price.id)
            if individual_prod.name == 'Gold':
                subscription = Subscription.objects.filter(name='Gold')
                if subscription:
                    for subscription_instance in subscription:
                        if subscription_instance.stripe_product_id is None or subscription_instance.stripe_price_id is None:
                            Subscription.objects.update(id=subscription.id, stripe_product_id=individual_prod.id,
                                                        stripe_price_id=individual_price.id)
                else:
                    Subscription.objects.create(name='Gold', price=50.00, validity=6,
                                                stripe_product_id=individual_prod.id,
                                                stripe_price_id=individual_price.id)

            if individual_prod.name == 'Platinum':
                subscription = Subscription.objects.filter(name='Platinum')
                if subscription:
                    for subscription_instance in subscription:
                        if subscription_instance.stripe_product_id is None or subscription_instance.stripe_price_id is None:
                            Subscription.objects.update(id=subscription.id, stripe_product_id=individual_prod.id,
                                                        stripe_price_id=individual_price.id)
                else:
                    Subscription.objects.create(name='Platinum', price=60.00, validity=12,
                                                stripe_product_id=individual_prod.id,
                                                stripe_price_id=individual_price.id)

        return Response({'data': get_price.data})


class StripeCustomerApiView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        stripe_customer = Customer.objects.all()
        serializer = CustomerSerializer(stripe_customer, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            email = request.data['email']
            user = request.data.get('user', None)
            user_exist = User.objects.get(id=user)
            full_name = f'{user_exist.first_name}  {user_exist.last_name}'
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']
            postal_code = request.data['postal_code']
            address = request.data['address']
            source = request.data['source']
            subscription_id = request.data['subscription']
            if email and subscription_id:
                subscription = Subscription.objects.get(id=subscription_id)
                create_customer = stripe.Customer.create(
                    email=email, name=full_name,
                    address={"city": city, 'state': state, 'country': country, 'line1': address,
                             'postal_code': postal_code},
                                )
                create_subscription = stripe.Subscription.create(
                    customer=create_customer.id,
                    items=[
                        {"price": subscription.stripe_price_id},
                    ],
                    payment_behavior='default_incomplete',
                    expand=['latest_invoice.payment_intent'],
                )
                serializer = CustomerSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(customer=create_customer.id, third_party_subscription=create_subscription.id,
                                    status=create_subscription.status, source=source)

                    return Response({'data': create_subscription})

            else:
                return Response({'error': 'fields can not be blank', 'data': []})
        except Exception as e:
            print(e)
            pass

        return Response({'error': 'something went wrong', 'data': []})


class StripeCustomerViewSets(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id", None)
        if user_id is None:
            queryset = Customer.objects.none()
        else:
            queryset = Customer.objects.filter(user=user_id, source='stripe')
        return queryset


class ConfirmPaymentIntent(APIView):
    def post(self, request, format=None):
        payment_intent_id = request.data['payment_intent_id']
        number = request.data['number']
        exp_month = request.data['expMonth']
        exp_year = request.data['expYear']
        cvc = request.data['cvc']
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )
        if payment_method:
            payment_method_id = payment_method.id

            # To create a PaymentIntent for confirmation

            confirm_payment_intent = stripe.PaymentIntent.confirm(
                                        payment_intent_id,
                                        payment_method=payment_method_id)
            get_payment = stripe.PaymentIntent.retrieve(confirm_payment_intent.id)
            stripe_customer = Customer.objects.filter(customer=get_payment['customer'])
            stripe_customer.update(status=get_payment['status'])
            return Response({'data': confirm_payment_intent})

        else:
            return Response({'data': [], 'error': "Payment can not be proceeded"})


class GetPaymentDetails(APIView):

    def post(self, request, format=None):
        payment_id = request.data['payment']
        get_payment = stripe.PaymentIntent.retrieve(payment_id)
        stripe_customer = Customer.objects.filter(customer=get_payment['customer'])
        stripe_customer.update(status=get_payment['status'])
        return Response({'data': get_payment})


class CancelSubscription(APIView):
    def post(self, request, format=None):
        subscription_id = request.data['subscription']
        if subscription_id:
            stripe_customer = Customer.objects.get(subscription_id=subscription_id, source='stripe')
            get_current_subscription_id = stripe_customer.strip_subscription
            cancel_subscription = stripe.Subscription.delete(get_current_subscription_id)
            subscription_instance = Subscription.objects.get(id=subscription_id)
            subscription_instance.status = cancel_subscription.status
            subscription_instance.save()
            return Response({'data': cancel_subscription})
        else:
            return Response({'data': [], 'error': 'please provide subscription id'})


class GetLocalMinglePaymentDetails(APIView):

    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        email = request.data.get('email', None)
        if email:
            customer = Customer.objects.filter(email=email, status='succeeded')
            if customer:
                return Response({'payment': True})
            else:
                get_user = User.objects.filter(email=email).last()
                if get_user:
                    paypal_customer = Customer.objects.filter(user=get_user.id, status='ACTIVE')
                    if paypal_customer:
                        return Response({'payment': True})
                    else:
                        return Response({'payment': False})
                else:
                    return Response({'payment': False})
        else:
            return Response({'payment': False})


class CustomerViewSets(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id", None)
        if user_id is None:
            queryset = Customer.objects.none()
        else:
            queryset = Customer.objects.filter(user=user_id)
        return queryset
