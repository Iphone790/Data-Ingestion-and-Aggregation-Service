from rest_framework.throttling import UserRateThrottle


class EventThrottle(UserRateThrottle):

    scope = "event"