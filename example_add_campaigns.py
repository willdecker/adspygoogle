#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example adds campaigns. To get campaigns, run get_campaigns.py.

Tags: CampaignService.mutate
Tags: BudgetService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import datetime
import os
import sys
import example_config

"""
modified and placed above the AdWordsClient import to make the script look for relatively close copy versus the root installed version.
"""
sys.path.insert(0, '..')

"""
modified to use local libraries and generate oauth2.0 credentials
"""
# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
# Import OAuth 2.0 to support adwords API call
from oauth2client.client import OAuth2Credentials

"""
added to attempt to override the logger in the config and write to standard out versus a temp file
"""
logger = logging.getLogger('adspygoogle')

"""
added name, amt and method variables to function.
name is camapaign name
amt is budget amount
method is delivery method
"""
def main(client, name, amt='1', method='STANDARD'):
  # Initialize appropriate services.
  campaign_service = client.GetCampaignService(version='v201306')
  budget_service = client.GetBudgetService(version='v201306')

  # Create a budget, which can be shared by multiple campaigns.
  budget = {
      'name': 'Interplanetary budget #%s' % Utils.GetUniqueName(),
      'amount': {
          'microAmount': amt
      },
      'deliveryMethod': method,
      'period': 'DAILY'
  }

  budget_operations = [{
      'operator': 'ADD',
      'operand': budget
  }]

  # Add the budget.
  budget_id = budget_service.Mutate(budget_operations)[0]['value'][0][
      'budgetId']

  # Construct operations and add campaigns.
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': name,
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPC',
              'biddingScheme': {
                  'xsi_type': 'ManualCpcBiddingScheme',
                  'enhancedCpcEnabled': 'false'
              }
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'networkSetting': {
              'targetGoogleSearch': 'true',
              'targetSearchNetwork': 'true',
              'targetContentNetwork': 'false',
              'targetPartnerSearchNetwork': 'false'
          },
          # Optional fields
          'startDate': (datetime.datetime.now() +
                        datetime.timedelta(1)).strftime('%Y%m%d'),
          'adServingOptimizationStatus': 'ROTATE',
          'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          },
          'settings': [
              {
                  'xsi_type': 'GeoTargetTypeSetting',
                  'positiveGeoTargetType': 'DONT_CARE',
                  'negativeGeoTargetType': 'DONT_CARE'
              },
              {
                  'xsi_type': 'KeywordMatchSetting',
                  'optIn': 'true'
              }
          ]
      }]
  campaigns = campaign_service.Mutate(operations)[0]

def add_campaign(client, name, amt, method):
    ad_useragent = example_config.AD_USER_AGENT
    ad_devtoken = example_config.ADWORDS_DEVELOPER_TOKEN
    ad_debug = example_config.AD_DEBUG
    ad_clientid = example_config.AD_CLIENT_ID
    ad_clientsecret = example_config.AD_CLIENT_SECRET
    ad_refreshtoken = example_config.AD_REFRESH_TOKEN
    ad_clientcustid = example_config.AD_CLIENT_CUST_ID
    ad_oauth2credentials = OAuth2Credentials(
        None, ad_clientid, ad_clientsecret, ad_refreshtoken,
        datetime.datetime(1980, 1, 1, 12), 'https://accounts.google.com/o/oauth2/token',
        'Google Ads* Python Client Library')
    ad_headers = {
    'oauth2credentials': ad_oauth2credentials,
    'userAgent': ad_useragent,
    'developerToken': ad_devtoken,
    'clientCustomerId': ad_clientcustid
    }
    ad_config = {
    'debug': ad_debug,
    'xml_log': 'n',
    'request_log': 'n',
    'pretty_xml': 'n',
    'xml_parser': '2',
    'compress': 'n'
    }
    client = AdWordsClient(path='.', headers=ad_headers, config=ad_config)
    main(client=client, name='Example Campaign', amt='30000000')

