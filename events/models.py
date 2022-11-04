from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todos(models.Model):
    task_name=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
# when a parent item deleted do cascade
    status=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task_name
