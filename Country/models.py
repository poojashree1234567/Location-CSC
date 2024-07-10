from django.db import models
import uuid

# Create your models here.
class Base(models.Model):
    is_active = models.BooleanField(default=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True

class Country(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    code = models.CharField(max_length=10, unique=True)
    flag = models.ImageField(upload_to='flag')
    is_state_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class State(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    population = models.IntegerField()

    def __str__(self):
        return self.name

class City(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name