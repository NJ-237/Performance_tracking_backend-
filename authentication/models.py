from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings;'l[]'


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    for user in User.objects.all():
       Token.objects.get_or_create(user=user)    

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        primary_key=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(max_length=20, blank=True)
    Service_location = models.CharField(max_length=100, blank=True)
    Position = models.CharField(max_length=100, blank=True)
    Employee_id = models.IntegerField(max_length=10, unique=True)
    Gender = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=10, blank=True, unique=True)
    password = models.CharField(max_length=20)


def __str__(self):
        return f"{self.user.username}'s Profile"

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
    # CRO = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # CDQ = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Patroller = models.ForeignKey(Profile, on_delete=models.CASCADE)

     # Operator fields
    cro1 = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='cro1_shifts')
    cro2 = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='cro2_shifts')
    patroller1 = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='patroller1_shifts')
    patroller2 = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='patroller2_shifts')
    cdq = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='cdq_shifts')
    
    # Other personnel that may not be in Profile
    app_elec = models.CharField(max_length=100)
    app_meca = models.CharField(max_length=100)
    laboratin1 = models.CharField(max_length=100)
    laboratin2 = models.CharField(max_length=100)

    # Metadata
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_shifts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="updated_shifts")
   

    #   # Extraction silo data (as JSON)
    # extraction_silo = models.JSONField(default=dict)
    # ensilage_silo = models.JSONField(default=dict)
    
    class Meta:
        unique_together = ('date', 'shift_number')
        ordering = ['date', 'shift_number']


class Equipement(models.Model):
    # BROYEUR_CHOICES = [
    #     ('BROYEUR-1', 'Broyeur 1'),
    #     ('BROYEUR-4', 'Broyeur 4'),
    #     ('BROYEUR-5', 'Broyeur 5'),
    # ]
    equipement_id = models.IntegerField( primary_key=True)
    # port_id = models.AutoField(max_length=10, primary_key=True)
    BDP = models.IntegerField()
    Name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    longueur = models.IntegerField()
    largeur = models.IntegerField()
    Date_de_fabrication = models.DateField()
    Date_installation = models.DateField()
    
class Ciment_type(models.Model):
     ciment_id = models.AutoField( primary_key=True)
     name = models.CharField(max_length=50)
     ciment_speciaux = models.CharField(max_length=50)
        
   
class Mill_production(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='Mill_productiont')
    equipement_id = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name='Mill_productiont')
    production = models.IntegerField()
    ciment_id = models.ForeignKey(Ciment_type, on_delete=models.CASCADE, related_name='Mill_productiont')
    
      # Common fields for all broyeurs
    clinker_debut = models.FloatField()
    clinker_fin = models.FloatField()
    pouzzolane_debut = models.FloatField()
    pouzzolane_fin = models.FloatField()
    gypse_debut = models.FloatField()
    gypse_fin = models.FloatField()
    fine_debut = models.FloatField()
    fine_fin = models.FloatField()
    compteur_horaire_debut = models.FloatField()
    compteur_horaire_fin = models.FloatField()
    compteur_horaire_Production = models.FloatField()
    compteur_horaire_Production = models.FloatField()
    SO3 = models.FloatField()
    Blaines = models.FloatField()
    # Production = models.FloatField() total value of production
    commentaires = models.TextField(blank=True)

     # Extraction silo data (as JSON)
    extraction_silo = models.JSONField(default=dict)
    ensilage_silo = models.JSONField(default=dict)
    
    # Situation
    situation_entree_quart = models.CharField(max_length=20, choices=[
        ('En Marche', 'En Marche'),
        ('En Arret', 'En Arret')
    ])
    

# class SecheurData(models.Model):
#     # secheur_id = models.AutoField(max_length=10, primary_key=True)
#     shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='secheur_data')
    
  
class Port_production(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='Port_production')
  


class Dryer_production(models.Model):
       # Matieres premieres pour secheur 
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
    production = models.CharField(max_length=100, blank=True)
    commentaires = models.TextField(blank=True)
    humidites_entree = models.TextField(blank=True)
    humidites_sortie = models.TextField(blank=True)

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='Dryer_production')
    # broyeur_type = models.CharField(max_length=10, choices=BROYEUR_CHOICES)
    
    # Godets data
    nbre_godets = models.IntegerField()
    poids_godets = models.FloatField()
    debit = models.FloatField()



# class PortData(models.Model):
    # port_id = models.AutoField(max_length=10, primary_key=True)
    # shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='port_data')
    
    # Dechargement data
    # commentaires = models.TextField(blank=True)
    # debut = models.DateTimeField()
    # fin = models.DateTimeField()
    # duree = models.DurationField()
    # compteur_debut = models.FloatField()
    # compteur_fin = models.FloatField()
    # dechargement = models.FloatField()

class ExpeditionData(models.Model):
    # expedition_id = models.AutoField(max_length=10, primary_key=True)
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


class Feedback(models.Model):
    Employee_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedbacks')
    submitted_by = models.CharField(max_length=100)
    feedback_type = models.CharField(max_length=100)
    comments = models.TextField()
    date = models.DateField()


