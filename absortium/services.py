import time

from absortium import constants

__author__ = 'andrew.shvv@gmail.com'


class Base():
    def __init__(self, client):
        self.client = client


def timing(func):
    def decorator(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()

        print('{} - {} sec - (price - {} , amount - {})'.format(func.__name__, te - ts, kwargs.get('price'), kwargs.get('amount')))
        return result

    return decorator


class Withdrawal(Base):
    def list(self, currency=None):
        params = {
            'currency': currency
        }

        return self.client.get('api', 'withdrawals', params=params)

    def create(self, amount, address):
        data = {
            'amount': amount,
            'address': address
        }

        return self.client.post('api', 'withdrawals', data=data)


class Deposit(Base):
    def list(self, currency=None):
        params = {
            'currency': currency
        }

        return self.client.get('api', 'deposits', params=params)


class Order(Base):
    def create(self,
               price,
               amount=None,
               total=None,
               order_type=None,
               pair=constants.PAIR_BTC_ETH,
               need_approve=False):
        data = {
            'type': order_type,
            'price': price,
            'pair': pair,
            'total': total,
            'amount': amount,
            'need_approve': need_approve
        }

        return self.client.post('api', 'orders', data=data)

    def retrieve(self, pk):
        return self.client.get('api', 'orders', pk)

    def list(self,
             order_type=None,
             pair=None):
        params = {
            'type': order_type,
            'pair': pair,
        }
        return self.client.get('api', 'orders', params=params)

    def update(self,
               pk,
               price,
               amount=None,
               total=None,
               **kwargs):
        data = {
            'price': price,
            'amount': amount,
            'total': total,
        }
        return self.client.put('api', 'orders', pk, data=data)

    def cancel(self, pk, **kwargs):
        return self.client.delete('api', 'orders', pk)

    def approve(self, pk, **kwargs):
        return self.client.post('api', 'orders', pk, 'approve')

    def lock(self, pk, **kwargs):
        return self.client.post('api', 'orders', pk, 'lock')

    def unlock(self, pk, **kwargs):
        return self.client.post('api', 'orders', pk, 'unlock')


class Account(Base):
    def list(self):
        return self.client.get('api', 'accounts')

    def retrieve(self, currency):
        return self.client.get('api', 'accounts', currency)

    def create(self, currency):
        data = {'currency': currency}
        return self.client.post('api', 'accounts', data=data)
