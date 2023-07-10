from enum import Enum

class City(Enum):
    # ISO 3166-2 city code
    TPE = 'Taipei'
    NWT = 'NewTaipei'
    TAO = 'Taoyuan'
    TXG = 'Taichung'
    TNN = 'Tainan'
    KHH = 'Kaohsiung'
    KEE = 'Keelung'
    HSZ = 'Hsinchu'
    HSQ = 'HsinchuCounty'
    MIA = 'MiaoliCounty'
    CHA = 'ChanghuaCounty'
    NAN = 'NantouCounty'
    YUN = 'YunlinCounty'
    CYQ = 'ChiayiCounty'
    CYI = 'Chiayi'
    PIF = 'PingtungCounty'
    ILA = 'YilanCounty'
    HUA = 'HualienCounty'
    TTT = 'TaitungCounty'
    KIN = 'KinmenCounty'
    PEN = 'PenghuCounty'
    LIE = 'LienchiangCounty'

class Direction(Enum):
    # 去返程 : [0:'去程'1:'返程'2:'迴圈'255:'未知']
    OUTBOUND = 0
    INBOUND = 1
    CYCLE = 2
    UNKNOWN = 255