from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.utils.service_request import ServiceResult
from app.utils.hash import hash_password, hmac_sha256

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

from app.schemas.order import OrderCreate, OrderBase, OrderAmount,OrderCapture
from app.schemas.admit_card import AdmitCard
from app.models.championship import Championship as ChampionShipModel
from app.models.admit_card import AdmitCard as AdmitCardModel
from app.services.championship import ChampionshipCRUD
from app.services.profile import ProfileCRUD
from app.services.admit_card import AdmitCardCRUD


import logging
import requests
import datetime
import os
import json
import random
import string


logger = logging.getLogger(__name__)

class OrderService(AppService):

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
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error calculating order: {str(e)}"}))

    async def create_order(self, order: OrderCreate) -> ServiceResult:
        """
        Create new order.
        """
        try:
            #calculate the amount
            championship = await self.calculate_order(order)
            order_amount = championship.value.amount

            #create order
            payload = {
                "amount": int(order_amount) * 100,
                "currency": "INR",
                "receipt": f'order#{datetime.datetime.now().strftime("%H:%M:%S")}',
                "notes": json.dumps({
                    "championship": str(order.championship_id),
                    "examination_ids": ",".join(map(str, order.examination_ids)),
                })
            }

            championship_detail =  await ChampionshipCRUD(self.db).get(int(payload['notes']['championship']))

            if len(payload['notes']['examination_ids']) > championship_detail.max_exams:
                return ServiceResult(AppException.RequestGetItem( {"ERROR": f"You can only select {championship_detail.max_exams} for this championship"}))

            req = requests.post(
                os.getenv('RAZORPAY_ORDER_URL'),
                auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET')),
                headers={'content-type': 'application/json'},
                json=payload  # Convert payload to JSON
            )
            res = req.json()

            #create OrderBase
            if req.status_code == 200:
                order_base = OrderBase(
                    order_id = str(res['id']),
                    amount = "{:.2f}".format(res['amount']/100),
                    currency = res['currency']
                )
                # add the order to the cache
                self.cache.set( order_base.order_id, json.dumps(payload))
                return ServiceResult(order_base)
            else:
                return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating order: {req.text}"}))
        except Exception as e:
            logger.error(f'Error creating order: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating order: {str(e)}"}))

    async def capture_order(self, order_id: str, order_details: OrderCapture) -> ServiceResult:
        try:
            #get the order from the cache
            order = self.cache.get( order_id)
            if order is None:
                return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Order not found"}))

            order = json.loads(order)
            notes = json.loads(order['notes'])
            examination_ids =  [int(id) for id in notes['examination_ids'].split(",")]

            #signature verify
            generated_signature = await hmac_sha256(order_id + "|" + order_details.payment_id, os.getenv('RAZORPAY_KEY_SECRET'))
            if generated_signature != order_details.signature:
                return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Signature mismatch"}))

            logger.info(f'Order verified: {order_id} {order_details.payment_id} {order_details.signature}')

            #capture order
            payload = {
                "amount": order['amount'],
                "currency": order['currency'],
            }

            req = requests.post(
                f'{os.getenv("RAZORPAY_PAYMENT_URL")}/{order_details.payment_id}/capture',
                auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET')),
                headers={'content-type': 'application/json'},
                json=payload  # Convert payload to JSON
            )

            res = req.json()
            if req.status_code != 200:
                return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error capturing order: {req.text}"}))

            logger.info(f'Order captured: {order_id} {order_details.payment_id} {order_details.signature} {res['contact']}')

            #create a random 6 letter and digits combined password
            password = ''.join(random.choices(string.digits, k=6))

            #create the profile
            profile = await ProfileCRUD(self.db).create_inital_profile()
            if hasattr(profile, 'error'):
                return ServiceResult(f'Error creating profile: {profile.error}')

            #create the admit card
            admitcard = {
                "order_id": order_id,
                "password_hash": await hash_password(password)
            }
            _admitcard = await AdmitCardCRUD(self.db).create( profile_id=profile.id, championship_id=int(notes['championship']), examination_ids=examination_ids, item=admitcard)
            logger.info(f'Admit card created: {str(_admitcard)}')
            admitcard = AdmitCard(
                id = _admitcard.id,
                order_id = _admitcard.order_id,
                password = password,
                championship_id = _admitcard.championship_id,
                examination_ids = _admitcard.examination_ids,
                profile_id = _admitcard.profile_id
            )

            return ServiceResult(admitcard)

        except Exception as e:
            logger.error(f'Error capturing order: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error capturing order: {str(e)}"}))
