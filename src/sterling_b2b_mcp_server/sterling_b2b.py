import re
import requests
from requests.auth import HTTPBasicAuth
import time
import urllib3
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMMUNITY_API_URL = '/B2BAPIs/svc/communities/'
TRADING_API_URL = '/B2BAPIs/svc/tradingpartners/'

# @dataclass
# class SterlingB2BConfig:
#     url: str
#     # Optional credentials
#     username: Optional[str] = None
#     password: Optional[str] = None


@dataclass
class SterlingB2B:
    host: str
    username: str
    password: str
    verify_ssl: bool = True

    def __post_init__(self):
        self.base_url = f"{self.host.rstrip('/')}"
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


    # communityData = {
    #     'name': 'DEMO_SFG_COMMUNITY',
    #     'cdListening': True,
    #     'ftpListening': True,
    #     'partnerNotificationsEnabled': True,
    #     'partnersInitiateConnections': True,
    #     'partnersListenForConnections': True,
    #     'sshListening': True,
    #     'wsListening': True
    # }
    # def create_community(self, communityData):
    #     """Create a new community in Sterling B2Bi/Filegateway."""
    #     url = f"{self.base_url}{COMMUNITY_API_URL}"

    #     res = requests.post(url=url, auth=self.auth, json=communityData, headers=self.headers, verify=self.verify_ssl)

    #     if (res.status_code == 201):
    #         print( 'Community Created with Sucess %s\n' % (res) )
    #     else:
    #         print( 'Community NOT created-> %s\n' % (res) )

    #     return res.content

    def get_trading_partners(self, trading_partner_id: str = None) -> Optional[Dict[str, Any]]:
        """Get trading partners from Sterling B2Bi/Filegateway."""

        url = f"{self.base_url}{TRADING_API_URL}"

        search_for = ''
        if trading_partner_id is not None:
            if not re.match(r'^[\w\s-]+$', trading_partner_id):  # Allow alphanumerics, space, hyphen, underscore
                print("Invalid characters in trading_partner_id")
                return None
            search_for = f"%{trading_partner_id}%"

        params = {
            '_range': '0-100',
            'searchFor': search_for,
            '_include':'community'
        }

        res = requests.get(url=url, headers=self.headers, auth=self.auth, params=params, verify=self.verify_ssl)

        if (res.status_code != 200):
            print(f"Cannot Read Trading Partners \n requests.get -> {res.url} = {res}")
            return None

        return res.json()


    # strnow = datetime.now().strftime("_%Y%m%d_%H%M%S")
    # partnerData = {
    #     'username': 'demopartner' + strnow,
    #     'partnerName': 'REST_API_Partner' + strnow,
    #     'authenticationType': 'Local',
    #     'community': 'DEMO_SFG_COMMUNITY',
    #     'emailAddress': 'kk@ibm.com',
    #     'givenName': 'Demo',
    #     'isInitiatingConsumer': True,
    #     'isInitiatingProducer': True,
    #     'isListeningConsumer': False,
    #     'isListeningProducer': False,
    #     'doesUseSSH': True,
    #     'password': 'password',
    #     'phone':'1234567891',
    #     'postalCode': '12345',
    #     'surname': 'Partner'
    # }
    # def create_trading_partner(self, partnerData):
    #     """Create a new trading partner in Sterling B2Bi/Filegateway."""
    #     url = f"{self.base_url}{TRADING_API_URL}"

    #     res =  requests.post(url=url, auth=self.auth, json=partnerData, headers=self.headers, verify=self.verify_ssl)

    #     if (res.status_code != 200):
    #         print ('requests.post -> %s = %s\n' % (res.url, res) )
    #         print (res.content)
    #         return None;

    #     if (res.headers['Content-Type'] == 'application/json;charset=utf-8'):
    #         print(res.headers['Content-Type'])

    #     return res.json()
    
    def get_trading_partner_by_id(self, trading_partner_id: str) -> Optional[Dict[str, Any]]:
        """Get a Trading Partner by ID."""
        url = f"{self.base_url}{TRADING_API_URL}{trading_partner_id}"

        res = requests.get(url=url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)

        if (res.status_code != 200):
            print(f"Cannot Read Trading Partner by ID {trading_partner_id} requests.get -> {res.url} = {res}")
            return None

        return res.json()
    
    def get_communities(self):
        """Get communities from Sterling B2Bi/Filegateway."""
        url = f"{self.base_url}{COMMUNITY_API_URL}"

        res = requests.get(url=url, headers=self.headers, auth=self.auth, verify=self.verify_ssl)

        if (res.status_code != 200):
            print(f"Cannot Read Communities requests.get -> {res.url} = {res}")
            return None

        return res.json()