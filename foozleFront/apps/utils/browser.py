import httpagentparser


def get_browser_from_useragent(useragent):
    return httpagentparser.simple_detect(useragent)[1]


def get_so_from_useragent(useragent):
    pass