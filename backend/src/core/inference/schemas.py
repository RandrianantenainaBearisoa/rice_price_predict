from pydantic import BaseModel, ValidationError, PositiveFloat, field_validator
from enum import Enum

class Region(str, Enum):
    Alaotra_Mangoro = 'Alaotra Mangoro'
    Amoron_I_Mania = 'Amoron I Mania'
    Analamanga = 'Analamanga'
    Analanjirofo = 'Analanjirofo'
    Androy = 'Androy'
    Anosy = 'Anosy'
    Atsimo_Andrefana = 'Atsimo Andrefana'
    Atsimo_Atsinanana = 'Atsimo Atsinanana'
    Atsinanana = 'Atsinanana'
    Betsiboka = 'Betsiboka'
    Boeny = 'Boeny'
    Bongolava = 'Bongolava'
    Diana = 'Diana'
    Haute_Matsiatra = 'Haute Matsiatra'
    Ihorombe = 'Ihorombe'
    Itasy = 'Itasy'
    Menabe = 'Menabe'
    Sava = 'Sava'
    Sofia = 'Sofia'
    Vakinankaratra = 'Vakinankaratra'
    Vatovavy_Fitovinany = 'Vatovavy Fitovinany'

class Commodity(str, Enum):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def get_selected_feature(self):
        return self.value["value"]

    def get_features_list(cls):
        return list(cls.__members__.keys())
    
    Rice_Imported = {
        "value": 'Rice_Imported',
        "feature": "Rice (imported)",
        "labels": {'fr': 'Riz (importé)', 'en': 'Rice (imported)'}
        }

    Rice_Local = {
        "value": 'Rice_Local',
        "feature": "Rice (local)",
        "labels": {'fr': 'Riz (local)', 'en': 'Rice (local)'}
        }

class Month(str, Enum):
    def __new__(cls, value):
            obj = str.__new__(cls, value)
            obj._value_ = (value)
            return obj
        
    month_1 = {
        "value": 'month_1',
        "feature": 'month_1',
        "labels": {'fr': 'Janvier', 'en': 'January'}
        }
    month_2 = {
        "value": 'month_2',
        "feature": 'month_2',
        "labels": {'fr': 'Février', 'en': 'February'}
        }
    month_3 = {
        "value": 'month_3',
        "feature": 'month_3',
        "labels": {'fr': 'Mars', 'en': 'March'}
        }
    month_4 = {
        "value": 'month_4',
        "feature": 'month_4',
        "labels": {'fr': 'Avril', 'en': 'April'}
        }
    month_5 = {
        "value": 'month_5',
        "feature": 'month_5',
        "labels": {'fr': 'Mai', 'en': 'May'}
        }
    month_6 = {
        "value": 'month_6',
        "feature": 'month_6',
        "labels": {'fr': 'Juin', 'en': 'June'}
        }
    month_7 = {
        "value": 'month_7',
        "feature": 'month_7',
        "labels": {'fr': 'Juillet', 'en': 'July'}
        }
    month_8 = {
        "value": 'month_8',
        "feature": 'month_8',
        "labels": {'fr': 'Août', 'en': 'August'}
        }
    month_9 = {
        "value": 'month_9',
        "feature": 'month_9',
        "labels": {'fr': 'Septembre', 'en': 'September'}
        }
    month_10 = {
        "value": 'month_10',
        "feature": 'month_10',
        "labels": {'fr': 'Octobre', 'en': 'October'}
        }
    month_11 = {
        "value": 'month_11',
        "feature": 'month_11',
        "labels": {'fr': 'Novembre', 'en': 'November'}
        }
    month_12 = {
        "value": 'month_12',
        "feature": 'month_12',
        "labels": {'fr': 'Décembre', 'en': 'December'}
        }

class InferenceInput(BaseModel):
    gasoline_price: PositiveFloat
    diesel_price: PositiveFloat
    usd_to_mga: PositiveFloat
    region: Region
    commodity: Commodity
    month: Month

    @field_validator("region", "commodity", "month", mode="before")
    @classmethod
    def validate_key(cls, value):
        if value in Region.__members__:
            return Region[value].value
        if value in Commodity.__members__:
            return Commodity[value].value
        if value in Month.__members__:
            return Month[value].value
        return value
