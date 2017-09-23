import http.client, urllib.request, urllib.parse, urllib.error, base64, json

def identify(file):
    
    subscription_key = '930ab871cde148b3a7dacc803a0b5451'
    uri_base = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0'

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = urllib.parse.urlencode({
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    
    body = ""
    filename = file
    f = open(filename, "rb")
    body = f.read()
    f.close()

    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    parsed = json.loads(data)
    string = []

    for line in range(len(parsed['regions'][0]['lines'])):
        group = []
        for word in parsed['regions'][0]['lines'][line]['words']:
            string.append({'text': str(word['text']), 'bounding_box': word['boundingBox']})

    conn.close()
    
    return string
