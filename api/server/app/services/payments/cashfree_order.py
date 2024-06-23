from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.utils.service_request import ServiceResult
from app.utils.hash import hash_password, hmac_sha256

from fastapi import HTTPException
from typing import List, Any , Optional, Union
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

from app.schemas.order import OrderCreate, OrderBase, OrderAmount,OrderCapture
from app.schemas.admit_card import AdmitCard
from app.schemas.profile import ProfileOrderCreate
from app.models.championship import Championship as ChampionShipModel
from app.models.admit_card import AdmitCard as AdmitCardModel
from app.services.championship import ChampionshipCRUD
from app.services.profile import ProfileCRUD
from app.services.admit_card import AdmitCardCRUD


import logging
import asyncio
import datetime
import os
import json
import random
import string
import phonenumbers
import shortuuid


logger = logging.getLogger(__name__)

Cashfree.XClientId = os.getenv('CASHFREE_KEY_ID')
Cashfree.XClientSecret = os.getenv('CASHFREE_KEY_SECRET')
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"

class CashFreeOrderService(AppService):

    async def calculate_order(self, order: OrderCreate) -> ServiceResult:
        """
        Calculate order.
        """
        try:
            #calculate the amount
            championship = await  ChampionshipCRUD(self.db).get(ChampionShipModel, order.championship_id)

            order_amount = championship.primary_price + ((len(order.examination_ids) -1) * championship.secondary_price) if len(order.examination_ids) > 1 else championship.primary_price
            order_base = OrderAmount(
                amount = "{:.2f}".format(order_amount/100) ,
                notes = f'Order for championship {order.championship_id} with {len(order.examination_ids)} examinations.'
            )
            return ServiceResult(order_base)
        except Exception as e:
            logger.error(f'Error calculating order: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"Error": f"Error calculating order: {str(e)}"}))
        
    async def _create_order_id(self, name:str, phone:int, email:str)-> str:

        cleaned_name = ''.join(e for e in name if e.isalnum())
        last_four_digits = phone[-4:]  
        first_five_chars = email[:5]
        order_id = cleaned_name[:3].upper() + last_four_digits + first_five_chars.upper()
        return order_id
    
    async def _validate_phone_number(phone_number):
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        
    async def _cashfree_order(self, order: OrderCreate, profile: ProfileOrderCreate):
            try:
                order_id, order_amount, customer_details = await self._prepare_order(order, profile)
                create_order_request = self._create_order_request(order_id, order_amount, customer_details, order)

                api_response = self._create_cashfree_order(create_order_request)

                self._cache_order_data(order_id, order, profile)
                
                return api_response.data
            except Exception as e:
                logger.error(f'CashFree:: Error creating order: {str(e)}')
                raise ServiceResult(AppException.RequestOrderCreateItem({"ERROR": f"Please Check Your Details!"}))

    async def _prepare_order(self, order: OrderCreate, profile: ProfileOrderCreate):
        championship = await self.calculate_order(order)
        order_amount = championship.value.amount
        order_id = f'order_{shortuuid.ShortUUID().random(length=20)}'
        customer_id = await hash_password(profile.phone)

        customer_details = self._create_customer_details(customer_id, profile)

        return order_id, order_amount, customer_details

    def _create_customer_details(self, customer_id: str, profile: ProfileOrderCreate):
        customer_details = CustomerDetails(
            customer_id=str(customer_id),
            customer_phone=profile.phone
        )
        customer_details.customer_name = profile.name
        customer_details.customer_email = profile.email
        return customer_details

    def _create_order_request(self, order_id: str, order_amount: float, customer_details: CustomerDetails, order: OrderCreate):
        create_order_request = CreateOrderRequest(
            order_id=order_id,
            order_amount=float(order_amount),
            order_currency="INR",
            customer_details=customer_details
        )

        order_meta = OrderMeta()
        order_meta.return_url = None
        create_order_request.order_meta = order_meta
        create_order_request.order_note = f'order#{datetime.datetime.now().strftime("%H:%M:%S")}'
        create_order_request.order_tags = {
            "championship": str(order.championship_id),
            "examination_ids": ",".join(map(str, order.examination_ids))
        }

        return create_order_request

    def _create_cashfree_order(self, create_order_request: CreateOrderRequest):
        return Cashfree().PGCreateOrder(x_api_version, create_order_request, None, None)

    def _cache_order_data(self, order_id: str, order: OrderCreate, profile: ProfileOrderCreate):
        self.cache.set(order_id, json.dumps({
            'championship_id': order.championship_id,
            'examination_ids': order.examination_ids,
            'name': profile.name,
            'phone': profile.phone,
            'email': profile.email
        }))

    async def create_order(self, order: OrderCreate, profile : ProfileOrderCreate) -> ServiceResult:
        """
        Create new order.
        """
        try:

            championship_detail =  await ChampionshipCRUD(self.db).get(ChampionShipModel, int(order.championship_id))

            if len(order.examination_ids) > championship_detail.max_exams:
                return ServiceResult(AppException.RequestOrderGetItem( {"ERROR": f"You can only select {championship_detail.max_exams} examination(s)"}))
    
            cashfree_res = await self._cashfree_order(order, profile)
            
            return ServiceResult({'payment_session_id':cashfree_res.payment_session_id, 'order_id': cashfree_res.order_id})
        except Exception as e:
            logger.error(f'Error creating order: {str(e)}')
            raise ServiceResult(AppException.RequestOrderCreateItem( {"ERROR": f"Please Check Your Details"}))

    async def capture_order(self, order_id: str) -> ServiceResult:
        try:
            order = self._get_order_from_cache(order_id)
            if order is None:
                return ServiceResult(AppException.RequestCreateItem({"ERROR": "Order not found"}))

            order, examination_ids = self._parse_order(order)

            api_response = self._fetch_order_payments(order_id)

            successful_transaction = next((txn for txn in api_response if txn.payment_status == 'SUCCESS'), None)

            if successful_transaction:
                return await self._handle_successful_payment(order_id, order, examination_ids)
            
            latest_transaction = max(api_response, key=lambda txn: txn.payment_time, default=None)

            if latest_transaction:
                if latest_transaction.payment_status == 'PENDING':
                    return await self._handle_pending_payment(order_id)
                else:
                    return self._handle_failed_payment(latest_transaction.payment_status)
            else:
                return self._handle_failed_payment("No transactions found")
        except Exception as e:
            logger.error(f'Error capturing order: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem({"ERROR": f"Error capturing order: {str(e)}"}))


    def _get_order_from_cache(self, order_id: str):
        return self.cache.get(order_id)

    def _parse_order(self, order):
        order = json.loads(order)
        examination_ids = order['examination_ids']
        return order, examination_ids

    def _fetch_order_payments(self, order_id: str):
        return Cashfree().PGOrderFetchPayments(x_api_version, order_id, None).data

    async def _handle_successful_payment(self, order_id: str, order, examination_ids:list):
        logger.info(f'Order captured: {order_id}')

        password = self._generate_random_password()
        profile = await ProfileCRUD(self.db).create_inital_profile(order)
        if hasattr(profile, 'error'):
            return ServiceResult(f'Error creating profile: {profile.error}')

        admitcard = await self.create_admit_card(order_id, order, examination_ids, password, profile.id)
        return ServiceResult(admitcard)

    async def _handle_pending_payment(self, order_id: str):
        logger.error(f'Payment Pending for: {order_id}')
        raise HTTPException(status_code=202, detail=f'Payment Pending for: {order_id}')

    def _handle_failed_payment(self, payment_status: str):
        logger.error(f'Payment failed with status: {payment_status}')
        raise HTTPException(status_code=400, detail=f'Payment failed with status: {payment_status}')

    def _generate_random_password(self):
        return ''.join(random.choices(string.digits, k=6))

    async def create_admit_card(self, order_id: str, order, examination_ids, password, profile_id: int):
        password_hash = await hash_password(password)
        admitcard_data = {
            "order_id": order_id,
            "password_hash": password_hash
        }
        _admitcard = await AdmitCardCRUD(self.db).create(
            profile_id=profile_id, 
            championship_id=int(order['championship_id']), 
            examination_ids=order['examination_ids'], 
            item=admitcard_data
        )
        logger.info(f'Admit card created: {str(_admitcard)}')
        return AdmitCard(
            id=_admitcard.id,
            order_id=_admitcard.order_id,
            password=password,
            championship_id=_admitcard.championship_id,
            examination_ids=_admitcard.examination_ids,
            profile_id=_admitcard.profile_id
        )