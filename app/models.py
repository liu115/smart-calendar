from django.db import models

class Event(models.Model):
    '''
    Save the event for calendar usage
    '''
    title = models.CharField(max_length=50)
    comment = models.TextField(max_length=100)
    starttime = models.DateTimeField()
    duration = models.DurationField()
    owner_user_id = models.PositiveIntegerField()

    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'

class Group(models.Model):
    '''
    Group is a invite link between starter and target.

    is_pending: wait for target accept
    is_success: True if the target accept
    
    if is_pending == False and is_success == False,
    the grouping invitation is canceled
    '''

    group_id = models.PositiveIntegerField()
    starter_id = models.PositiveIntegerField()
    starter_name = models.CharField(max_length=50)
    target_id = models.PositiveIntegerField()
    target_name = models.CharField(max_length=50)
    
    is_pending = models.BooleanField()
    is_success = models.BooleanField()

    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "group_id": self.group_id,
            "starter_id": self.starter_id,
            "starter_name": self.starter_name,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "is_pending": self.is_pending,
            "is_success": self.is_success,
            "created": self.created.timestamp(),
        }
    class Meta:
        db_table = 'groups'

