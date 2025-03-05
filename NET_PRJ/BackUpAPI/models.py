from django.db import models


class BU_model(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    user = models.CharField(max_length=200)
    
    def __str__(self):
        return self.file.name
