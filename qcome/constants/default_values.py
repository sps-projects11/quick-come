from enum import Enum

class Role(Enum):
    ADMIN = 1
    END_USER = 2
    SUPER_ADMIN = 3


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class Status(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELLED = 4

    
class Vehicle_Type(Enum):
    CAR = 1
    BIKE = 2



    
class PayType(Enum):
    CASHONDELIVERY = 1
    NETBANKING = 2
    UPI = 3

class PayStatus(Enum):
    PENDING = 1
    COMPLETE = 2
    FAILED = 3


class ResponseMessageType(Enum):
    SUCCESS='success'
    ERROR='error'
    WARNING='warning'
    INFO='info'
    NONE='null'