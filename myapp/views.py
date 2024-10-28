from django.shortcuts import render,redirect
from django.views import View
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create your views here.
def daraz(item):
    url=f'https://www.amazon.in/s?k={item}&crid=1ONU435O7Q3BN&sprefix={item}%2Caps%2C230&ref=nb_sb_noss_2'
    res=requests.get(url)
    name_list=[]
    url_list=[]
    price_list=[]
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')
        product_cards = soup.find('div',class_='s-main-slot s-result-list s-search-results sg-row')
        products=product_cards.find_all('div',class_='s-result-item')
        for d in products:
            if d is not None:
                price=d.find('div',class_='puisg-row')
                product_name=d.find('div',class_='a-section a-spacing-none puis-padding-right-small s-title-instructions-style')
                if product_name is not None:
                    product_names=product_name.find('h2')
                    product_url='https://www.amazon.in/'+product_names.a['href']
                    name_list.append(product_names.a.span.text.strip())
                    url_list.append(product_url) 
                if price is not None:
                    p=price.find('span',class_='a-price').span.text.strip()  
                    price_list.append(p) 
    else:
        daraz(item)  
    
    df=pd.DataFrame(
        {
            'product':name_list,
            'price':price_list,
            'link':url_list
        }
    ) 
    data={
            'product':name_list,
            'price':price_list,
            'link':url_list
        }
    return data    
        
    
class Home(View):
    
   def get(self, request, *args, **kwargs):
       data={ 
           'choice':['daraz','amazon'],
       }
       return render(request,'home.html',data)
   
   def post(self, request, *args, **kwargs):
    context = {'search_results': [], 'choice': ['daraz', 'amazon']}  

    try:
        search = request.POST.get('searchval', '')  
        data = daraz(search)

        if data and 'product' in data and 'price' in data and 'link' in data:
            search_results = [
                {'product': product, 'price': price, 'link': link}
                for product, price, link in zip(data['product'], data['price'], data['link'])
            ]
            context['search_results'] = search_results
        else:
            print("No data received from daraz function or missing keys in the response.")

    except Exception as e:
        print(f"Error occurred: {e}")

    return render(request, 'home.html', context)




       
           
       