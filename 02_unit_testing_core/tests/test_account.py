"""
Test Cases TestAccountModel
"""
import json
from unittest import TestCase
from models import db
from models.account import Account

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """Connect to database and load test data once before all tests"""

    @classmethod
    def tearDownClass(cls):
        """Disconnect from database after running all tests"""

    def setUp(self):
        """Truncate tables before each test to guarantee isolation"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
