import requests as r
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def find_recipes(food):
    food=food.lower()
    page=r.get("https://www.allrecipes.com/search/results/?wt="+food+"&sort=re")
    content=page.content
    soup=bs(content,'html.parser')
    soup.prettify()

    recipes=[]
    temp_recipes = []
    top_recipes=[]
    list_of_links=[]

    section=soup.find('section',id={'fixedGridSection'})
    recipes=section.find_all('a')

    for recipe in recipes:
        link=recipe.get('href')
        list_of_links.append(link)

    for recipe in list_of_links:
        if((recipe not in temp_recipes) and len(recipe)>50 and 'video' not in recipe and food in recipe):
            temp_recipes.append(recipe)
    if(len(temp_recipes)<10):
        length=len(temp_recipes)
        top_recipes=temp_recipes[:length]
    else:
        top_recipes=temp_recipes[:10]

    all_images=[]
    images=[]
    temp_images=[]
    temp_name=[]
    list_of_names=[]

    if(len(temp_recipes)<10):
        for index in range(len(temp_recipes)):
            new_page=r.get(top_recipes[index])
            content=new_page.content
            soup=bs(content,'html.parser')
            soup.prettify()

            section1=soup.find('section',attrs={'class':'ar_recipe_index'})
            if section1 is not None:
                all_images=section1.find_all('img')
                food_image=all_images[0].get('src')
            else:
                all_images=0
            temp_images.append(food_image)

            html = urlopen(top_recipes[index])
            bsh = bs(html.read(), 'html.parser')
            title = bsh.find('h1', {'class' : 'recipe-summary__h1'})

            if title is not None:
                temp_name=list(title)
            else:
                temp_name=[0]
            list_of_names.append(temp_name[0])
            temp_name=[]

        final_list=[]
        for index in range(len(temp_recipes)):
        	if(not(list_of_names[index]==0 or temp_images[index]==0)):
    	        final=(list_of_names[index],top_recipes[index],temp_images[index])
    	        final_list.append(final)
            
    else:
        for index in range(10):
            new_page=r.get(top_recipes[index])
            content=new_page.content
            soup=bs(content,'html.parser')
            soup.prettify()

            section=soup.find('section',attrs={'class':'ar_recipe_index'})
            if section is not None:
                all_images=section.find_all('img')
                food_image=all_images[0].get('src')
            else:
                all_images=0
            temp_images.append(food_image)

            html = urlopen(top_recipes[index])
            bsh = bs(html.read(), 'html.parser')
            title = bsh.find('h1', {'class' : 'recipe-summary__h1'})
            if title is not None:
                temp_name=list(title)
            else:
                temp_name=[0]
            list_of_names.append(temp_name[0])
            temp_name=[]
        
        final_list=[]
        for index in range(10):
            if(not(list_of_names[index]==0 or temp_images[index]==0)):
                final=(list_of_names[index],top_recipes[index],temp_images[index])
                final_list.append(final)

    top_5_recipes=[]
    for index in range(5):
        final=(final_list[index][0],final_list[index][1],final_list[index][2])
        top_5_recipes.append(final)

    print(top_5_recipes)

    













