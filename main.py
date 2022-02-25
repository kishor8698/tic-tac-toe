# from selenium import webdriver
from selenium import webdriver
import time
search_item=input('Enter your search Term:')

driver=webdriver.Chrome()
driver.get("https://www.flipkart.com/")
driver.maximize_window()

try:
    driver.find_element_by_xpath('//button[@class="_2KpZ6l _2doB4z"]').click()
except:
    pass

driver.find_element_by_xpath('//input[@name="q"]').send_keys(search_item)
driver.find_element_by_xpath('//button[@class="L0Z3Pu"]').click()

time.sleep(3)
pcontainer=driver.find_element_by_xpath('//div[@class="_1YokD2 _2GoDe3"]')
all_container=pcontainer.find_elements_by_xpath('//div[@class="_1YokD2 _3Mn1Gg"]')
print(len(all_container),'length')

all_produts=all_container.find_elements_by_xpath('//div[@class="_13oc-S"]')
print(all_produts)

# for product in all_produts:
#     product.click()
#     driver.switch_to.window(driver.window_handles[1])
#     title=driver.find_element_by_xpath('//span[@class="B_NuCI"]').text
#     price=driver.find_element_by_xpath('//div[@class="_30jeq3 _16Jk6d"]').text
#     print(title)
#     try:
#         mrp=driver.find_element_by_xpath('//div[@class="_3I9_wc _2p6lqe"]').text
#         discount=driver.find_element_by_xpath('//div[@class="_3Ay6Sb _31Dcoz"]').text
#     except:
#         pass
#     seller_name=driver.find_element_by_id('sellerName').text
#     print(f"Title-{title}")
#     print(f"Price-{price}")
#     try:
#         print(f"MRP-{mrp}")
#         print(f"discount-{discount}")
#     except:
#         driver.switch_to.window(driver.window_handles[0])
    
# driver.quit()
        
        