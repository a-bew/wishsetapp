# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
	
class Tbl_wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')
    wish_title = models.CharField(max_length=45)
    wish_description = models.CharField(max_length=300)
#    wish_user_id = models.IntegerField(default=0)
    wish_date = models.DateField(datetime.datetime.now)

    def __str__(self):
        return self.wish_title
