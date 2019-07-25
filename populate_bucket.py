import os 
import sys

import django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def populate():
   
    
    add_wish(
				wish_title="Barbing",
				wish_description="We offer best inhouse barbing service experience. Call now. 08111312278",
				wish_date=timezone.now())
   
    add_wish(	wish_title="Exam",
				wish_description="Pray and wish me best success examination experience",
				wish_date=timezone.now())

    
    

#def add_user(name):
#		u = UserProfile.objects.get_or_create(user=name)[0]
#		return u

def add_wish(user, wish_title, wish_description, wish_date):
		w = Page.objects.get_or_create(user=user, wish_title=wish_title, wish_description=wish_description, wish_date = wish_date)[0]
		return w


		# Print out what we have added to the user.
#		for u in add_user.objects.all():
		for w in add_wish.objects.all():
				print "- {0}".format(str(w))

# Start execution here!
if __name__ == '__main__':
		print "Starting Bucketlist population script..."
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bucketsite.settings",)

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from bucketlist.models import Tbl_wish
populate()