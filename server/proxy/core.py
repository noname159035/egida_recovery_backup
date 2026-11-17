from database.database import DatabaseManager
from server.classifier.classifier import ClassifierManager
from argon2 import PasswordHasher

db = DatabaseManager()
cm = ClassifierManager()
ph = PasswordHasher()