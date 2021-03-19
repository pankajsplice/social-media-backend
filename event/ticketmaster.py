import ticketpy

# tm_client = ticketpy.ApiClient('X8Mlm2UNqERPNOmdLCH3fbA77Qo3GOuO')
#
# pages = tm_client.events.find(
#     classification_name='Sport',
# )
# concert_x = tm_client.events.by_id('17GOvbG62k5Z8yV')
# print(concert_x)
#
# concert_y = tm_client.events.by_id('Z698xZG2Zaaig')
# print(concert_y)
#
# festival_x = tm_client.events.by_id('Z698xZC2Z17CpF_')
# print(festival_x)
#
# # KZFzBErXgnZfZ7vAAn
# # competition_x = tm_client.events.by_id('17AZvbG62XkTsh4')
# # print(competition_x)
# for page in pages:
#     for event in page:
#         print(event)
#


class GetEventList:

    def __init__(self, name):
        self.name = name

    def fetch(self):
        tm_client = ticketpy.ApiClient('X8Mlm2UNqERPNOmdLCH3fbA77Qo3GOuO')
        pages = tm_client.events.find(classification_name=self.name)
        return pages




