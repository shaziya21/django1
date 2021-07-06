from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
# sender: the model that sending the signal. The instance of it, the created instance
# what we're doing here is whenever that signal calls this fn this receiver gonna check if this is the first instance, if this is we'll go ahead & create a new profile
	if created:
		Profile.objects.create(user=instance)
		print('Profile created!')
# here user  is user model. # create_profile is receiver and user is sender# this is how we connect a receiver to a sender.
# everysingle time the save method is called we're gonna go ahead and trigger this receive method(create_profile) or this create_profilefn after the save is complete so post save after save go ahead and trigger that fn and listen  to this (post_save) model here .

#post_save.connect(create_profile, sender=User)


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):

	if created == False:  # this means that this user already exists
		instance.profile.save()  # lets go ahead and update that user profile
		print('Profile updated!')


#post_save.connect(update_profile, sender=User)
