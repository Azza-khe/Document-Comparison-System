from app.services.extraction.supplier_profiles import SUPPLIERS



def detect_supplier(text):


    header = "\n".join(
        text.split("\n")[:30]
    )


    header = header.upper()



    for name,profile in SUPPLIERS.items():


        for alias in profile["aliases"]:


            if alias in header:


                return {


                    "name":name,

                    "known":True,

                    "profile":profile

                }



    return {


        "name":"UNKNOWN",

        "known":False,

        "profile":None

    }