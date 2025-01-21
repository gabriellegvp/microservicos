from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_products():
    return {"products": ["product1", "product2"]}

@app.post("/products")
def create_product(product: dict):
    return {"message": "Product created successfully", "product": product}