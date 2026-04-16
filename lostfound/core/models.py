from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    ITEM_TYPE = (
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='items/')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ClaimRequest(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    proof = models.ImageField(upload_to='proofs/')

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.item} - {self.status}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']