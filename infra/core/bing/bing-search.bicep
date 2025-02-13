metadata description = 'Creates a Bing Search Grounding instance.'
param name string
param location string = 'global'
param sku string = 'G1'
param tags object = {}

resource bing 'Microsoft.Bing/accounts@2020-06-10' = {
  name: name
  location: location
  kind: 'Bing.Grounding'
  tags: (contains(tags, 'Microsoft.Bing/accounts') ? tags['Microsoft.Bing/accounts'] : json('{}'))
  sku: {
    name: sku
  }
}

#disable-next-line outputs-should-not-contain-secrets
output bingApiKey string = bing.listKeys().key1
output endpoint string = 'https://api.bing.microsoft.com/'
output bingName string = bing.name

