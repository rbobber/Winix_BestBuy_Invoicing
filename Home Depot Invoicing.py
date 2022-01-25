from selenium import webdriver
import time
import csv

driver = webdriver.Chrome()
driver.get("https://apps.commercehub.com/account/login?service=https://dsm.commercehub.com/dsm/shiro-cas")

driver.find_element_by_xpath('//input[@class="sign-in-input"]').send_keys("***")
driver.find_element_by_xpath('//input[@type="password"]').send_keys("*****")
driver.find_element_by_xpath('//input[@class="sign-in-button"]').click()
time.sleep(1)
driver.find_element_by_xpath("//a[contains(@href, '=thehomedepot')]").click()

time.sleep(1)
driver.find_element_by_xpath("//a[contains(text(),'Needs Invoicing')]").click()
time.sleep(1)
invoice_list = []  # empty initialized list of invoice numbers from a BAQ excel csv file
po_num_from_csv = []  # empty initialized list of PO numbers from a BAQ excel csv file

qty_lists = driver.find_elements_by_xpath("//td[contains(@id, 'cell.line.order') and contains(@id, '.invoiceable')]")
qtys = driver.find_elements_by_xpath("//input[contains(@maxlength, '15') and contains(@id, '.invoiced')]")
#print(len(qty_lists))
#print(len(qtys))
for qty, qty_list in zip(qtys, qty_lists):
    qty.send_keys(qty_list.text)

print("invoice test comes next")
with open('sales to date.csv', 'r') as file:
    reader = csv.DictReader(file)
    next(reader)
    print("\n")
    for line in reader:
        invoice_list.append(line['Invoice'])
        po_num_from_csv.append(line['PO'])
po_list = []
po_numbers = driver.find_elements_by_xpath('//a[@class="simple_link"]')
for po_number in po_numbers:
    po_list.append(po_number.text)

count = 0
invoice_boxes = driver.find_elements_by_xpath('//input[@maxlength="50"]')
for invoice_box in invoice_boxes:
    po = po_list[count]
    index = po_num_from_csv.index(po)
    invoice = invoice_list[index]
    if invoice == '':
        print("invoice for po", po, "is blank")
    invoice_box.send_keys(invoice)
    count += 1

# Home Depot Net Days Due and discount days due update, it alternates between 60 and 75
discount_percentages = driver.find_elements_by_xpath('//input[@maxlength="10"]')
for discount_percentage in discount_percentages:
    discount_percentage.send_keys("1")
items = driver.find_elements_by_xpath('//input[@maxlength="5"]')
item_count = 1
for item in items:
    if item_count % 2 == 0:
        item.send_keys("60")
    else:
        item.send_keys("75")
    item_count += 1

qty_list = []
count = 0
i = 0
j = 0
stop_flag = 0
i_value = 6
qty_boxes = driver.find_elements_by_xpath('//input[@maxlength="15"]')
count2 = 0
count3 = 0


