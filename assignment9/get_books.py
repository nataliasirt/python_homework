import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
        driver.get(url)
        time.sleep(5)
        
        search_results = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
        
        if len(search_results) == 0:
            time.sleep(5)
            search_results = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
            
        print(f"Found {len(search_results)} search results")
        
        results = []
        
        for result in search_results:
            try:
                try:
                    title_element = result.find_element(By.CSS_SELECTOR, "span.title-content")
                    title = title_element.text.strip()
                except:
                    try:
                        title_element = result.find_element(By.CSS_SELECTOR, "a.title-link")
                        title = title_element.text.strip()
                    except:
                        title = "Title not found"
                
                try:
                    author_elements = result.find_elements(By.CSS_SELECTOR, "a.author-link")
                    authors = [author.text.strip() for author in author_elements]
                    author = "; ".join(authors) if authors else "Unknown"
                except:
                    author = "Author not found"
                
                try:
                    format_year_div = result.find_element(By.CSS_SELECTOR, "div.cp-format-info")
                    try:
                        format_year_element = format_year_div.find_element(By.CSS_SELECTOR, "span.cp-format-year")
                        format_year = format_year_element.text.strip()
                    except:
                        format_year = format_year_div.text.strip()
                        
                    if not format_year:
                        spans = format_year_div.find_elements(By.TAG_NAME, "span")
                        if spans:
                            format_year = " ".join([span.text.strip() for span in spans if span.text.strip()])
                except:
                    format_year = "Format-Year not found"
                    
                if not format_year or format_year == "Format-Year not found":
                    try:
                        format_elements = result.find_elements(By.CSS_SELECTOR, "span.cp-format-badge")
                        if format_elements:
                            format_parts = [elem.text.strip() for elem in format_elements if elem.text.strip()]
                            format_year = " ".join(format_parts)
                    except:
                        pass
                
                if format_year and '\n' in format_year:
                    format_year = format_year.split('\n')[0].strip()
                
                book_data = {
                    "Title": title,
                    "Author": author,
                    "Format-Year": format_year
                }
                results.append(book_data)
                
                print(f"Processed book: {title}")
                
            except Exception as e:
                print(f"Error processing a book entry: {str(e)}")
        
        df = pd.DataFrame(results)
        print("\nDataFrame of results:")
        print(df.head())
        
        df.to_csv("get_books.csv", index=False)
        print("\nSaved results to get_books.csv")
        
        with open("get_books.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Saved results to get_books.json")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()