import os
import logging
from distutils.util import strtobool
import kicost_digikey_api_v4.oauth.oauth2
from kicost_digikey_api_v4.exceptions import DigikeyError
from kicost_digikey_api_v4.v4.productinformation import (KeywordRequest, KeywordResponse, ProductDetails, DigiReelPricing,
                                           )
from kicost_digikey_api_v4.v4.productinformation.rest import ApiException

logger = logging.getLogger(__name__)


class DigikeyApiWrapper(object):
    def __init__(self, wrapped_function, module):
        self.sandbox = False

        apinames = {
            kicost_digikey_api_v4.v4.productinformation: 'products',
        }

        apiclasses = {
            kicost_digikey_api_v4.v4.productinformation: kicost_digikey_api_v4.v4.productinformation.ProductSearchApi,
        }

        apiname = apinames[module]
        apiclass = apiclasses[module]

        # Configure API key authorization: apiKeySecurity
        configuration = module.Configuration()
        configuration.api_key['X-DIGIKEY-Client-Id'] = os.getenv('DIGIKEY_CLIENT_ID')
        configuration.logger["package_logger"] = logger

        # Return quietly if no clientid has been set to prevent errors when importing the module
        if os.getenv('DIGIKEY_CLIENT_ID') is None or os.getenv('DIGIKEY_CLIENT_SECRET') is None:
            raise DigikeyError('Please provide a valid DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET in your env setup')

        # Use normal API by default, if DIGIKEY_CLIENT_SANDBOX is True use sandbox API
        configuration.host = 'https://api.digikey.com/' + apiname + '/v4'
        try:
            if bool(strtobool(os.getenv('DIGIKEY_CLIENT_SANDBOX'))):
                configuration.host = 'https://sandbox-api.digikey.com/' + apiname + '/v4'
                self.sandbox = True
        except (ValueError, AttributeError):
            pass

        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        # configuration.api_key_prefix['X-DIGIKEY-Client-Id'] = 'Bearer'

        # Configure OAuth2 access token for authorization: oauth2AccessCodeSecurity
        self._digikeyApiToken = kicost_digikey_api_v4.oauth.oauth2.TokenHandler(version=4, sandbox=self.sandbox).get_access_token()
        configuration.access_token = self._digikeyApiToken.access_token

        # create an instance of the API class
        self._api_instance = apiclass(module.ApiClient(configuration))

        # Populate reused ids
        self.authorization = self._digikeyApiToken.get_authorization()
        self.x_digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID')

        self.wrapped_function = wrapped_function

    @staticmethod
    def _remaining_requests(header, api_limits):
        try:
            rate_limit = header['X-RateLimit-Limit']
            rate_limit_rem = header['X-RateLimit-Remaining']

            if api_limits is not None and type(api_limits) == dict:
                api_limits['api_requests_limit'] = int(rate_limit)
                api_limits['api_requests_remaining'] = int(rate_limit_rem)

            logger.debug('Requests remaining: [{}/{}]'.format(rate_limit_rem, rate_limit))
        except (KeyError, ValueError) as e:
            logger.debug('No api limits returned -> {}: {}'.format(e.__class__.__name__, e))
            if api_limits is not None and type(api_limits) == dict:
                api_limits['api_requests_limit'] = None
                api_limits['api_requests_remaining'] = None

    @staticmethod
    def _store_api_statuscode(statuscode, status):
        if status is not None and type(status) == dict:
            status['code'] = int(statuscode)

        logger.debug('API returned code: {}'.format(statuscode))

    def call_api_function(self, *args, **kwargs):
        try:
            # If optional api_limits, status mutable object is passed use it to store API limits and status code
            api_limits = kwargs.pop('api_limits', None)
            status = kwargs.pop('status', None)

            func = getattr(self._api_instance, self.wrapped_function)
            logger.debug('CALL wrapped -> {}'.format(func.__qualname__))
            api_response = func(*args, self.x_digikey_client_id, authorization = self.authorization, **kwargs)
            self._remaining_requests(api_response[2], api_limits)
            self._store_api_statuscode(api_response[1], status)

            return api_response[0]
        except ApiException as e:
            if e.reason != 'Not Found' or logger.getEffectiveLevel() <= logging.DEBUG:
                logger.error('Exception when calling {}: {}'.format(self.wrapped_function, e))
            self._store_api_statuscode(e.status, status)


def keyword_search(*args, **kwargs) -> KeywordResponse:
    client = DigikeyApiWrapper('keyword_search_with_http_info', kicost_digikey_api_v4.v4.productinformation)

    if 'body' in kwargs and type(kwargs['body']) == KeywordRequest:
        logger.debug('Search for: {}'.format(kwargs["body"].keywords))
        logger.debug('CALL -> keyword_search')
        return client.call_api_function(*args, **kwargs)
    else:
        raise DigikeyError('Please provide a valid KeywordSearchRequest argument')


def product_details(*args, **kwargs) -> ProductDetails:
    client = DigikeyApiWrapper('product_details_with_http_info', kicost_digikey_api_v4.v4.productinformation)

    if len(args):
        logger.debug('Get product details for: {}'.format(args[0]))
        return client.call_api_function(*args, **kwargs)


def digi_reel_pricing(*args, **kwargs) -> DigiReelPricing:
    client = DigikeyApiWrapper('digi_reel_pricing_with_http_info', kicost_digikey_api_v4.v4.productinformation)

    if len(args):
        logger.debug('Calculate the DigiReel pricing for {} with quantity {}'.format(args[0], args[1]))
        return client.call_api_function(*args, **kwargs)


def suggested_parts(*args, **kwargs) -> ProductDetails:
    client = DigikeyApiWrapper('suggested_parts_with_http_info', kicost_digikey_api_v4.v4.productinformation)

    if len(args):
        logger.debug('Retrieve detailed product information and two suggested products for: {}'.format(args[0]))
        return client.call_api_function(*args, **kwargs)


# def manufacturer_product_details(*args, **kwargs): ??? Missing???!


def set_logger(lg):
    global logger
    logger = lg
