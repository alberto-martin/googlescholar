# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScholarScraperItem(Item):
    # define the fields for your item here like:
    origin_url = Field()
    meta_source_format = Field()
    title = Field()
    title_link = Field()
    aut_pub_year = Field()
    cited_by = Field()
    cited_by_link = Field()
    related_link = Field()
    versions = Field()
    versions_link = Field()
    wos_cit = Field()
    wos_ut = Field()
    ft_link = Field()
    ft_format = Field()
    ft_text = Field()
    cited_cluster = Field()
    start_page = Field()
    