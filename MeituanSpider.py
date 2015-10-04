# coding=utf-8
__author__ = 'shibotian'

from bs4 import BeautifulSoup
import urllib2
import json

url = 'http://waimai.meituan.com/home/wx4eqz733tgq'

# 处理cookie
cookie_file = open('cookie.json')
cookie_dict = json.load(cookie_file)
cookie_str = ''
req = urllib2.Request(url)
for cookie_item in cookie_dict:
    cookie_str += '{0:s}={1:s};'.format(cookie_item['name'], cookie_item['value'])
req.add_header('Cookie', cookie_str)

# 读网页
print 'dumping web...'
response = urllib2.urlopen(req)
html = response.read()


# 解析数据
print 'analyzing....'
soup_meituan = BeautifulSoup(html)
restaurant_list = []
restaurant_soup_list = soup_meituan.find_all('li', attrs={'class': 'fl rest-li'})
for restaurant in restaurant_soup_list:
    restaurant_dict = {}
    restaurant_dict['restaurant_name'] = restaurant.find('div', attrs={'class': 'restaurant'})['data-title']
    restaurant_dict['start_price'] = float(restaurant.find('span', attrs={'class': 'start-price'}).get_text().split(u'￥')[-1])
    send_price = restaurant.find('span', attrs={'class': 'send-price'}).get_text().split(u'￥')[-1].strip()
    restaurant_dict['send_price'] = float(send_price) if send_price != u'免配送费' else 0.
    restaurant_dict['href'] = 'http://waimai.meituan.com{0:s}'.format(restaurant.find('a', attrs={'class': 'rest-atag'})['href'])
    restaurant_dict['outof_sale'] = True if restaurant.find('div', attrs={'class': 'outof-sale'}) is not None else False
    discount = restaurant.find('script', attrs={'data-icon': 'i-minus'})
    if discount is not None:
        discount_str_split = discount.get_text().strip().split('<')[0].split(';')[0].strip(u'满元').split(u'元减')
        discount_from = float(discount_str_split[0])
        discount_to = float(discount_str_split[1])
        restaurant_dict['discount_from'] = discount_from
        restaurant_dict['discount_to'] = discount_to
        discount_from = discount_from if discount_from > restaurant_dict['start_price'] else restaurant_dict['start_price']
        discount_from += restaurant_dict['send_price'] if 'send_price' in restaurant_dict else 0
        restaurant_dict['discount_off'] = (discount_from - discount_to) / discount_from
    restaurant_list.append(restaurant_dict)

# 分析优惠

# 1.过滤掉休息中的
restaurant_list = filter(lambda item: item['outof_sale'] is False, restaurant_list)
# 2.过滤掉没有打折的
restaurant_list = filter(lambda item: 'discount_off' in item, restaurant_list)
# 3.按照优惠比例排序
restaurant_list = sorted(restaurant_list, lambda x, y: cmp(x['discount_off'], y['discount_off']), reverse=True)

# 显示
for restaurant in restaurant_list:
    min_order_price = restaurant['discount_from'] if restaurant['discount_from'] > restaurant['start_price'] else restaurant['start_price']
    min_order_price += restaurant['send_price'] if 'send_price' in restaurant else 0
    ori_discount_off = (restaurant['discount_from'] - restaurant['discount_to']) / restaurant['discount_from']
    print '店铺名称：{0:s}\n{1:s}\n{2:s}\n{3:s}\n{4:s}'.format(
        restaurant['restaurant_name'].encode('utf-8'),
        '起送价{0:.0f}元, 配送费{1:.0f}元'.format(restaurant['start_price'], restaurant['send_price']),
        '满{0:.0f}元减{1:.0f}元={2:.1f}折'.format(restaurant['discount_from'], restaurant['discount_to'], ori_discount_off * 10),
        '最低订单{0:.0f}元减{1:.0f}元={2:.1f}折'.format(min_order_price, restaurant['discount_to'], restaurant['discount_off'] * 10),
        '网址: {0:s}'.format(restaurant['href'])
    )
    print

print '按实际可行折扣排序'
