import types

from xdbSearcher import XdbSearcher

dbpath = "ip2region.xdb"
cb = XdbSearcher.loadContentFromFile(dbfile=dbpath)
searcher = XdbSearcher(contentBuff=cb)


class DefaultObject:
    Nation = '0'
    City = '0'
    Company = '0'


def get_location(ip_address):
    ip = ip_address
    region_str = searcher.search(ip)
    key_list = ["Nation", "NationId", "City", "CityId", "Company"]  # 自行定义键
    value_list = region_str.split("|")
    modified_value_list = []
    for value in value_list:
        if value == '0':
            modified_value_list.append('未知')
        else:
            modified_value_list.append(value)
    result_dict = {key: value for key, value in zip(key_list, modified_value_list)}
    result_object = types.SimpleNamespace(**result_dict)
    return result_object

# if __name__ == '__main__':
#     target_ip = '123.45.67.89'
#     target = get_location(target_ip)
#     print(target)