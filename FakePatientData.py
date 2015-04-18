# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Fake Patient Data Generator

# <markdowncell>

# * Script to create some fake patient data with mixed distribution of the type of patient (donors,nondonor) for this exercise
# * Using this package http://fake-factory.readthedocs.org/en/v0.4/ to provide some fake info

# <codecell>

from faker import Factory
from faker.providers import BaseProvider
from random import randint
from pandas import ExcelWriter
import pandas as pd
import numpy as np

class AddressBook(BaseProvider):
    
    # AddressBook as a Fake Provider
    # Some street names, prefixes, residential and commercial types
    street_names = ('Yew', 'Walnut', 'Tupelo', 'Tamarack', 'Tallowwood', 'Tallowtree', 'Sycamore', 'Sweetleaf', 'Sweetbay', 
                    'Sumac', 'Sugarberry', 'Strawberry', 'Spruce', 'Spirea', 'Sourwood', 'Snowberry', 'Silverbell', 
                    'Silver','Silk','Sequoia','Satinwood','Satinleaf','Roseberry', 'Rose', 'Redwood', 'Redcedar', 'Redbud',
                    'Poplar', 'Plum', 'Pine', 'Persimmon', 'Pecan', 'Pear', 'Peach', 'Palm', 'Olive', 'Oak', 'Myrtle',
                    'Mulberry', 'Mountain', 'Marlberry', 'Maple', 'Mangrove', 'Mahogany', 'Magnolia', 'Larch', 'Juniper', 
                    'Jasmine', 'Hornbeam', 'Hoptree', 'Holly', 'Hickory', 'Hibiscus', 'Hemlock', 'Hazelnut', 'Hawthorn',
                    'Hackberry', 'Gallberry', 'Fir', 'Filbert', 'Fig', 'Elm', 'Elder', 'Dogwood', 'Devilwood', 'Desertwillow',
                    'Deer', 'Cypress', 'Cranberry', 'Cottonwood', 'Chestnut', 'Cherry', 'Cedar', 'Buttonbush', 'Butternut',
                    'Buckwheat', 'Buckthorn', 'Buckeye', 'Birch', 'Beech', 'Bayberry', 'Basswood', 'Aspen', 'Ash', 'Arrowwood',
                    'Arbor','Aralia','Apricot','Apple','Almond','Alder','Acacia')
    
    street_prefix = ('', 'North', 'N','North West', 'NW','North East', 'NE','South', 'S', 'South West', 'SW', 'South East', 'SE', 'West', 'W', 'East', 'E')
    street_type = ('', 'Street', 'St.', 'Ave', 'Avenue')
    res_type = ('', 'Apt.')
    com_type = ('Suite', 'STE')
    
    # create a few donor clinics
    clinics = []
    for i in range(np.random.randint(5, 10)):
        clinic_address = str(np.random.randint(100, 9000)) + ' ' + np.random.choice(street_prefix, 1)[0] + ' ' \
        + np.random.choice(street_names, 1)[0] + ' ' + np.random.choice(street_type, 1)[0] 
        clinic_address = clinic_address + ' ' + np.random.choice(com_type, 1)[0] + ' ' + str(np.random.randint(100, 9000))
        zipcode = fake.postcode().split("-")[0]
        clinics.append({'address':clinic_address, 'zipcode':zipcode})

    @classmethod
    def get_clinic(cls):
        return cls.random_element(cls.clinics)
        
    @classmethod
    def get_street(cls):
        return cls.random_element(cls.street_names)
    
    @classmethod
    def get_street_prefix(cls):
        return cls.random_element(cls.street_prefix)
    
    @classmethod
    def get_street_type(cls):
        return cls.random_element(cls.street_type)
    
    @classmethod
    def get_res_type(cls):
        return cls.random_element(cls.res_type)
    

# <headingcell level=2>

# Patient class with two types of patients, Donors and NonDonors

# <markdowncell>

# * Have three types of forms of payment (client (i.e. payed by the clinic), self and insurance)
# * Only nondonors can be linked  (i.e. spouse/partner etc..)
# * Use probability distribution to simulate real world example of the mixed patient types

# <codecell>

class Patient(object):
    
    # some probabilities for payment and converting strings
    payment_type = {"insurance":0.5, "self":0.5}
    change_case = {"upper":0.2, "lower":0.2, "no":0.6}
    CHAR_SET = string.ascii_uppercase + string.digits
    
    def __init__(self, **kwargs):
        self.patient_id = kwargs.pop('patient_id', None)
        self.last_name = kwargs.pop('last_name', None)
        self.first_name = kwargs.pop('first_name', None)
        self.partner = kwargs.pop('partner', None)
        self.patient_type = kwargs.pop('patient_type', None)
        self.gender = kwargs.pop('gender', None)
        self.payment_type = kwargs.pop('payment_type', None)
        self.insurance_num = kwargs.pop('insurance_num', None)
        self.address = kwargs.pop('address', None)
        self.zipcode = kwargs.pop('zipcode', None)
        self.has_partner = kwargs.pop('has_partner', False)
        self.accessioned_date = fake.date_time_between(start_date='-3y', end_date='now').strftime('%m/%d/%Y')
    
    # create fake id, names,address,zipcode,insurance
    def fake_name(self):
        if self.gender == 'F':
            self.last_name = fake.last_name_female()
            self.first_name = fake.first_name_female()
        elif self.gender == 'M':
            self.last_name = fake.last_name_male()
            self.first_name = fake.first_name_male()
            
    def fake_address(self):
        # random string case to simulate real data
        case = fake.random_element(Patient.change_case)
        if case == 'upper':
            self.address = fake.get_street_prefix().upper() + ' ' + fake.get_street() + ' ' + \
            fake.get_street_type() + ' ' + fake.get_res_type() + ' ' + fake.building_number()
        elif case == 'lower':
            self.address = fake.get_street_prefix() + ' ' + fake.get_street() + ' ' + fake.get_street_type().lower() + \
            ' ' + fake.get_res_type() + ' ' + fake.building_number()
        else:
            self.address = fake.get_street_prefix() + ' ' + fake.get_street() + ' ' + fake.get_street_type() + ' ' \
            + fake.get_res_type() + ' ' + fake.building_number()

    def fake_insurance(self):
        # some clients will have insurance others will pay themselves
        self.payment_type = fake.random_element(Patient.payment_type)
        if self.payment_type == 'insurance':
            self.insurance_num = ''.join(random.sample(Patient.CHAR_SET*8, 12)) 
    
    def fake_zipcode(self):
        self.zipcode = fake.postcode().split("-")[0]
        
class Donor(Patient):
    
    def __init__(self, **kwargs):
        super(Donor, self).__init__(**kwargs)
        super(Donor, self).fake_name()
        clinic = fake.get_clinic()
        self.address = clinic['address']
        self.zipcode = clinic['zipcode']
    
    def get_patient_info(self):
        return self.__dict__
    
    def get_patient_item(self, key):
        return self.__dict__[key]
    
class NonDonor(Patient):
    
    def __init__(self, **kwargs):
        super(NonDonor, self).__init__(**kwargs)
        super(NonDonor, self).fake_name()
        super(NonDonor, self).fake_address()
        super(NonDonor, self).fake_zipcode()
        super(NonDonor, self).fake_insurance()

    def get_patient_info(self):
        return self.__dict__
    
    def get_patient_item(self, key):
        return self.__dict__[key]
    
    def set_patient_item(self, key, value):
        self.__dict__[key] = value
    
    # update common patient/partner fields
    def update_patient_info(self, last_name, address, zipcode, insurance):
        last_names = [self.last_name, last_name + '-' + self.last_name, last_name]
        # have ~ 1/3 equal distribution of last name possibilities
        random_last_name = np.random.choice(last_names, 1, p=[0.33,0.34,0.33])[0]
        self.last_name = random_last_name
        if insurance is not None:
            insurance_num = [insurance,insurance + str(1)]
            random_insurance = np.random.choice(insurance_num, 1, p=[0.5,0.5])[0]
            self.insurance_num = random_insurance
        case = fake.random_element(Patient.change_case)
        if case == 'upper':
            self.address = address.upper()
        elif case == 'lower':
            self.address = address.lower()
        else:
            self.address = address
        self.zipcode = zipcode

# create patients records
def create_patients(fake, seed, total=1000, prob=[0.1, 0.25, 0.65]):

    np.random.seed(seed)
    # create X distribution of patients, partner is linked to a nondonor
    patient_type = ['donor', 'partner', 'nondonor']
    # provide sufficient number of ids
    patient_ids = random.sample(range(1,total*3), total*2)
    patient_types = np.random.choice(patient_type, total, p=prob)
    # append patients
    patient_data = []
    
    # create patients based on patient type
    for pt in patient_types:
        if pt == 'donor':
            donor = Donor(patient_id="PAT000" + str(patient_ids.pop()), patient_type='donor', gender=fake.random_element({"M":0.75, "F":0.25}), payment_type='client')
            patient_data.append(donor.get_patient_info())
        elif pt == 'nondonor':
            nondonor = NonDonor(patient_id="PAT000" + str(patient_ids.pop()), patient_type='nondonor', gender=fake.random_element({"M":0.25, "F":0.75}))
            patient_data.append(nondonor.get_patient_info())
        elif pt == 'partner':
            nondonor = NonDonor(patient_id="PAT000" + str(patient_ids.pop()), patient_type='nondonor', gender='F', has_partner=True)
            partner = NonDonor(patient_id="PAT000" + str(patient_ids.pop()), patient_type='nondonor', gender='M', partner=nondonor.get_patient_item('patient_id'), has_partner=True)
            partner.update_patient_info(last_name=nondonor.get_patient_item('last_name'),
                                         address=nondonor.get_patient_item('address'),
                                         zipcode=nondonor.get_patient_item('zipcode'),
                                         insurance=nondonor.get_patient_item('insurance_num'))
            nondonor.set_patient_item('partner', partner.get_patient_item('patient_id'))
            if partner.get_patient_item('payment_type') == 'self':
                partner.set_patient_item('insurance_num',None)
                
            patient_data.append(nondonor.get_patient_info())
            patient_data.append(partner.get_patient_info())
    return patient_data

# <markdowncell>

# * Use random seed to recreate the same results
# * Can create a database of any size for this exercise
# * Output results to excel using pandas

# <codecell>

if __name__ == "__main__":
    # can use different names/addresses based on geography
    fake = Factory.create('en_US')
    # add custom address
    fake.add_provider(AddressBook)
    data = create_patients(fake, seed=fake.seed(1234), total=5000)
    # convert list of dictionaries to a pandas dataframe
    dataframe = pd.DataFrame(data)
    dataframe.sort(['patient_id'], ascending=[True], inplace=True)
    workbook = pd.ExcelWriter('patient_data.xlsx', engine='xlsxwriter')
    # write out to excel using pandas function
    dataframe[['patient_id', 'last_name', 'first_name', 'gender', 'patient_type', 'partner', 'address',
               'zipcode', 'payment_type', 'insurance_num', 'has_partner', 'accessioned_date']].to_excel(workbook, sheet_name = 'Patient Data'
                                                                                    , index = False)
    workbook.save()

# <codecell>


