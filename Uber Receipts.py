'''This script is used to download Uber rides PDFs and taking the total amount of each ride'''
'''required to open riders.uber.com by using command 'chrome --remote-debugging-port=9222' and to sign in manually, open first page of trips, set to last 30 days '''


from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


total_amount = 0.0
currRecieptTime = ""
year=2024

startDate = datetime(2024, 8, 23)
endDate = datetime.now()

'''called inside specific trip'''
def downloadReceipt():
    view_receiptbtn = driver.find_element(By.CSS_SELECTOR, "#wrapper > div._css-dqxzrQ > div._css-jjNqJr > div._css-dUXcyn > div > main > div > div._css-ksaRzh > div._css-eiVMjb > div:nth-child(1) > button")
    view_receiptbtn.click()
    downloadPDFbtn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/a")
    downloadPDFbtn.click()

'''trip specific functions
getTripTime()
addSelectedTripValue()
'''

'''check if trip cancelled, if not get trip time and trip value'''
def getTripDetails():
    try:
        return getTripTime(), getTripValue()
    except:
        return ("Cancelled",0.0)


'''get trip time'''
def getTripTime():
    try:
        currRecieptTime= driver.find_element(By.CSS_SELECTOR, "#wrapper > div._css-dqxzrQ > div._css-jjNqJr > div._css-dUXcyn > div > main > div > div._css-ksaRzh > div._css-iGWEKZ > div").text
    except:
        return
    print(currRecieptTime)
    return currRecieptTime


'''add amount to total reciepts downloaded'''
def getTripValue():
    amount = driver.find_element(By.CSS_SELECTOR, "#wrapper > div._css-dqxzrQ > div._css-jjNqJr > div._css-dUXcyn > div > main > div > div._css-ksaRzh > div._css-eFpLwT > div:nth-child(4) > div > p").text
    amount=amount.split(" ")
    amount=amount[1]
    amount=float(amount)
    print(amount)
    return amount

'''Selenium routing to uber page ... this is incomplete currently causing very hard captcha, alternative to add implicit waiing till login manually/attach to session '''
# driver = webdriver.Firefox()

# driver.get("https://riders.uber.com/trips")
# driver.implicitly_wait(1.0)

# '''email input'''
# emailInput = driver.find_element(By.CSS_SELECTOR, "#PHONE_NUMBER_or_EMAIL_ADDRESS")
# emailInput.send_keys(emailInputText)

# submit_button = driver.find_element(By.CSS_SELECTOR, "#forward-button")
# submit_button.click()
# moreOptionsButton = driver.find_element(By.CSS_SELECTOR, "#alt-action-help-v2")

chrome_options = Options()
 

chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


driver = webdriver.Chrome(chrome_options)
# print(driver.title)


''' input date from user'''
# startDate = input("start date dd-mm-yyyy: ")
# endDate = input("end date dd-mm-yyyy:  ... now for current date")

# startDate = startDate.split("-")
# startDate = datetime(day=int(startDate[0]),month=int(startDate[1]),year=int(startDate[2]))

# if endDate == "now":
#     endDate = datetime.now()
# else:
#     endDate = endDate.split("-")
#     endDate= datetime(day=int(endDate[0]),month=int(endDate[1]),year=int(endDate[2]))


''' First element handling '''
'''get reciept date'''
# def firstElement():
#     recDateElem = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/main/div/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div[1]")
#     recDate = recDateElem.text.split(" ")
#     full_date_str = f"{recDate[0]} {recDate[1]} {year}"
#     recDate = datetime.strptime(full_date_str, "%b %d %Y")

#     if(recDate<= endDate and recDate>=startDate):
#         first_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/main/div/div[1]/div[3]/div")
#         first_element.click()
#         '''inside trips'''
#     tripDetails = getTripDetails()
#     downloadReceipt()
#     return tripDetails



''' remaining elements function in whole page'''
def normalElementsInPage():
    tripDetails = []
    
    listElements = driver.find_elements(By.CLASS_NAME, "_css-ggbmUT")
    for i in range(0,len(listElements)):
        listElements = driver.find_elements(By.CLASS_NAME, "_css-ggbmUT")

        element = listElements[i]
        driver.implicitly_wait(9.0)
        # get Date
        recDateElem = element.find_element(By.CLASS_NAME, "_css-eqvdEW")
        recDate = recDateElem.text.split(" ")
        # parse date into readable form
        full_date_str = f"{recDate[0]} {recDate[1]} {year}"
        recDate = datetime.strptime(full_date_str, "%b %d %Y")

        # if date is within set range, go get details else jump record
        if(recDate<= endDate and recDate>=startDate):
            element.click()
        else:
            continue

        '''inside trips'''
        driver.implicitly_wait(5.0)

        # get trip details, if not cancelled download receipt
        tripDtls = getTripDetails()
        if(tripDtls[0]!="Cancelled"):
            downloadReceipt()
            xBtn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/button")
            xBtn.click()
        else:
            print("cancelled file")

        tripDetails.append(tripDtls)
        driver.implicitly_wait(3.0)
        driver.back()

    
    return tripDetails


tripDetailsList = []   
while(True):
    driver.implicitly_wait(3.0)
    tripDetailsList = tripDetailsList + (normalElementsInPage())
    try:
        moreBtn = driver.find_element(By.CSS_SELECTOR, "#wrapper > div._css-dqxzrQ > div._css-jjNqJr > div._css-dUXcyn > div > main > div > div._css-hwEvcr > button")
        moreBtn.click()
    except:
        print("no more files")
        break

for trip in tripDetailsList:
    total_amount+=trip[1]

print(round(total_amount, 2))


'''currently in progress export trip details and amounts to CSV in order to export to inspire portal'''