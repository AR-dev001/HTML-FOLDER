import pandas as pd
mydataset = {
    'cars':["BMW","Ford","Lamborghini"],
    'passings':[3,7,2]
}
myvar=pd.DataFrame(mydataset)
print(myvar)
myvar2=pd.Series(mydataset,index=["x","y","z"])
print(myvar2)
data = {
    'calories':[420,380,390],
    'duration':[50,40,45]
}
df=pd.DataFrame(data,index=["day1","day2","day3"])
print(df)
print(df.loc["day1"])