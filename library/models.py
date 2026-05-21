from django.db import models
from django.contrib.auth.models import User


class Membership(models.Model):
    membership_type = models.CharField(max_length=50)
    duration_days = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.membership_type


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    available = models.IntegerField()

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class IssueBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=8,
                           decimal_places=2,
                           default=0)

    fine_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title
# Create your models here.
