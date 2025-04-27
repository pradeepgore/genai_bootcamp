import pandas as pd
from langchain_core.documents import Document

class data_conveter:
    def __init__(self):
        print("data convert has been init...")
        self.product_data=pd.read_csv(r"C:\\genai_bootcamp\\Customer_Support_Agent\\data\\amazon_product_review.csv")
        #print(self.product_data.head())
    
    def data_transformation(self):
        required_columns=self.product_data.columns
        required_columns=list(required_columns[1:])
        #print(required_columns)
        
        product_list = []
        
        for index,row in self.product_data.iterrows():
            
            object={
                "product_name":row['product_title'],
                "product_rating":row['rating'],
                "product_summary":row["summary"],
                "product_review":row["review"]
                
            }
            product_list.append(object)
        #print("********below is my product list************")
        #print(product_list[0])
        docs=[]
        for entry in product_list:
            metadata={"product_name":entry["product_name"],"product_rating":entry["product_rating"],"product_summary":entry["product_summary"]}
            doc=Document(page_content=entry["product_review"],metadata=metadata)
            docs.append(doc)
        #print(docs[0])   
        return docs
            
        
        
    
    
if __name__ == '__main__':
    data_con=data_conveter()
    data_con.data_transformation()
    
    