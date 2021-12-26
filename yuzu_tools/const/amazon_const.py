from . import currency_const as _CURRENCY_CONST

# amazon domain
DOMAIN_US = 'www.amazon.com'
DOMAIN_UK = 'www.amazon.co.uk'
DOMAIN_CA = 'www.amazon.ca'
DOMAIN_IN = 'www.amazon.in'
DOMAIN_CN = 'www.amazon.cn'
DOMAIN_JP = 'www.amazon.co.jp'
DOMAIN_DE = 'www.amazon.de'
DOMAIN_FR = 'www.amazon.fr'
DOMAIN_IT = 'www.amazon.it'
DOMAIN_ES = 'www.amazon.es'
DOMAIN_BR = 'www.amazon.com.br'
DOMAIN_AU = 'www.amazon.com.au'
DOMAIN_MX = 'www.amazon.com.mx'
DOMAIN_AE = 'www.amazon.ae'
DOMAIN_TR = 'www.amazon.com.tr'
DOMAIN_SG = 'www.amazon.sg'
DOMAIN_NL = 'www.amazon.nl'
DOMAIN_SMILE_US = 'smile.amazon.com'

DOMAIN_LIST = (
    DOMAIN_US, DOMAIN_UK, DOMAIN_CA, DOMAIN_IN, DOMAIN_CN, DOMAIN_JP, DOMAIN_DE, DOMAIN_FR,
    DOMAIN_IT, DOMAIN_ES, DOMAIN_BR, DOMAIN_AU, DOMAIN_MX, DOMAIN_AE, DOMAIN_TR, DOMAIN_SG,
    DOMAIN_NL, DOMAIN_SMILE_US
)

SITE_URL = {
    _CURRENCY_CONST.US:         DOMAIN_US,
    _CURRENCY_CONST.UK:         DOMAIN_UK,
    _CURRENCY_CONST.INDIA:      DOMAIN_IN,
    _CURRENCY_CONST.DE:         DOMAIN_DE,
    _CURRENCY_CONST.CHINA:      DOMAIN_CN,
    _CURRENCY_CONST.JAPAN:      DOMAIN_JP,
    _CURRENCY_CONST.CANADA:     DOMAIN_CA,
    _CURRENCY_CONST.FRANCE:     DOMAIN_FR,
    _CURRENCY_CONST.ITALY:      DOMAIN_IT,
    _CURRENCY_CONST.SPAIN:      DOMAIN_ES,
    _CURRENCY_CONST.AUSTRALIA:  DOMAIN_AU,
    _CURRENCY_CONST.BRAZIL:     DOMAIN_BR,
    _CURRENCY_CONST.MEXICO:     DOMAIN_MX,
    _CURRENCY_CONST.UNITED_ARAB_EMIRATES:   DOMAIN_AE,
    _CURRENCY_CONST.TURKEY:     DOMAIN_TR,
    _CURRENCY_CONST.SINGAPUR:   DOMAIN_SG,
    _CURRENCY_CONST.HOLLANDA:   DOMAIN_NL
}

URL_SITE = {
    DOMAIN_US: _CURRENCY_CONST.US,
    DOMAIN_UK: _CURRENCY_CONST.UK,
    DOMAIN_IN: _CURRENCY_CONST.INDIA,
    DOMAIN_DE: _CURRENCY_CONST.DE,
    DOMAIN_CN: _CURRENCY_CONST.CHINA,
    DOMAIN_JP: _CURRENCY_CONST.JAPAN,
    DOMAIN_CA: _CURRENCY_CONST.CANADA,
    DOMAIN_FR: _CURRENCY_CONST.FRANCE,
    DOMAIN_IT: _CURRENCY_CONST.ITALY,
    DOMAIN_ES: _CURRENCY_CONST.SPAIN,
    DOMAIN_AU: _CURRENCY_CONST.AUSTRALIA,
    DOMAIN_BR: _CURRENCY_CONST.BRAZIL,
    DOMAIN_MX: _CURRENCY_CONST.MEXICO,
    DOMAIN_AE: _CURRENCY_CONST.UNITED_ARAB_EMIRATES,
    DOMAIN_TR: _CURRENCY_CONST.TURKEY,
    DOMAIN_SG: _CURRENCY_CONST.SINGAPUR,
    DOMAIN_NL: _CURRENCY_CONST.HOLLANDA
}