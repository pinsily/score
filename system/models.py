from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

class Profile(AbstractUser):
    """
    information about student
    """
    index = models.BigAutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)
    nickname = models.CharField(verbose_name="昵称", max_length=256, default="", blank=True)

    class Meta:
        db_table = "profile"
        verbose_name = "student"
        app_label = "system"

    def __str__(self):
        return self.username


class Professor(models.Model):
    """
    information about professor
    """
    index = models.BigAutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)
    code = models.CharField(verbose_name="code", max_length=10, default="")
    name = models.CharField(verbose_name="name", max_length=255)

    class Meta:
        db_table = "professor"
        verbose_name = "professor"

    def __str__(self):
        return self.name


class Module(models.Model):
    """
    information about module
    """
    index = models.BigAutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)
    code = models.CharField(verbose_name="code", max_length=10)
    name = models.CharField(verbose_name="name", max_length=255)
    year = models.CharField(verbose_name="year", max_length=255)
    semester = models.IntegerField(verbose_name="semester")
    professor = models.ManyToManyField(Professor, related_name="module_professor")

    class Meta:
        db_table = 'module'
        verbose_name = 'module'

    def __str__(self):
        return f"{self.year}-{self.semester}-{self.name}"


class Score(models.Model):
    """
    information about score
    """
    index = models.BigAutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)
    student = models.ForeignKey(to=Profile, related_name="score_student", on_delete=models.DO_NOTHING)
    module = models.ForeignKey(to=Module, related_name="score_module", on_delete=models.DO_NOTHING)
    professor = models.ForeignKey(to=Professor, related_name="score_professor", on_delete=models.DO_NOTHING)
    score = models.IntegerField(verbose_name="score", default="0", validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

    class Meta:
        db_table = 'score'
        verbose_name = 'score'
