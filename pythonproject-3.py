import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from babel.numbers import format_currency
import time
from pandas_profiling import ProfileReport
import webbrowser



csvfilee=pd.read_csv(r"C:\Users\Kaiyu\Desktop\dataset.csv")
# print(csvfilee.head())
# print(csvfilee.info())
print(csvfilee.head())
print()
time.sleep(2)
print(csvfilee.tail())
print()
uniquelocation=csvfilee.site_location.unique()
# print(len(lengthlocation))
citylist=np.array(uniquelocation)

citylist=citylist.reshape(24,4)
# print(len(citylist))

# ---------------------------------------------------------------------------------------------------
# price vs square feet graph
# csvfilee['priceinlakhs']=csvfilee['price'] * 100000
time.sleep(4)
x = list(csvfilee['price'])
y = list(csvfilee['total_sqft'])
plt.scatter(x,y)
plt.ylabel("Sqft")
plt.xlabel("Price(in Lakhs)")
plt.title("Price vs Square Feet")
plt.show()


#-------------------------------------------------------------------------------------------------------------
# printing list for user
mx = len(max((sub[0] for sub in citylist),key=len))

for row in citylist:
    print(" ".join(["{:<{mx}}".format(ele,mx=mx) for ele in row]))

#----------------------------------
# to check occureence of all cities
# print(csvfilee['site_location'].value_counts())

#-------------------------------------------------------------------------------------------------------------

#user input
def userinput():
    global siteloc
    siteloc=input("\nenter sitelocation from above list i.e, Alandi Road: ").title()

userinput()

def scattering():
    x = list(reqrows['total_sqft'])
    y = list(reqrows['perfeet'])
    plt.scatter(x,y)
    plt.xlabel("Sqft")
    plt.ylabel("Perfeet")
    plt.title("Square Feet vs Perfeet")
    plt.show()

def siteyes():
    print("yes, your city location founded!")
    time.sleep(2)
    # -------------------------
    # bar graph for bhks
    
    csvfilee['BHK'].value_counts().plot(kind='bar')
    plt.title('number of BHKS')
    plt.xlabel('BHKS')
    plt.ylabel('Count')
    plt.show()
    # -------------------------
    print(f"available bhk's in {siteloc}: ",end=' ')
    reqbhk=csvfilee[['BHK','total_sqft','price','site_location']][csvfilee['site_location']==siteloc]

    uniquebhk=np.array(reqbhk.BHK.unique())
    uniquebhk.sort()
    print(uniquebhk)

    bhk=int(input("enter bhk from the above list: "))
    if bhk not in uniquebhk:
        print("kindly enter valid bhk...")
    else:
        squarefoot=int(input("how many squarefoot area i.e, 1056?: "))

#-------------------------------------------------------------------------------------------------------------
        global reqrows
        global length_bhk
        reqrows2=csvfilee[['BHK','total_sqft','price','site_location','availability']][csvfilee['site_location']==siteloc]
        reqrows=reqrows2[['BHK','total_sqft','price','site_location','availability']][reqrows2['BHK']==bhk]       
        for i in reqrows:
            reqrows['perfeet']=(reqrows['price'] * 100000)/reqrows['total_sqft']
        np.round(reqrows.drop(columns=['price']),3)

        # print(reqrows.describe())
        def prediction(x):
            if(length_bhk==0):
                print("we cannot predict the price because we dont have any data available...")
            elif(length_bhk > 10):
                # removing perfeet outliers
                q1_perfeet=x.perfeet.quantile(0.25)
                q3_perfeet=x.perfeet.quantile(0.75)
                iqr=q3_perfeet-q1_perfeet
                lowerlimit=q1_perfeet-1.5*iqr
                upperlimit=q3_perfeet+1.5*iqr
                drop_perfeet=x[(x.perfeet<lowerlimit)|(x.perfeet>upperlimit)]


                # removing totalsqft outliers
                q1_sqft=x.total_sqft.quantile(0.25)
                q3_sqft=x.total_sqft.quantile(0.75)
                iqr=q3_sqft-q1_sqft
                lowerlimit1=q1_sqft-1.5*iqr
                upperlimit1=q3_sqft+1.5*iqr
                drop_total_sqft=x[(x.total_sqft<lowerlimit1)|(x.total_sqft>upperlimit1)]
                # print(drop_total_sqft)
                # -----------------------------------------------------------------------------------------------------

                nooutlier=x[(x.total_sqft>lowerlimit1)&(x.total_sqft<upperlimit1)][(x.perfeet>lowerlimit)&(x.perfeet<upperlimit)]
                from statistics import mean
                perfeet=np.round(nooutlier.perfeet.mean(),2)
                # print(perfeet)
                predictedprice=int(perfeet*squarefoot)
                
                predictedprice=format_currency(predictedprice,'INR',locale='en_IN')
                print(f"THE PREDICTED PRICE IS: {predictedprice} Rs.")
                
                # ------------------------------------------------------------------------------------------------------------
                # scatter plot``
                # 
                
                
                #-------------------------------------------------------------------------------------------------------------
            else:
                perfeet=x.perfeet.mean()
                # print(np.round(perfeet,2))
                predictedprice=int(perfeet*squarefoot)
                # scattering()
                predictedprice=format_currency(predictedprice,'INR',locale='en_IN')
                print(f"THE PREDICTED PRICE IS: {predictedprice} Rs.")
        
         
        ready_to_move=reqrows[['BHK','total_sqft','price','site_location','availability','perfeet']][reqrows['availability']==1]
        length_bhk=len(ready_to_move['BHK'])
        print("FOR READY TO MOVE")
        prediction(ready_to_move)
        time.sleep(2)
        scattering()
        not_ready_to_move=reqrows[['BHK','total_sqft','price','site_location','availability','perfeet']][reqrows['availability']==0]
        length_bhk=len(not_ready_to_move['BHK'])
        print("FOR NOT-READY TO MOVE")
        prediction(not_ready_to_move)
        





        # ------------------------------------------------------------------------------------------------------------
        
            
if siteloc in citylist:
    siteyes()
    # price vs location of area


else:
    while(1):
        print("either you entered wrong location or the required location is not in list....\n")
        choice=input("want to continue ? press 'y': ").lower()
        if choice == 'y':
            userinput()
        else:
            break

        
# profile=ProfileReport(csvfilee)
# fg=pd.read_html(profile.to_file(output_file="housing.html"))
time.sleep(5)        
webbrowser.open_new_tab('housing2.html')
input("enter any key to exit")