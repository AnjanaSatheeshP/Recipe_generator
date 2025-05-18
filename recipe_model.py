from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-recipe-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("flax-community/t5-recipe-generation")

def generate_recipe(ingredients):
    input_text = f"Ingredients: {ingredients}"
    inputs = tokenizer(input_text,return_tensors="pt")
    output = model.generate(**inputs,max_length=250)
    return tokenizer.decode(output[0], skip_special_tokens=True)    