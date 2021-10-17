from django.db import models

# Create your models here.
class PageImage(models.Model):
    img1= models.ImageField(upload_to="stuff/images")
    img2= models.ImageField(upload_to="stuff/images")
    img3= models.ImageField(upload_to="stuff/images")
    about= models.ImageField(upload_to="stuff/images")
    features= models.ImageField(upload_to="stuff/images")
    comment= models.ImageField(upload_to="stuff/images")
    contact= models.ImageField(upload_to="stuff/images")
    # img1= models.ImageField(upload_to="stuff/images")
    


