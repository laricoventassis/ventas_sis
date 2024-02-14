from django.db import models
from django.contrib.auth.models import AbstractUser


TURNO = (
  ('maniana', 'Mañana'),
  ('noche', 'Noche')
)

class Usuario(AbstractUser):
  cNombres = models.CharField('Nombres y Apellidos', max_length=120, null=True)
  turno = models.CharField('Turno', choices=TURNO, default="maniana",  max_length=120)
  lVigente = models.BooleanField('Vigente', default=True)
