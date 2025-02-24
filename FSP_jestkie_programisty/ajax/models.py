from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    registration_date = models.DateField(auto_now_add=True)
    is_send = models.BooleanField(default=False, blank=True)
    is_read = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name