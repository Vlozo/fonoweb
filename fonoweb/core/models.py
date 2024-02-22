from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Society(models.Model):
    acronym = models.CharField('Sigla', max_length=50)
    name = models.CharField('Nome', max_length=100)
    is_national = models.BooleanField(default = True)

    registered_in = models.DateField("Cadastrado em", default=date.today)
    updated_in = models.DateField("Atualizado em", default=date.today)
    #updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Atualizado por')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Sociedade"
        verbose_name_plural = "Sociedades"


class Pseudonym(models.Model):
    holder = models.ForeignKey('Holder', on_delete=models.CASCADE, verbose_name='Titular', blank=True, null=True, unique = True)
    pseudonym = models.CharField('Pseudônimo', max_length=100)
    is_main = models.BooleanField('Principal', default=False)

    def __str__(self):
        return f"{self.pseudonym}"    
    
    class Meta:
        verbose_name = 'Pseudônimo'
        verbose_name_plural = 'Pseudônimos'
    

class Holder(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('F', 'Fisica'),
        ('J', 'Jurídica'),
    ]

    ORIGIN_TYPE_CHOICES = [
        ('N', 'Nacional'),
        ('E', 'Estrangeira'),
    ]

    CPF_TYPE_CHOICES = [
        ('proprio', 'Próprio'),
        ('responsavel', 'Responsável'),
        ('estrangeiro', 'Estrangeiro'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('solteiro', 'Solteiro'),
        ('casado', 'Casado'),
        ('separado', 'Separado'),
        ('divorciado', 'Divorciado'),
        ('viúvo', 'Viúvo')
    ]

    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ]

    #owner = models.ForeignKey(Group, on_delete=models.DO_NOTHING, verbose_name='Grupos')
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email Principal', blank=True)
    ecad_code = models.IntegerField('Cód. ECAD', blank=True, null=True)

    origin = models.CharField('Origem', choices=ORIGIN_TYPE_CHOICES, max_length=1, default='N')
    entity_type = models.CharField('Tipo de Pessoa', choices=ENTITY_TYPE_CHOICES, max_length=1, default='F')
    is_interpreter = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_musician = models.BooleanField(default=False)
    is_record_producer = models.BooleanField(default=False)
    society = models.ForeignKey('Society', null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField('Observação', blank=True)

    cpf_type = models.CharField('Tipo CPF', max_length=1, blank=True)
    cpf = models.CharField('CPF', max_length=11, blank=True)
    rg = models.CharField('RG', max_length=12, blank=True)
    doc_issuer = models.CharField('Órgão Emissor', max_length=14, blank=True)
    birth_date = models.DateField('Nascimento', blank=True)
    nationality = models.CharField('Nacionalidade', max_length=2, blank=True)
    profession = models.CharField('Profissão', max_length=30)
    marital_status = models.CharField('Estado Civil', max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True)
    sex = models.CharField('Sexo', max_length=10, choices=SEX_CHOICES, blank=True)

    trade_name = models.CharField('Nome Fantasia', max_length=100, blank=True)
    cnpj = models.CharField('CNPJ', max_length=16, blank=True)
    state_registration = models.CharField("Insc. Estadual", max_length=36, blank=True)
    municipal_registration = models.CharField("Insc. Municipal", max_length=36, blank=True)

    registered_in = models.DateField("Cadastrado em", default=date.today)
    updated_in = models.DateField("Atualizado em", default=date.today)
    #updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Atualizado por') 

    def clean(self):
        super().clean()
        if self.entity_type == self.ENTITY_TYPE_CHOICES[1][0]:
            if not self.cnpj:
                print('O campo CNPJ é obrigatório para pessoa jurídica')
                raise ValidationError('Pessoas jurídicas devem preencher o campo de CNPJ')
        elif self.entity_type == self.ENTITY_TYPE_CHOICES[0][0]:
            if not self.cpf:
                print('O campo de CPF é obrigatório para pessoa física')
                raise ValidationError('Pessoas físicas devem preencher o campo de CPF')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Titular'
        verbose_name_plural = 'Titulares'




    
