# coding: utf-8

"""
    WeGlide Integration Test

    This test verifies that the WeGlide Python client can successfully connect to the API.
    It requires an internet connection and access to the WeGlide API.

    To run this test:
        python -m unittest test.test_integration
"""

import os
import unittest
from weglide_client.api_client import ApiClient
from weglide_client.configuration import Configuration
from weglide_client.api.airport_api import AirportApi  # Example of a likely public endpoint
from weglide_client.exceptions import ApiException


class TestIntegration(unittest.TestCase):
    """Integration test for the WeGlide client library.
    
    This test verifies that the client can successfully connect to the API.
    """
    
    def setUp(self):
        """Set up the API client for all tests."""
        # Configure API client
        self.config = Configuration()
        self.config.host = os.environ.get('WEGLIDE_API_URL', 'https://api.weglide.org')
        self.client = ApiClient(self.config)
        
        # Initialize API instance for a public endpoint
        self.airport_api = AirportApi(self.client)
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_api_connection(self):
        """Test that the client can connect to the API using a public endpoint."""
        try:
            # Attempt to get an airport with ID 1 with a timeout
            # The _request_timeout parameter sets a timeout for the request
            response = self.airport_api.get_airport_v1_airport_id_get(id=161522, _request_timeout=10)
            
            # Verify the response
            self.assertIsNotNone(response)
            
            # Basic verification that we received data
            print(f"Successfully connected to the API. Response type: {type(response)}")
            
        except ApiException as e:
            if e.status == 401:
                self.skipTest("Endpoint requires authentication. Skipping test.")
            elif e.status == 404:
                self.skipTest("Endpoint not found. Might have been moved or renamed.")
            else:
                self.fail(f"API error: {e}")
        except Exception as e:
            self.fail(f"Unexpected error: {e}")


if __name__ == '__main__':
    unittest.main()