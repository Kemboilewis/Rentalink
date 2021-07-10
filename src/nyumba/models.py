from django.db import models
from user_account.models import myUser
#from MpesaPayments.models import *

# plots table
class Plot(models.Model):
    types = (
		('single', 'single'),
		('multi_unit', 'multi_unit'),
		)
    plot_owner = models.ForeignKey(myUser, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=50, choices=types)
    property_name = models.CharField(max_length=100)
    year_built = models.DateField()
    location = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    property_image = models.ImageField(upload_to='images/',default='image')
    currency = models.CharField(max_length=10)
    date_created = models.DateTimeField( auto_now_add=True, blank=True, null=True)
    class Meta:
        verbose_name = 'Plot'
        verbose_name_plural = 'Plots'

    def __str__(self):
        return self.property_name
class Room(models.Model):
    room_plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    room_image = models.ImageField(upload_to='images/',default='image')
    room_tenant = models.ForeignKey(myUser, on_delete=models.CASCADE, blank=True, null=True)
    room_status = models.BooleanField(default=False)
    room_wallet = models.DecimalField(decimal_places=3, max_digits=10, blank=True, null=True)
    beds = models.CharField( max_length=100)
    baths = models.CharField( max_length=100)
    size = models.CharField( max_length=100)
    market_rent = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    parking = models.CharField( max_length=100)
    min_deposit = models.DecimalField(decimal_places=2, max_digits=12, blank=True)
    payment_status = models.BooleanField(default=False) 
    date_created = models.DateTimeField( auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.room_name

#booking applications
class Room_application(models.Model):
    pending = 0
    succesful = 1
    declined = 2

    landlord_choices = (
        (pending, ('pending')),
        (succesful, ('succesful')),
        (declined, ('declined')),

        ) 
    booking_user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    booked_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked_plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    #payment_reference = models.ForeignKey(Succesful_Room_payments, on_delete=models.CASCADE, blank=True, null=True)
    landlords_response = models.PositiveSmallIntegerField(choices=landlord_choices,default=pending)
    payment_status = models.BooleanField(default=False)
    disabled_status = models.BooleanField(default=False)
    merchantrequestid = models.CharField(max_length=50, blank=True, null=True)
    active_status = models.BooleanField(default=True)
    book_time = models.DateTimeField()
    check_in_date = models.DateField()
    stay_time = models. CharField( max_length=100)
    check_out_date = models.DateField()
    Receipt_Number = models.CharField(max_length=100, blank=True, null=True)

    class Meta: 
        verbose_name = 'Room application'
        verbose_name_plural = 'Room applications'

    def __str__(self):
        return self.booking_user.username

class Maintenance(models.Model):
    new = 0
    progress = 1
    completed = 2
    declined = 3

    stage = (
        (new, ('new')),
        (progress, ('progress')),
        (completed, ('completed')),

        )
    applying_user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    problem = models.TextField()
    pr_image = models.ImageField(upload_to='images/',default='image')
    status = models.PositiveSmallIntegerField(choices=stage,default=new)
    date_applied = models.DateTimeField( auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Maintenance request'
        verbose_name_plural = 'Maintenance requests'

    def __str__(self):
        return self.plot.property_name

class Store(models.Model):
    store_owner = models.ForeignKey(myUser, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    store_capacity = models.CharField(max_length=100)
    store_image = models.ImageField(upload_to='images/',default='image')
    store_plot = models.ForeignKey(Plot, on_delete=models.CASCADE, blank=True)
    store_location = models.CharField(max_length=100)
    year_built = models.DateField()
    store_address = models.CharField( max_length=100)
    store_state = models.CharField(max_length=100)
    m_cost = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    space_availability = models.BooleanField(default=True)
    date_created = models.DateTimeField( auto_now_add=True, blank=True, null=True)
    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.store_name
class Store_unit(models.Model):
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    unit_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    unit_status = models.BooleanField(default=True)
    user_mzigo = models.ForeignKey(myUser, on_delete=models.CASCADE, blank=True, null=True)
    unit_mzigo = models.CharField(max_length=100, blank=True, null=True)
    unit_number = models.PositiveIntegerField()
    date_created = models.DateTimeField( auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Store Unit'
        verbose_name_plural = 'Store Units'

    def __str__(self):
        return self.unit_store.store_name

class Store_applications(models.Model):
    pending = 0
    succesful = 1
    declined = 2

    owners_choices = (
        (pending, ('pending')),
        (succesful, ('succesful')),
        (declined, ('declined')),

        )
    applied_unit = models.ForeignKey(Store_unit, on_delete=models.CASCADE)
    applying_user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    #payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    applied_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    owner_response = models.PositiveSmallIntegerField(choices=owners_choices,default=pending)
    starting_date = models.DateField()
    ending_date = models.DateField()
    application_time = models.DateTimeField()
    goods = models.CharField(max_length=100, default="mzigo")

    class Meta:
        verbose_name = 'Store application'
        verbose_name_plural = 'Store applications'

    def __str__(self):
        return self.applying_user.username
class Chat(models.Model):
	sender=models.ForeignKey(myUser, on_delete=models.CASCADE)
	receiver=models.CharField(max_length=100)
	subject=models.CharField(max_length=500, default='NO SUBJECT')
	text=models.TextField(max_length=2000, blank=True, null=True)
	message_status=models.BooleanField(default=False)
	date_sent=models.DateTimeField(max_length=20)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	hide_status = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Chat'
		verbose_name_plural = 'Chats'

	def __str__(self):
		today=str(self.date_sent).split('.',2)
		date_today=today[0]
		return self.sender + ' '+ date_today













