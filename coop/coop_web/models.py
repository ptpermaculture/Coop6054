from django.db import models
from django.contrib import admin

class Role(models.Model):
    ROLE_CHOICES = (('w', 'worker'), ('v', 'volunteer') )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    role_details = models.TextField()

class Worker(models.Model):
    roles = models.ManyToManyField(Role)

class Address(models.Model):
    street_name = models.CharField(max_length=50)
    unit_number = models.IntegerField(blank=True, null=True)
    street_number = models.IntegerField()
    postcode = models.IntegerField()
    suburb_town_locality = models.CharField(max_length=40)
    #member = models.ForeignKey(Member)

    def __unicode__(self):
        return ("%s %s, %s, %s" % (self.street_number, self.street_name, self.suburb_town_locality, self.postcode))

class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_address',)
    list_filter = ('postcode',)

    def full_address (self, obj):
        return ("%s %s, %s, %s" % (obj.street_number, obj.street_name, obj.suburb_town_locality, obj.postcode))
    full_address.short_description = 'name'

#class AddressInline(admin.TabularInline):
#    model = Address
#    max_num = 1

class Role(models.Model):
    ROLE_CHOICES = (('w', 'worker'), ('v', 'volunteer') )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    role_details = models.TextField()

class Worker(models.Model):
    roles = models.ManyToManyField(Role)

class Member(models.Model):
    worker_id = models.ForeignKey(Worker, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    paid_member = models.BooleanField()
    address_id = models.ForeignKey(Address)
    #orders = models.ManyToManyField(Order, blank=True, null=True)

    def __unicode__(self):
        return ("%s %s" % (self.first_name, self.last_name))

class MemberAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    raw_id_fields = ('address_id',)

class Product(models.Model):
    product_code = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    size_unit = models.CharField(max_length=10, blank=True, null=True) 
    gst_taxable = models.NullBooleanField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True) 
    price_wholesale = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    price_wholesale_gst = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    price_retail = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    price_retail_gst = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    item_type = models.CharField(max_length=30, blank=True, null=True)
    item_number = models.IntegerField(blank=True, null=True)
    brand = models.CharField(max_length=30, blank=True, null=True) 
    location = models.CharField(max_length=40, blank=True, null=True) 

    def __unicode__(self):
        return ("%s, %s %s" % (self.description, self.size, self.size_unit))

class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'product_size', 'brand')
    list_filter = ('size', 'brand', 'location')
    search_fields = ['description', 'item_type']
    
    def product_size (self, obj):
        return ("%s %s" % (obj.size, obj.size_unit))

class Order(models.Model):
    products = models.ManyToManyField(Product, through=LineItem)

class LineItem(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    quantity = models.IntegerField()

class Producer(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address)
    products = models.ManyToManyField(Product)

class Distributor(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address)
    products = models.ManyToManyField(Product, blank=True, null=True)
    
    def __unicode__(self):
        return ("%s, %s" % (self.name, self.address.suburb_town_locality))

class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    raw_id_fields = ('address',)

class Certification(models.Model):
    CERTIFICATION_CHOICES = ( ('n', 'none'), ('o', 'organic'), ('f', 'fairtrade') )
    certification_type = models.CharField(max_length=30, choices=CERTIFICATION_CHOICES)
    name = models.CharField(max_length=30)
    products = models.ManyToManyField(Product)

class Type(models.Model):
    description = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)

admin.site.register(Product, ProductAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Producer)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order)
