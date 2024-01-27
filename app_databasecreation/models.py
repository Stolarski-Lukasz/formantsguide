from django.db import models

# Create your models here.
class Phonetician(models.Model):
    name = models.CharField(max_length=25)
    official_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=6)

    def __str__(self) -> str:
        return self.name

class Recording(models.Model):
    phonetician = models.ForeignKey(Phonetician, on_delete=models.CASCADE)
    vowel_str = models.CharField(max_length=2)
    vowel = models.IntegerField()
    path = models.CharField(max_length=100)
    f1 = models.IntegerField()
    f2 = models.IntegerField()
    f3 = models.IntegerField()

    def __str__(self) -> str:
        return self.path