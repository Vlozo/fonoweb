from django.test import TestCase
from ..models import *

# Path-Handler for unit tests: fonoweb.core.tests.test_models.InsertTestCase

today = date(2024,1,12) # Use your actually date to validate tests with this parameter

class Holder_Creation_Test(TestCase):

    def test_create_PF_holder(self):
        holder = Holder(name="Ricardo Nunes Soares",
                        email = 'R-Soares@gmail.com',
                        origin = Holder.ORIGIN_TYPE_CHOICES[0][0],
                        entity_type = Holder.ENTITY_TYPE_CHOICES[0][0],
                        is_author = True,
                        is_interpreter = True,
                        is_record_producer = True,
                        cpf_type = Holder.CPF_TYPE_CHOICES[0][0],
                        cpf = '585.011.250-24')
        
        self.assertTrue(holder.entity_type == 'F')
        self.assertFalse(holder.is_musician)
        self.assertFalse(holder.cnpj)
        self.assertTrue(holder.registered_in == today)
    
    def test_create_PJ_holder(self):
        holder = Holder(name="BoogieWoogie Records",
                        email = 'contato@boogiewoogie.com.br',
                        origin = Holder.ORIGIN_TYPE_CHOICES[0][0],
                        entity_type = Holder.ENTITY_TYPE_CHOICES[1][0],
                        is_publisher = True,
                        is_record_producer = True,
                        trade_name = 'BoogieWoogie')
        
        self.assertTrue(holder.entity_type == 'J')
        self.assertFalse(holder.is_author)
        self.assertFalse(holder.cpf)
        self.assertTrue(holder.registered_in == today)
    
    def test_CNPJ_required(self):
        holder = Holder(name="WoogieBoogie Records",
                        origin = Holder.ORIGIN_TYPE_CHOICES[0][0],
                        entity_type = Holder.ENTITY_TYPE_CHOICES[1][0],
                        )
        
        with self.assertRaises(ValidationError): holder.full_clean()
    
    def test_CPF_required(self):
        holder = Holder(name="Adamastor Vieira Santos") # PF choices are preseted as default
        with self.assertRaises(ValidationError): holder.full_clean()


class Society_Creation_Test(TestCase):
    
    def test_create_society(self):
        society = Society(name = 'Mendigo de Calçada',
                          acronym = 'MDC')
        
        self.assertTrue(society.is_national)
        self.assertTrue(society.registered_in == today)
    
    def test_holder_society(self):
        society = Society(name = 'Mendigo de Calçada',
                          acronym = 'MDC')
        
        holder = Holder(name="Ricardo Nunes Soares",
                        cpf = '585.011.250-24',
                        society = Society(name='Fulano da Vitrine'))

        self.assertTrue(holder.society != society)


class Pseudonym_Creation_Test(TestCase):

    def test_create_pseudonym(self):
        holder = Holder(name="Ricardo Nunes Soares",
                        cpf = '585.011.250-24')
        
        pseudonym1 = Pseudonym(holder = holder,
                              pseudonym = "MC Rico")
        pseudonym2 = Pseudonym(holder = holder,
                               pseudonym = "Ricardinho do Trem Bala",
                               is_main = True)
        
        self.assertFalse(pseudonym1.is_main)
        self.assertTrue(pseudonym1.holder.name and pseudonym2.holder.name == "Ricardo Nunes Soares" )

    
        

    
    
        
