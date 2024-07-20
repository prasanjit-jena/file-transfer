from django.db import models

class ProcessedData(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    clubbed_name = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    value = models.FloatField()

    def __str__(self):
        return f"{self.year} - {self.month} - {self.category} - {self.clubbed_name} - {self.product} - {self.value}"

    class Meta:
        # ordering=['-id']
        verbose_name = 'Output Data'    
        verbose_name_plural = "Output Data's"

# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
