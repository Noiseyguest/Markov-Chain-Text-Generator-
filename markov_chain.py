import random

def markov_chain(text,order):
    words = text.split() #converts words into items in a list
    chain = {}  #dictionary data type

    for i in range(len(words) - order):
        current_word = tuple(words[i:i+order]) #uses one or more subsequent words as key field depending on the order
        next_word = words[i+order] #appends the next subsequent word as an element of the key field
        if current_word not in chain:
            chain[current_word] = [] #inserts as keyfield
        chain[current_word].append(next_word) #adds values to keyfield 
    
    return chain

def generate_text(chain, start_word, order, length=100):
    current_word = tuple(start_word) #All key fields are tuples
    result = list(current_word) #easy way of forming the overall words by appending them to a list first and then converting them into a string later

    for x in range(length-1):
        if current_word not in chain: #breaks the text generation if new tuple no longer matches with tuples which are key fields
            break   
        next_word = random.choice(chain[current_word]) #randomly chooses one of many words associated with that particular key field tuple
        result.append(next_word)
        current_word = tuple(result[-order:]) #elements of the tuple should be equal to elements of the tuple which are key fields
    
    return ' '.join(result) #Converts elements of list into a string    

try:
    with open("alice.txt","r") as f:
        text = f.read()
except:
    print("File couldn't be opened")
order = 3 #Any from 1 to 3 (inclusive)
chain = markov_chain(text,order)
start_word = random.choice(list(chain.keys()))
print(generate_text(chain, start_word, order, length=100))


        



