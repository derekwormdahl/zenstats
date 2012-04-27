#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# copyright 2012 Google Inc. All Rights Reserved.
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

"""Reference command-line example for Google Analytics Core Reporting API v3.

This application demonstrates how to use the python client library to access
all the pieces of data returned by the Google Analytics Core Reporting API v3.

The application manages autorization by saving an OAuth2.0 token in a local
file and reusing the token for subsequent requests.

Before You Begin:

Update the client_secrets.json file

  You must update the clients_secrets.json file with a client id, client
  secret, and the redirect uri. You get these values by creating a new project
  in the Google APIs console and registering for OAuth2.0 for installed
  applications: https://code.google.com/apis/console

  Learn more about registering your analytics application here:
  http://code.google.com/apis/analytics/docs/gdata/v3/gdataAuthorization.html

Supply your TABLE_ID

  You will also need to identify from which profile to access data by
  specifying the TABLE_ID constant below. This value is of the form: ga:xxxx
  where xxxx is the profile ID. You can get the profile ID by either querying
  the Management API or by looking it up in the account settings of the
  Google Anlaytics web interface.

Sample Usage:

  $ python core_reporting_v3_reference.py

Also you can also get help on all the command-line flags the program
understands by running:

  $ python core_reporting_v3_reference.py --help
"""

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'

import sys
import sample_utils

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError


# The table ID is used to identify from which Google Anlaytics profile
# to retrieve data. This ID is in the format ga:xxxx where xxxx is the
# profile ID.
TABLE_ID = 'ga:56441937'


def main(argv):
  sample_utils.process_flags(argv)

  # Authenticate and construct service.
  service = sample_utils.initialize_service()

  # Try to make a request to the API. Print the results or handle errors.
  try:
    results = get_api_query(service).execute()
    print_results(results)

  except TypeError, error:
    # Handle errors in constructing a query.
    print ('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_api_query(service):
  """Returns a query object to retrieve data from the Core Reporting API.

  Args:
    service: The service object built by the Google API Python client library.
  """

  return service.data().ga().get(
      ids=TABLE_ID,
      start_date='2012-04-01',
      end_date='2012-04-22',
      metrics='ga:pageviews',
      #dimensions='ga:source,ga:keyword',
      dimensions='ga:hostname,ga:pagePath,ga:pageTitle,ga:city',
      sort='-ga:pageviews',
      #filters='ga:medium==organic',
      start_index='1',
      max_results='500')


def print_results(results):
  """Prints all the results in the Core Reporting API Response.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print_report_info(results)
  print_pagination_info(results)
  print_profile_info(results)
  print_query(results)
  print_column_headers(results)
  print_totals_for_all_results(results)
  print_rows(results)


def print_report_info(results):
  """Prints general information about this report.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Report Infos:'
  print 'Contains Sampled Data = %s' % results.get('containsSampledData')
  print 'Kind                  = %s' % results.get('kind')
  print 'ID                    = %s' % results.get('id')
  print 'Self Link             = %s' % results.get('selfLink')
  print


def print_pagination_info(results):
  """Prints common pagination details.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Pagination Infos:'
  print 'Items per page = %s' % results.get('itemsPerPage')
  print 'Total Results  = %s' % results.get('totalResults')

  # These only have values if other result pages exist.
  if results.get('previousLink'):
    print 'Previous Link  = %s' % results.get('previousLink')
  if results.get('nextLink'):
    print 'Next Link      = %s' % results.get('nextLink')
  print


def print_profile_info(results):
  """Prints information about the profile.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Profile Infos:'
  info = results.get('profileInfo')
  print 'Account Id      = %s' % info.get('accountId')
  print 'Web Property Id = %s' % info.get('webPropertyId')
  print 'Profile Id      = %s' % info.get('profileId')
  print 'Table Id        = %s' % info.get('tableId')
  print 'Profile Name    = %s' % info.get('profileName')
  print


def print_query(results):
  """The query returns the original report query as a dict.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Query Parameters:'
  query = results.get('query')
  for key, value in query.iteritems():
    print '%s = %s' % (key, value)
  print


def print_column_headers(results):
  """Prints the information for each column.

  The main data from the API is returned as rows of data. The column
  headers describe the names and types of each column in rows.


  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Column Headers:'
  headers = results.get('columnHeaders')
  for header in headers:
    # Print Dimension or Metric name.
    print '\t%s name:    = %s' % (header.get('columnType').title(),
                                  header.get('name'))
    print '\tColumn Type = %s' % header.get('columnType')
    print '\tData Type   = %s' % header.get('dataType')
    print


def print_totals_for_all_results(results):
  """Prints the total metric value for all pages the query matched.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Total Metrics For All Results:'
  print 'This query returned %s rows.' % len(results.get('rows'))
  print ('But the query matched %s total results.' %
         results.get('totalResults'))
  print 'Here are the metric totals for the matched total results.'
  totals = results.get('totalsForAllResults')

  for metric_name, metric_total in totals.iteritems():
    print 'Metric Name  = %s' % metric_name
    print 'Metric Total = %s' % metric_total
    print


def print_rows(results):
  """Prints all the rows of data returned by the API.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print 'Rows:'
  if results.get('rows', []):
    for row in results.get('rows'):
      print '\t'.join(row)
  else:
    print 'No Rows Found'


if __name__ == '__main__':
  main(sys.argv)
