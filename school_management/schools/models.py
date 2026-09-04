# schools/models.py
from django.db import models
from django.utils.text import slugify

class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'école")
    code = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Code unique")
    location = models.CharField(max_length=255, verbose_name="Localisation")
    is_active = models.BooleanField(default=True, verbose_name="Est active")
    configuration = models.JSONField(default=dict, blank=True, verbose_name="Configuration spécifique")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Génération automatique du code unique si le champ est vide
        if not self.code:
            # Nettoie le nom pour en faire un code propre (ex: "EP Ghost" -> "EP-GHOST" ou "EPGHOST")
            base_code = slugify(self.name).upper().replace("-", "")[:8]
            
            # Vérifie l'unicité et ajuste si le code existe déjà
            unique_code = base_code
            counter = 1
            while School.objects.filter(code=unique_code).exists():
                unique_code = f"{base_code}{counter}"
                counter += 1
                
            self.code = unique_code
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"