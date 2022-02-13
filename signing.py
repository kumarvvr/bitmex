import hashlib
import hmac

def _generate_signature(data, apisecret):
    key = apisecret # Defined as a simple string.
    key_bytes= bytes(key , 'latin-1')
    data_bytes = bytes(data, 'latin-1') # Assumes `data` is also a string.
    return hmac.new(key_bytes, data_bytes , hashlib.sha256).hexdigest()

def bitmex_signature(secret, verb, url, nonce, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    # parsedURL = urlparse(url)
    # path = parsedURL.path
    # if parsedURL.query:
    #     path = path + '?' + parsedURL.query

    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf-8')


    message = verb + url + str(nonce) + data

    signature = hmac.new(bytes(secret, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
    return signature





if __name__ == '__main__':
    data = 'POST/api/v1/order1429631577995{"symbol":"XBTM15","price":219.0,"clOrdID":"mm_bitmex_1a/oemUeQ4CAJZgP3fjHsA","orderQty":98}'
    apisecret = 'chNOOS4KvNXR_Xq4k4c9qsfoKWvnDecLATCRlcBwyKDYnWgO'
    result = '93912e048daa5387759505a76c28d6e92c6a0d782504fc9980f4fb8adfc13e25'

    computed = bitmex_signature(apisecret,"POST","/api/v1/order","1429631577995",'{"symbol":"XBTM15","price":219.0,"clOrdID":"mm_bitmex_1a/oemUeQ4CAJZgP3fjHsA","orderQty":98}')
    if(result == computed):
        print("Matched")
    else:
        print("Error")