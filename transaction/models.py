from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SENT = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER_RECEIVED, "TransferReceived"),
        (TRANSFER_SENT, "TransferSent")
    )

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.RESTRICT)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        """Show all users and their balance"""
        positive_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type__in=[1, 3])
        )
        negative_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type__in=[2, 4])
        )
        users = User.objects.all().annotate(
            transactions_count=Count('transactions__id'),
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )

        return users

    @classmethod
    def get_total_balance(cls):
        queryset = cls.get_report()
        return queryset.aggregate(Sum('balance'))

    @classmethod
    def user_balance(cls, user):
        positive_transactions = Sum('amount', filter=Q(transactions_type__in=[1, 3]))
        negative_transactions = Sum('amount', filter=Q(transaction_type__in=[2, 4]))

        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )
        return user_balance.get('balance', 0)


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='balance_records', on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_balance_display()} - {self.created_time}"

    @classmethod
    def recorder_user_balance(cls, user):
        balance = Transactions.user_balance(user)
        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def record_all_users_balance(cls):
        for user in User.objects.all():
            cls.recorder_user_balance(user)


class TransferTransaction(models.Model):
    sender_transaction = models.OneToOneField(
        Transaction, related_name='sent_transfers', on_delete=models.RESTRICT
    )
    receiver_transaction = models.ForeignKey(
        Transaction, related_name='received_transfers', on_delete=models.RESTRICT
    )

    def __str__(self):
        return f"{self.sender_transaction} >> {self.receiver_transaction}"

    @classmethod
    def transfer(cls, sender, receiver, amount):
        if Transaction.user_balance(sender) < amount:
            return "Transaction not Allowed, insufficient balance"

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender, amount=amount, transaction=Transaction.TRANSFER_SENT
            )

            receiver_transaction = Transaction.objects.create(
                user=receiver, amount=amount, transaction=Transaction.TRANSFER_RECEIVED
            )

            instance = cls.objects.create(
                sender_transaction=sender_transaction, receiver_transaction=receiver_transaction
            )
        return instance


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        permissions = [
            ('has_score_permission', "User has Score permission")
        ]

    @classmethod
    def change_score(cls, user, score):
        instance = cls.objects.select_for_update().get(user=user)
        with transaction.atomic():
            if not instance.exists():
                instance = cls.objects.create(user=user, score=0)
            else:
                instance = instance.first()
            instance.score += score
            instance.save()
