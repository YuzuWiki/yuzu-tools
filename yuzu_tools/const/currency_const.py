from collections import OrderedDict as _OrderedDict

# 国家地区相关简写
AUSTRALIA = "au"  # 澳大利亚
UNITED_ARAB_EMIRATES = "ae"  # 阿拉伯联合酋长国
BRAZIL = "br"  # 巴西
CANADA = "ca"  # 加拿大
CHINA = "cn"  # 中国
DE = "de"  # 德国
SPAIN = "es"  # 西班牙
EGYPT = "eg"  # 埃及
FRANCE = "fr"  # 法国
INDIA = "in"  # 印度
ITALY = "it"  # 意大利
JAPAN = "jp"  # 日本
MEXICO = "mx"  # 墨西哥
HOLLANDA = "nl"  # 荷兰
TURKEY = "tr"  # 土耳其
SINGAPUR = "sg"  # 新加坡
SAUDI_ARABIA = "sa"  # 沙特阿拉伯
US = "us"  # 美国
UK = "uk"  # 英国

# 货币简写
CNY = "CNY"  # 人民币
RMB = "RMB"  # 人民币
USD = "USD"  # 美元
JPY = "JPY"  # 日元
GBP = "GBP"  # 英镑
EUR = "EUR"  # 欧元
AUD = "AUD"  # 澳元
HKD = "HKD"  # 港元
CAD = "CAD"  # 加元
KRW = "KRW"  # 韩元
INR = "INR"  # 印度卢比
IDR = "IDR"  # 印尼卢比
PHP = "PHP"  # 菲律宾比索
MXN = "MXN"  # 墨西哥比索
SGD = "SGD"  # 新加坡元
CHF = "CHF"  # 瑞士法郎
CZK = "CZK"  # 捷克克朗
DKK = "DKK"  # 丹麦克朗
HUF = "HUF"  # 匈牙利福林
ILS = "ILS"  # 以色列新谢克尔
NOK = "NOK"  # 挪威克朗
NZD = "NZD"  # 新西兰元
PLN = "PLN"  # 波兰兹罗提
RUB = "RUB"  # 俄罗斯卢布
SEK = "SEK"  # 瑞典克朗
THB = "THB"  # 泰铢
TWD = "TWD"  # 新台币
RUR = "RUR"  # 老俄国卢布

# 交易相关
CURRENCY_CODE_MAP = {
    USD: "$",
    EUR: "€",
    GBP: "￡",
    RMB: "¥",
    JPY: "￥",
    CNY: "¥"
}

CURRENCY_SYMBOL_DICT = {
    US:     "$",  # 美元
    DE:     "€",  # 德国，欧元
    FRANCE: "€",  # 法国，欧元
    ITALY:  "€",  # 意大利，欧元
    SPAIN:  "€",  # 西班牙，欧元
    UK:     "￡",  # 英镑
    CHINA:  "¥",  # 人民币
    JAPAN:  "￥",  # 日元
    INDIA:  "₨",  # 印度
    AUSTRALIA:  "$",  # 澳大利亚元
    CANADA:     "$",  # 加拿大元
    HOLLANDA:   "€",  # 荷兰站用欧元表示
    UNITED_ARAB_EMIRATES:   "ريال",  # 沙特阿拉伯 里亚尔
    BRAZIL:     "R$",  # 巴西 黑奥
    MEXICO:     "$",  # 墨西哥 用美元
    SINGAPUR:   "S$",  # 新加坡 新币
}

SHOP_CURRENCY_LIST = (
    USD,
    RMB,
)
GIFT_CURRENCY_LISTS = (
    USD,
    RMB,
    CNY,
    JPY,
    INR,
    GBP,
    RUR,
)

AMAZON_MWS_MARKETPLACE_ID_SITE_MAP = {
    "ATVPDKIKX0DER":    US,
    "A1F83G8C2ARO7P":   UK,
    "A1PA6795UKMFR9":   DE,
    "A13V1IB3VIYZZH":   FRANCE,
    "A1RKKUPIHCS9HS":   SPAIN,
    "APJ6JRA9NG5V4":    ITALY,
    "A1VC38T7YXB528":   JAPAN,
    "A2Q3Y263D00KWC":   BRAZIL,
    "A2EUQ1WTGCTBG2":   CANADA,
    "A1AM78C64UM0Y8":   MEXICO,
    "A2VIGQ35RCS4UG":   UNITED_ARAB_EMIRATES,
    "A21TJRUUN4KGV":    INDIA,
    "A33AVAJ2PDY3EV":   TURKEY,
    "A39IBJ37TRP1C6":   AUSTRALIA,
    "A1805IZSGTT6HS":   HOLLANDA
}

SUPPORT_SITE_LIST = (US, UK, INDIA, DE, CHINA, JAPAN, CANADA, FRANCE, ITALY, SPAIN, AUSTRALIA, BRAZIL,
                     MEXICO, UNITED_ARAB_EMIRATES, TURKEY, SINGAPUR, HOLLANDA, SAUDI_ARABIA)

AMAZON_MWS_SITE_DEVELOPER_ID_MAP = _OrderedDict(
    [
        (US,        {"id": "5558-9567-4656", "app_name": "liyuanqingshi"}),
        (UK,        {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
        (DE,        {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
        (FRANCE,    {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
        (ITALY,     {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
        (SPAIN,     {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
        (HOLLANDA,  {"id": "7054-2017-8246", "app_name": "zx-eu Ecommerce"}),
    ]
)
