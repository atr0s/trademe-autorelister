# trademe-autorelister and trademe class

This is a python command line proof of concept and a set of classes to list, relist and offer items.

The following classes are currently available:

- TrademeApiConnection: the API connection object. Takes a URL and credentials as parameters:

`a = TrademeApiConnection('https://api.tmsandbox.co.nz/v1',creds.oauthcreds)`

An example for the credentials is included in creds.py.dist 

In order for it to work a consumer key and secret + a user oauth key + secret are required. You need to make sure the user can at least read and write. The current classes can only retrieve info, relist and offer items.

- TrademeItem: an item abstraction, on top of the attributes returned by http://developer.trademe.co.nz/api-reference/listing-methods/retrieve-the-details-of-a-single-listing/ the following methods are currently available:

`quickRelist()`: relists the item if possible and returns a TrademeItem object for the new listing
`offer(price,offerDuration)`: offers an item for the price and duration specified. It currently offers it to all watchers/bidders.

- MyTradeMe
`unsoldItems(filter)`: retrieves a list of unsold TrademeItem objects with a filter specified, if none is specified it will list all unsold items in the last 45 days. List of possible filters can be found here: http://developer.trademe.co.nz/api-reference/my-trade-me-methods/retrieve-your-unsold-items/

`t.sellingItems()`: retrieves a list of TrademeItem objects currently being sold 

Automatically relist and/or offers Trademe auctions from your list

This is still work in progress, watch this space for more.

