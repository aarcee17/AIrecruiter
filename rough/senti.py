from senginta.static.Google import GScholar

search_spider = GScholar('')
print(search_spider.to_json())

search_spider.get_all()