import pandas as pd
import re
import os
from Bio import Medline


def handle_uploaded_file(fileIn):
    #print("here")      
    #print(fileIn)
    #print("here")   
    #fr = os.fdopen(f, "r") 
    #print(fr)   
    #print("here") 
    with open(fileIn, "r", encoding="utf-8") as file:
    
        data = []
        records = Medline.parse(file)
        for record in records:
            #print("pmid:", record.get("PMID", "?"))
            #print("title:", record.get("TI", "?"))
            #print("author full name:", record.get("FAU", "?"))
            #print("author short name:", record.get("AU", "?"))
            #print("affiliations:", record.get("AD", "?"))
            #print("source:", record.get("SO", "?"))
            #print("")
            pmid = record.get("PMID", "?")
            title = record.get("TI", "?")
            fauList = record.get("FAU", "?")
            auList = record.get("AU", "?")
            adList = record.get("AD", "?")
            #print("pmid:", pmid)
            #print("title:", title)
            #print("fauList:", fauList)
            #print("auList:", auList)
            #print("adList:", adList)
            #print("")
            #print(len(fauList))
            #print(len(auList))
            #print(len(adList))
            #print("")
            if (len(fauList) == len(auList) == len(adList)):
                for i, j, k in zip(fauList, auList, adList):
                    match = re.search("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", k) 
                    if match:
                        #print(match.group())
                        email = match.group()
                        if email[-1] == ".":
                            email = email[:-1] #to remove . at the end of email
                        #print(email)
                        fauName = i.split(",",1) 
                        name = fauName[1] + " " + fauName[0]  #to display name properly
                        #data.append((pmid, title, name.lstrip(), j, email))
                        data.append((email.lower(), name.lstrip(), title))
        
        
        #cols=['pmid','title', 'FAU', 'AU', 'AD']
        cols=['email','name','title']
        result = pd.DataFrame(data, columns=cols)
        result.drop_duplicates( "email", keep='first', inplace=True)  #to remove duplicate mail ids
        #print(result)   
        outName = fileIn.split(".",1)
        fout = outName[0] + ".csv"
        #print(fout)   
        result.to_csv(fout, encoding='utf-8-sig', index=False)
        
    file.close()        
        
    #input('Press Enter to Continue...')