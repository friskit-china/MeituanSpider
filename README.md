## 美团外卖优惠筛选器
---
还在为找不到最优惠的外卖发愁嘛？可以试试这个！

使用Python，需要安装依赖：urllib2、BeautifulSoup

### 使用方法：

1. 如果是MSRA的小伙伴直接请跳转到第6步啦，只要不失效的话应该就不需要导入cookie了，其他人等继续往下看。
2. 使用Chrome浏览器，安装EditThisCookie插件
2. 配置EditThisCookie插件，在左边“选项”栏中设置“选择cookies的导出格式”为JSON
3. 用Chrome浏览器打开美团外卖网站，选择好地址之后，用EditThisCookie导出Cookies（会自动复制到剪贴板）
4. 将剪贴板中复制下来的Cookies完整地替换粘贴到cookie.json文件中
5. 把浏览器地址栏中的地址（如：http://waimai.meituan.com/home/wrr2jycxw236 的格式）替换到MeituanSpider.py文件中上面的url变量上。
6. 运行MeituanSpider.py (python MeituanSpider.py)。

### 结果说明

1. 程序以优惠折扣倒序排列（越靠下优惠越高）。
2. 只考虑最高档的满减优惠（例如有满20减10元和满30减12元，程序只会考虑后者）
3. 尽管有些满减优惠很高，但完成订单有起送价和配送费等限制，所以程序以“最低享受优惠价格”计算折扣


> 只花了半个小时随手写的，请不要吐槽代码乱 

> 不保证能用。如果发生严重意外（例如中午吃不上饭饿肚肚神马的），后果自负

> 只保证上传日（2015年8月16日）之前能用，以后美团要是改版了这程序不好使了我也不一定会更新哈
