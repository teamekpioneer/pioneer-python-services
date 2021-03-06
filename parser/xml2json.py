import xmltodict
from pymongo import MongoClient


# Connection string and database
client = MongoClient('localhost', 27017)
db = client.test


def parse_branded_fares_shopping(xml_file):
    """Parse branded fares shopping xml file xml_file and return a dictionary result_dict"""

    result_dict = {}

    with open(xml_file, "rb") as f:
        document = xmltodict.parse(f, xml_attribs=True)

    soap = document['SOAP-ENV:Envelope']
    client_transaction_id = soap['SOAP-ENV:Header']['ns2:securityHeader']['ns2:serviceSecurityHeader']['ns2:clientTransactionId']

    branded_fares_shopping_body = soap['SOAP-ENV:Body']['ns2:brandedFaresShoppingRequest']['ns2:brandedFaresShopping']['ns2:brandedFaresShoppingBody']

    sales_info = branded_fares_shopping_body['ns2:salesInfo']
    sales_info['currencyCode'] = sales_info.pop('ns2:currencyCode')
    sales_info['pointOfSale'] = sales_info.pop('ns2:pointOfSale')
    sales_info['pointOfSaleCountryCode'] = sales_info.pop('ns2:pointOfSaleCountryCode')
    sales_info['pointOfTicketCountryCode'] = sales_info.pop('ns2:pointOfTicketCountryCode')

    carrier_code = branded_fares_shopping_body['ns2:carrierCode']

    onward_travel_details = branded_fares_shopping_body['ns2:onwardTravelDetails']
    onward_travel_details['originAirport'] = onward_travel_details.pop('ns2:originAirport')
    onward_travel_details['originCity'] = onward_travel_details.pop('ns2:originCity')
    onward_travel_details['destinationAirport'] = onward_travel_details.pop('ns2:destinationAirport')
    onward_travel_details['destinationCity'] = onward_travel_details.pop('ns2:destinationCity')
    onward_travel_details['departureDate'] = onward_travel_details.pop('ns2:departureDate')
    onward_travel_details['cabinClass'] = onward_travel_details.pop('ns2:cabinClass')

    return_travel_details = None

    if 'ns2:returnTravelDetails' in branded_fares_shopping_body:
        return_travel_details = branded_fares_shopping_body['ns2:returnTravelDetails']
        return_travel_details['originAirport'] = return_travel_details.pop('ns2:originAirport')
        return_travel_details['originCity'] = return_travel_details.pop('ns2:originCity')
        return_travel_details['destinationAirport'] = return_travel_details.pop('ns2:destinationAirport')
        return_travel_details['destinationCity'] = return_travel_details.pop('ns2:destinationCity')
        return_travel_details['departureDate'] = return_travel_details.pop('ns2:departureDate')
        return_travel_details['cabinClass'] = return_travel_details.pop('ns2:cabinClass')

    is_redemption = branded_fares_shopping_body['ns2:isRedemption']

    result_dict['clientTransactionId'] = client_transaction_id
    result_dict['salesInfo'] = sales_info
    result_dict['carrierCode'] = carrier_code
    result_dict['onwardTravelDetails'] = onward_travel_details

    if return_travel_details:
        result_dict['returnTravelDetails'] = return_travel_details

    result_dict['isRedemption'] = is_redemption

    return result_dict


def main():

    try:
        print('... Parsing brandedfaresshopping-rq ...')
        result_dict = parse_branded_fares_shopping("brandedfaresshopping-rq.xml")
        print('Completed Parsing')

        print('... Inserting to brandedfaresshopping collection ...')
        db.brandedfaresshopping.insert(result_dict)
        print('Completed inserting to brandedfaresshopping collection ')

    except IOError as e:
        print(e)
    except ImportError as ie:
        print(ie)
    except NameError as ne:
        print(ne)
    except Exception as ex:
        print('Unexpected Error' + ex)

if __name__ == "__main__":
    main()