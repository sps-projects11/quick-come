from enum import Enum


class ErrorMessage(Enum):
    E00001 = "Login failed, please try again"
    E00002 = "Invalid date format for DOB. Please use YYYY-MM-DD."
    E00003 = "Please enter your email address first."
    E00004 = "Email is already registered."
    E00005 = "OTP expired. Please request a new one."
    E00006 = "Invalid OTP."
    E00007 = "Password doesn't match."
    E00008 = "Email not verified."
    E00009 = "Invalid email or password."
    E00010 = "User Doesn't Exists."
    
    