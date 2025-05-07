from django.db import models


# Create your models here.
class ProductType(models.Model):
    title = models.CharField(
        max_length=32,blank=True,null=True
    )
    description = models.TextField(blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add= True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#Define ProductAttributes
class ProductAttribute (models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3
    ATTRIBUTE_TYPE_FIELD = (
        (INTEGER,'INTEGER'),
        (STRING, 'STRING'),
        (FLOAT,'FLOAT'),
    )

    title = models.CharField(
        max_length=32
    )
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE,related_name='attributes')
    attribute_type = models.PositiveSmallIntegerField(
        default=INTEGER,choices=ATTRIBUTE_TYPE_FIELD
    )
    def __str__(self):
        return self.title


# Define category table
class Category(models.Model):
        name = models.CharField(max_length=32)
        parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
        def __str__(self):
            return self.name
        def get_absolute_url(self):
            from django.urls import reverse
            return reverse('product_detail',args = [self.pk])


# Define Brand table
class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name


# Define ProductManager #
class ProductManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(soft_delete = False)


# Define Product table
class Product(models.Model):
    product_type = models.ForeignKey(ProductType,on_delete=models.PROTECT,related_name='products')
    upc = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT,related_name='products')
    soft_delete = models.BooleanField(default=False)
    image = models.ImageField(blank=True,null=True,upload_to='products/')
    # --- Default ModelsManager --- #
    default_objects = models.Manager()

    # --- overwrite ModelManager for Product --- #
    objects = ProductManager()

    def __str__(self):
        return self.title
    # Define 'stock' as a property to show product's price
    @property
    def stock(self):
        return self.partners.all().order_by('price').first()


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
# --- Define ProductImage table to keep more than one image for each product ---#
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(blank=True,null=True,upload_to='products/')

    def __str__(self):
        return self.product.title

#Define ProductAttributeValue
class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='attribute_values')
    value = models.CharField(max_length=48)
    attribute = models.ForeignKey(ProductAttribute,on_delete=models.PROTECT,related_name='values')
    def __str__(self):
        return f"{self.product}{self.attribute}:{self.value}"


