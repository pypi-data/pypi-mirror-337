from transformers import pipeline

def Practical_12():
    generator = pipeline("text-generation", model="gpt2")
    text = generator("Once upon a time, there was an person name shreeyansh which was a great person ", max_length=50)
    print(text)

# Call practical_12 function
# practical_12()