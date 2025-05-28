import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_owasp_top_10():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://owasp.org/www-project-top-ten/")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '/Top10/A')]")
        ))
        
        xpath_query = "//a[contains(@href, '/Top10/A') and contains(@href, '_2021-')]"
        risk_elements = driver.find_elements(By.XPATH, xpath_query)
        
        risks = []
        for element in risk_elements:
            href = element.get_attribute('href')
            try:
                title = element.find_element(By.TAG_NAME, "strong").text.strip()
            except Exception:
                title = element.text.strip()
            
            if title and href:
                risks.append({"title": title, "href": href})
        
        return sorted(risks, key=lambda risk: _extract_risk_number(risk["title"]))
        
    finally:
        driver.quit()


def _extract_risk_number(title):
    try:
        num_str = title.split(':')[0].replace('A', '')
        return int(num_str)
    except (ValueError, IndexError):
        return 99


def save_to_csv(risks, filename="owasp_top_10.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'href'])
        writer.writeheader()
        writer.writerows(risks)


def main():
    risks = scrape_owasp_top_10()
    
    print("OWASP Top 10 Security Risks:")
    for risk in risks:
        print(f"{risk['title']} - {risk['href']}")
    
    save_to_csv(risks)
    print("\nResultss saved to owasp_top_10.csv")


if __name__ == "__main__":
    main()