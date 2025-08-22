from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Profile(models.Model):
    
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    Service_location = models.CharField(max_length=100, blank=True)
    Position = models.CharField(max_length=100, blank=True)
    Employee_id = models.CharField(max_length=50, blank=True)
    Gender = models.CharField(max_length=10, blank=True)
    # role = models.CharField(max_length=10, blank=True)

# class User(AbstractUser):
#         manager = models.ForeignKey(SomeModel, on_delete=models.CASCADE, related_name='managed_users', null=True, blank=True)

#         role = models.CharField(max_length=50, blank=True, null=True)  # Example
    
# Create your models here.


# models.py input data from ReportSide 

class Shift(models.Model):
    SHIFT_CHOICES = [
        (1, 'Shift 1 (6:00 AM - 2:00 PM)'),
        (2, 'Shift 2 (2:00 PM - 10:00 PM)'),
        (3, 'Shift 3 (10:00 PM - 6:00 AM)'),
    ]
    
    date = models.DateField()
    shift_number = models.IntegerField(choices=SHIFT_CHOICES)
    CRO1 = models.TextField()
    CRO2 = models.TextField()
    CDQ = models.TextField()
    Patroller1 = models.TextField()
    Patroller2 = models.TextField()
    APP_ELEC = models.TextField()
    APP_MECA = models.TextField()
    Laboratin1 = models.TextField()
    Laboratin2 = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('date', 'shift_number')

class BroyeurData(models.Model):
    BROYEUR_CHOICES = [
        ('BROYEUR-1', 'Broyeur 1'),
        ('BROYEUR-4', 'Broyeur 4'),
        ('BROYEUR-5', 'Broyeur 5'),
    ]
    
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='broyeur_data')
    broyeur_type = models.CharField(max_length=10, choices=BROYEUR_CHOICES)
    
    # Common fields for all broyeurs
    clinker_debut = models.FloatField()
    clinker_fin = models.FloatField()
    clinker_Difference = models.FloatField()
    pouzzolane_debut = models.FloatField()
    pouzzolane_fin = models.FloatField()
    pouzzolane_Difference = models.FloatField()
    gypse_debut = models.FloatField()
    gypse_fin = models.FloatField()
    gypse_Difference = models.FloatField()
    fine_debut = models.FloatField()
    fine_fin = models.FloatField()
    fine_Difference = models.FloatField()
    compteur_horaire_debut = models.FloatField()
    compteur_horaire_fin = models.FloatField()
    compteur_horaire_Difference = models.FloatField()
    compteur_horaire_Production = models.FloatField()
    # Production = models.FloatField() total value of production
    ciment_produit = models.FloatField()
    Tonnage = models.FloatField()
    commentaires = models.TextField(blank=True)
    
    # Extraction silo data (as JSON)
    extraction_silo = models.JSONField(default=dict)
    ensilage_silo = models.JSONField(default=dict)

class SecheurData(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='secheur_data')
    
    # Matieres premieres
    PZ_humide_debut = models.FloatField()
    PZ_humide_fin = models.FloatField()
    PZ_humide_Difference = models.FloatField()
    PZ_humide_Production = models.FloatField()
    bande_melange_debut = models.FloatField()
    bande_melange_fin = models.FloatField()
    bande_melange_Difference = models.FloatField()
    bande_melange_Production = models.FloatField()
    compteur_horaire_debut = models.FloatField()
    compteur_horaire_fin = models.FloatField()
    compteur_horaire_Difference = models.FloatField()
    compteur_horaire_Production = models.FloatField()
    quality = models.CharField(max_length=100, blank=True)
    commentaires = models.TextField(blank=True)
    
    # Godets data
    nbre_godets = models.IntegerField()
    poids_godets = models.FloatField()
    debit = models.FloatField()
    
    # Situation
    situation_entree_quart = models.CharField(max_length=20, choices=[
        ('En Marche', 'En Marche'),
        ('En Arret', 'En Arret')
    ])

      # Extraction silo data (as JSON)
    extraction_silo = models.JSONField(default=dict)
    ensilage_silo = models.JSONField(default=dict)
    

class PortData(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='port_data')
    
    # Dechargement data
    commentaires = models.TextField(blank=True)
    debut = models.DateTimeField()
    fin = models.DateTimeField()
    duree = models.DurationField()
    compteur_debut = models.FloatField()
    compteur_fin = models.FloatField()
    dechargement = models.FloatField()

     # Situation
    situation_entree_quart = models.CharField(max_length=20, choices=[
        ('En Marche', 'En Marche'),
        ('En Arret', 'En Arret')
    ])
    
    # Extraction data
    # extraction_data = models.JSONField(default=dict)
    ensilage_silo = models.JSONField(default=dict)

class ExpeditionData(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='expedition_data')
    
    # Expedition data
    kk_chargee_nomayos_kk = models.TextField()
    kk_chargee_nomayos_NbreCamion = models.FloatField()
    kk_chargee_nomayos_Tonnage = models.FloatField()
    gypse_chargee_nomayos_kk = models.FloatField()
    gypse_chargee_nomayos_NbreCamion = models.FloatField()
    gypse_chargee_nomayos_Tonnage = models.FloatField()
    gypse_figuil_kk = models.FloatField()
    gypse_figuil_NbreCamion = models.FloatField()
    gypse_figuil_Tonnage = models.FloatField()
    petcoke_figuil_kk = models.FloatField()
    petcoke_figuil_NbreCamion = models.FloatField()
    petcoke_figuil_Tonnage = models.FloatField()
    kk_cimaf_kk = models.FloatField()
    kk_cimaf_NbreCamion = models.FloatField()
    kk_cimaf_Tonnage = models.FloatField()
    kk_dangote_kk = models.FloatField()
    kk_dangote_NbreCamion = models.FloatField()
    kk_dangote_Tonnage = models.FloatField()
    kk_miraco_kk = models.FloatField()
    kk_miraco_NbreCamion = models.FloatField()
    kk_miraco_Tonnage = models.FloatField()
    
    # Reception camions
    reception_camions_rejets = models.FloatField()
    provenance_lieu = models.CharField(max_length=100)
    nbre_camion = models.IntegerField()
    tonnage = models.FloatField()
    
    # Stock biomasse
    no_godets_cim_biomasse = models.IntegerField()
    godets_geocycle_biomasse = models.IntegerField()
    no_godets_receptions = models.IntegerField()
    tonnage_stock_receptions = models.FloatField()
 