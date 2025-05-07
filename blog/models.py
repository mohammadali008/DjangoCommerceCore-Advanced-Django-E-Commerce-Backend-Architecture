from django.db import models

# Create your models here.
class Blog(models.Model):
    user_auther = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=32)
    post = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # --- Main Method --- #
    def __str__(self):
        return f"post :{self.title} is writen by : {self.user_auther}"