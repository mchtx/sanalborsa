from selenium import webdriver
from time import sleep

# Chrome tarayıcı ayarları
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--incognito")  # Gizli modda aç

# WebDriver'ı başlat (doğru parametreyle)
driver = webdriver.Chrome(options=chromeOptions)
driver.maximize_window()
driver.delete_all_cookies()

# TradingView grafik sayfasını aç
driver.get("https://tr.tradingview.com/chart/?symbol=BIST%3AYKBNK")
driver.implicitly_wait(10)

while True:
    fiyat_Bilgisi = driver.find_element("xpath", "/html/body/div[2]/div/div[6]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]").text
    print(fiyat_Bilgisi)
    sleep(3)
