import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import csv

baseUrl = "http://121.52.152.24/"
csvfile = open('class_data_result.csv', 'a+', encoding='utf-8', newline='')


def get_the_result(ag_list):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(baseUrl)

    for ag in ag_list:
        st_result = list()
        # Search Input value is set to ag #
        driver.find_element(By.ID, "ctl00_Main_txtReg").send_keys(ag)

        # Click the Access Student Information Buttton
        ActionChains(driver).click(driver.find_element(
            By.ID, "ctl00_Main_btnShow")).perform()

        # Click Result Information Tab Button
        ActionChains(driver).click(driver.find_element(
            By.ID, "__tab_ctl00_Main_TabContainer1_tbResultInformation")).perform()

        try:
            # Search for spring2022 results
            spring22_results = driver.find_elements_by_xpath(
                '//*[text() = "spring22"]')
            for r in driver.find_elements_by_xpath('//*[text() = "Spring22"]'):
                spring22_results.append(r)
        except:
            print('The Student with ag '+ag+' don\'t given paper')
            continue
        for result in spring22_results:
            parent_result_tr = result.find_element(By.XPATH, "..")
            total_mark = parent_result_tr.find_elements(By.TAG_NAME, 'td')[
                12].text
            st_result.append(float(total_mark))

        gpa_calulator(st_result, ag)
        driver.get(baseUrl)
    driver.close()


def generate_ags(start, end, prefix, suffix):
    ag_list = list()
    for i in range(start, end+1):
        ag_list.append(prefix + str(i) + suffix)
    return ag_list


def gpa_calulator(st_result, ag):
    total_credit_hrs = 0
    total_qp = 0
    threeCreditSet = [[24, 3],
                      [25, 3.5], [26, 4], [27, 4.5], [28, 5], [29, 5.5], [30, 6], [31, 6.33], [32,
                                                                                               6.67],
                      [33, 7], [34, 7.33], [35, 7.67], [36, 8],
                      [37, 8.33], [38, 8.67], [39, 9], [40, 9.33], [41, 9.67], [42, 10], [43,
                                                                                          10.33],
                      [44, 10.67], [45, 11], [46, 11.33], [47, 11.67],
                      [48, 12]
                      ]

    for marks in st_result:
        if marks < 24:
            total_qp += 0
        elif marks >= 24 and marks < 48:
            for mark in threeCreditSet:
                if mark[0] == marks:
                    total_qp += mark[1]
                    continue
        elif marks >= 48:
            total_qp += 12
    try:
        gpa = total_qp / (3 * len(st_result))
    except:
        print("Can't Divide By Zero ("+ag+")")
        return

    csvwriter = csv.writer(csvfile)
    row = [ag, gpa]
    csvwriter.writerow(row)
    print("=====================================================================\n")
    print("GPA of "+ag+" is " + str(gpa) + " and total qp are " +
          str(total_qp) + " and credit hrs are " + str(3 * len(st_result)))
    print("\n=====================================================================")


if __name__ == "__main__":
    ag_list = generate_ags(51, 91, "2019-ag-60", "")
    get_the_result(ag_list)
