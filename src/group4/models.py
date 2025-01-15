from django.db import models


class G25Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255)

    class Meta:
        db_table = 'G2_5_dataset'