# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class DependentPhoneNumberList(ListResource):
    """  """

    def __init__(self, version, account_sid, address_sid):
        """
        Initialize the DependentPhoneNumberList

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param address_sid: The sid

        :returns: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberList
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberList
        """
        super(DependentPhoneNumberList, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'address_sid': address_sid}
        self._uri = '/Accounts/{account_sid}/Addresses/{address_sid}/DependentPhoneNumbers.json'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams DependentPhoneNumberInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(page_size=limits['page_size'])

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists DependentPhoneNumberInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance]
        """
        return list(self.stream(limit=limit, page_size=page_size))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of DependentPhoneNumberInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of DependentPhoneNumberInstance
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberPage
        """
        params = values.of({'PageToken': page_token, 'Page': page_number, 'PageSize': page_size})

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return DependentPhoneNumberPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of DependentPhoneNumberInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of DependentPhoneNumberInstance
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return DependentPhoneNumberPage(self._version, response, self._solution)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.DependentPhoneNumberList>'


class DependentPhoneNumberPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the DependentPhoneNumberPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The account_sid
        :param address_sid: The sid

        :returns: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberPage
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberPage
        """
        super(DependentPhoneNumberPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of DependentPhoneNumberInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance
        """
        return DependentPhoneNumberInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            address_sid=self._solution['address_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.DependentPhoneNumberPage>'


class DependentPhoneNumberInstance(InstanceResource):
    """  """

    class AddressRequirement(object):
        NONE = "none"
        ANY = "any"
        LOCAL = "local"
        FOREIGN = "foreign"

    class EmergencyStatus(object):
        ACTIVE = "Active"
        INACTIVE = "Inactive"

    def __init__(self, version, payload, account_sid, address_sid):
        """
        Initialize the DependentPhoneNumberInstance

        :returns: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance
        :rtype: twilio.rest.api.v2010.account.address.dependent_phone_number.DependentPhoneNumberInstance
        """
        super(DependentPhoneNumberInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'account_sid': payload['account_sid'],
            'friendly_name': payload['friendly_name'],
            'phone_number': payload['phone_number'],
            'voice_url': payload['voice_url'],
            'voice_method': payload['voice_method'],
            'voice_fallback_method': payload['voice_fallback_method'],
            'voice_fallback_url': payload['voice_fallback_url'],
            'voice_caller_id_lookup': payload['voice_caller_id_lookup'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'sms_fallback_method': payload['sms_fallback_method'],
            'sms_fallback_url': payload['sms_fallback_url'],
            'sms_method': payload['sms_method'],
            'sms_url': payload['sms_url'],
            'address_requirements': payload['address_requirements'],
            'capabilities': payload['capabilities'],
            'status_callback': payload['status_callback'],
            'status_callback_method': payload['status_callback_method'],
            'api_version': payload['api_version'],
            'sms_application_sid': payload['sms_application_sid'],
            'voice_application_sid': payload['voice_application_sid'],
            'trunk_sid': payload['trunk_sid'],
            'emergency_status': payload['emergency_status'],
            'emergency_address_sid': payload['emergency_address_sid'],
            'uri': payload['uri'],
        }

        # Context
        self._context = None
        self._solution = {'account_sid': account_sid, 'address_sid': address_sid}

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def friendly_name(self):
        """
        :returns: The friendly_name
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def phone_number(self):
        """
        :returns: The phone_number
        :rtype: unicode
        """
        return self._properties['phone_number']

    @property
    def voice_url(self):
        """
        :returns: The voice_url
        :rtype: unicode
        """
        return self._properties['voice_url']

    @property
    def voice_method(self):
        """
        :returns: The voice_method
        :rtype: unicode
        """
        return self._properties['voice_method']

    @property
    def voice_fallback_method(self):
        """
        :returns: The voice_fallback_method
        :rtype: unicode
        """
        return self._properties['voice_fallback_method']

    @property
    def voice_fallback_url(self):
        """
        :returns: The voice_fallback_url
        :rtype: unicode
        """
        return self._properties['voice_fallback_url']

    @property
    def voice_caller_id_lookup(self):
        """
        :returns: The voice_caller_id_lookup
        :rtype: bool
        """
        return self._properties['voice_caller_id_lookup']

    @property
    def date_created(self):
        """
        :returns: The date_created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date_updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def sms_fallback_method(self):
        """
        :returns: The sms_fallback_method
        :rtype: unicode
        """
        return self._properties['sms_fallback_method']

    @property
    def sms_fallback_url(self):
        """
        :returns: The sms_fallback_url
        :rtype: unicode
        """
        return self._properties['sms_fallback_url']

    @property
    def sms_method(self):
        """
        :returns: The sms_method
        :rtype: unicode
        """
        return self._properties['sms_method']

    @property
    def sms_url(self):
        """
        :returns: The sms_url
        :rtype: unicode
        """
        return self._properties['sms_url']

    @property
    def address_requirements(self):
        """
        :returns: The address_requirements
        :rtype: DependentPhoneNumberInstance.AddressRequirement
        """
        return self._properties['address_requirements']

    @property
    def capabilities(self):
        """
        :returns: The capabilities
        :rtype: dict
        """
        return self._properties['capabilities']

    @property
    def status_callback(self):
        """
        :returns: The status_callback
        :rtype: unicode
        """
        return self._properties['status_callback']

    @property
    def status_callback_method(self):
        """
        :returns: The status_callback_method
        :rtype: unicode
        """
        return self._properties['status_callback_method']

    @property
    def api_version(self):
        """
        :returns: The api_version
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def sms_application_sid(self):
        """
        :returns: The sms_application_sid
        :rtype: unicode
        """
        return self._properties['sms_application_sid']

    @property
    def voice_application_sid(self):
        """
        :returns: The voice_application_sid
        :rtype: unicode
        """
        return self._properties['voice_application_sid']

    @property
    def trunk_sid(self):
        """
        :returns: The trunk_sid
        :rtype: unicode
        """
        return self._properties['trunk_sid']

    @property
    def emergency_status(self):
        """
        :returns: The emergency_status
        :rtype: DependentPhoneNumberInstance.EmergencyStatus
        """
        return self._properties['emergency_status']

    @property
    def emergency_address_sid(self):
        """
        :returns: The emergency_address_sid
        :rtype: unicode
        """
        return self._properties['emergency_address_sid']

    @property
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.DependentPhoneNumberInstance>'
