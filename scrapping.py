from turtle import title
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

aws_rds_endpoint = 'fintech-dev.cbnt8xhvtzh0.ap-southeast-1.rds.amazonaws.com'
username = 'admin'
password = 'CknvMh74qeFv'
aws_rds_uri = f'mysql+pymysql://{username}:{password}@{aws_rds_endpoint}:3306/fintech_dev'
db=create_engine(aws_rds_uri)
conn=db.connect()

def get_merchant_title(soup):

    try:
        title=soup.find_all("h1",attrs={"class":"merchant-title"})
        titles=[t.text.strip() for t in title]
    except AttributeError:
        titles=[]
    return titles

def get_offer_title(soup):

    try:
        offer_ttile=soup.find_all("div",attrs={"class":"offer-title"})
        offer_ttile_string=[t.text.strip() for t in offer_ttile]
    except AttributeError:
        offer_ttile_string=[]
    return offer_ttile_string

def get_verification(soup):

    try:
        verify=soup.find_all("div",attrs={"class":"verified-tag cd_exclusive"})
        verify_string=[t.text.strip() for t in verify]
    except AttributeError:
        verify_string=[]
    return verify_string
def get_description(soup):

    try:
        desc=soup.find_all("div",attrs={"data-offer-key":"offerTitle"})
        desc_string=[t.text.strip() for t in desc]
    except AttributeError:
        desc_string=[]
    return desc_string

def get_coupon_code(soup):

    try:
        code=soup.find_all("div",attrs={"class":"p1-code"})
        print(code)
        code_string=[t.string.strip() for t in code]
    except AttributeError:
        code_string= []
    return code_string
def get_stores(soup):

    try:
        store=soup.find_all("div",attrs={"class":"store-name"})
        store_string=[t.string.strip() for t in store]
    except AttributeError:
        store_string= []
    return store_string

def get_title_logo(soup):

    try:
        image=soup.find_all("div",attrs={"class":"tile-logo"})
        images=[x.find('img')['data-lazy-src'] for x in image]
    except AttributeError:
        images=[]
    return images

def get_element_list(i, array):
    if len(array) > 0:
        if i < len(array):
            return array[i]
        else:
            return array[-1]
    else:
        return None

if __name__=="__main__":
    URL='https://www.coupondunia.in'
    HEADERS=({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.5'})
    webpage=requests.get(URL,headers=HEADERS)
    soup=BeautifulSoup(webpage.content,'html.parser')
    links=soup.find_all("a")
    links_list=[]
    for link in links:
        links_list.append(link.get('href'))
        
    

    link_=[x for x in links_list if x is not None and "https" not in x and "#" not in x and x!="/" and "//" not in x]
    # print(link_)

    data=[]
    unique_coupon_code=set()
    
    for link in link_:
        new_webpage=requests.get("https://www.coupondunia.in"+link,headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        print("https://www.coupondunia.in"+link)
        merchant_title = get_merchant_title(new_soup)
        if len(merchant_title)>0:
            offer_titles = get_offer_title(new_soup)
            description = get_description(new_soup)
            coupon_codes = get_coupon_code(new_soup)
            verifications = get_verification(new_soup)
            store=get_stores(new_soup)
            print(verifications)
            title_logos =get_title_logo(new_soup)
            for i, offer in enumerate(offer_titles):
                    if merchant_title != "":
                        d = {}
                        d["merchant_title"] = merchant_title
                        d["offer_title"] = offer
                        d["description"] = get_element_list(i, description)
                        d["coupon_code"] =get_element_list(i,coupon_codes)
                        d["verified"] = get_element_list(i, verifications)
                        d["region"] = "India"
                        d['title_logo'] = get_element_list(i,title_logos)
                        d['store']=get_element_list(i,store)
                    
                    data.append(d)
                    print(d)

                
    datas = [
        {"merchant_title":"Samsung Coupons And Discount Codes","offer_title":"Great 9.9 Sale – Upto 55% + Extra $399 Off On Mobiles, Home Appliances, Computers & More","description":"Now Checkout The Great 9.9 Sale & Avail Upto 55% + Extra $399 Off On Mobiles, Home Appliances, Computers, Tvs, Projectors & More At Samsung. Users Can Also Get 9x Samsung Rewards, 0% Installment Plans, Official Samsung Warranty, Gifts With Purchase & More. Apply The Given Coupon Code At Checkout To Avail The Discount. Visit The Link To Grab This Deal.Validity: 15/September/2023.","coupon_code":"MEGA399","verified":"verified","region":"Singapore","title_logo":"https://www.couponzguru.sg/wp-content/uploads/2022/06/samsung-coupon-codes-222.jpg","store":"Samsung"},
        {"merchant_title":"Samsung Coupons And Discount Codes","offer_title":"Limited Time Offer – Upto 45% Off On Mobile, Home Appliances, Watches & More + Free Delivery","description":"Now Checkout The Limited Time Offer & Avail Upto 45% Off On Mobile, Home Appliances, Watches, Buds, Tvs, Soundbars, Computers  & More At Samsung. Users Can Also Get Free Delivery, 0% Installments Upto 36 Months, Samsung Official Warranty & More.Validity: Limited Period.","coupon_code":"","verified":"verified","region":"Singapore","title_logo":"https://www.couponzguru.sg/wp-content/uploads/2022/06/samsung-coupon-codes-222.jpg","store":"Samsung"},
        {"merchant_title":"Emirates Coupons And Discount Codes ","offer_title":"Student Offer – Upto 10% Off On Economy Class & Business Class Fares","description":"Now Avail Upto 10% Off On Economy Class & Business Class Fares. Explore 80+ Destinations & Get Benefits Like Date Change, Extra Baggage Allowance Etc. Click On The Link  For More Details.Validity: Limited Period.","coupon_code":"STUDENT","verified":"verified","region":"Singapore","title_logo":"https://www.couponzguru.sg/wp-content/uploads/2017/04/emirates-coupon-codes.jpg","store":"Emirates"},
        {"merchant_title":"Asus Coupons And Discount Codes","offer_title":"Asus Tech Show – Upto $2,500 Off On Laptops + Extra Upto $60 Grab Pay Cash Off","description":"Now Checkout The Asus Tech Show & Avail Upto $2,500 Off On Asus Laptops + Free Delivery. Users Can Also Get Upto $60 Grab Pay Cash Off + Extra Cashback On Shopback, 0% Interest Installments & More. Minimum Spend Of $2000 Is Required To Avail Extra $60 Off. Shop From Laptops Like Asus Vivobook G0 14, Asus Tif Gaming, Zenbook 14 Oled & More. Apply The Given Coupon Code At Checkout To Avail The Discount. Visit The Link To Grab This Deal.Validity: 10/September/2023.","coupon_code":"ASUSXGRAB60","verified":"verified","region":"Singapore","title_logo":"https://www.couponzguru.sg/wp-content/uploads/2023/07/Asus-Storelogo-new.jpg","store":"ASUS"},


    ]
    coupons_df=pd.DataFrame.from_dict(data)
    coupons_df=pd.concat([coupons_df,pd.DataFrame(datas)],ignore_index=True)
    coupons_df['type_of_voucher']=coupons_df['coupon_code'].apply(lambda x: "Deals" if pd.isnull(x) else "Coupons")
    coupons_df['merchant_title']=coupons_df['merchant_title'].apply(lambda x:"Others" if x==[] else x)
    duplicates = coupons_df[coupons_df.duplicated(subset='coupon_code', keep=False)]
    
    print("Duplicate Coupon Codes:")
    print(duplicates[['merchant_title', 'offer_title', 'coupon_code']])

    print(coupons_df)

    
    coupons_df.to_sql("Coupons_ind",conn,if_exists='replace')

    
