# Markov Chain Text Generator

A text generator built from scratch in Python that models word sequences as a Markov chain. It predicts the next word based on the previous 1, 2, or 3 words, and compares how the generated text changes as the amount of context increases.

## How It Works

A Markov chain assumes that the next word depends on a fixed amount of recent history rather than the entire text that came before it. In this project, the state is the last *n* words, where *n* is the order of the model.

The generator:

1. Splits training text into words
2. Builds a mapping from every sequence of *n* consecutive words to the word(s) that followed it in the source text
3. Generates new text by starting with a phrase and repeatedly picking a random "next word" from the possible words stored for that sequence, then moving the window forward

So for an order-2 model, for example, the last two words determine which words can come next.

## Usage

```python
try:
    with open("alice.txt", "r") as f:
        text = f.read()
except:
    print("File couldn't be opened")

order = 3  #Any from 1 to 3 (inclusive)
chain = markov_chain(text, order)
start_word = random.choice(list(chain.keys()))
print(generate_text(chain, start_word, order, length=100))
```

## Results: Comparing Orders 1, 2, and 3

Trained on *Alice's Adventures in Wonderland* by Lewis Carroll (public domain, via Project Gutenberg).

**Order 1:**

fault. So, among them, called out, we shall never get her violently up on the Mock Turtle in with curiosity, and half my tea--not above a good many miles high,' added to him: and beg your pardon!' cried the pool a great crash, as usual. `Come, THAT'S a large saucepan flew close behind it, and round the Mock Turtle, `but it for fear of swimming about it: it pointed to, but when you've no use their slates, and make out of the jury all that,' the way, and the chimney?--Nay, I to get out of his way you go round

**Order 2:**

hand round the court with a lobster as a boon, Was kindly permitted to pocket the spoon: While the Duchess asked, with another hedgehog, which seemed to Alice as he spoke, and the beak-- Pray how did you manage on the trumpet, and called out `The Queen! The Queen!' and the two creatures got so much frightened to say it over) `--yes, that's about the games now.' CHAPTER X The Lobster Quadrille The Mock Turtle to the jury, who instantly made a rush at the top of its mouth open, gazing up into a butterfly, I should think!' (Dinah was the

**Order 3:**

a writing-desk?' `Come, we shall have some fun now!' thought Alice. `I'm glad they don't give birthday presents like that!' But she did not venture to say it out loud. `Thinking again?' the Duchess asked, with another dig of her sharp little chin into Alice's shoulder as she added, `and the moral of that is--"The more there is of mine, the less there is of yours."' `Oh, I know!' exclaimed Alice, who had not attended to this last remark, `it's a vegetable. It doesn't look like one, but it is.' `I quite agree with you,' said the Hatter, and he poured a

## What I Learned

The clearest pattern I noticed across the three orders was that the text generally became more coherent as more context was given to the model.

Order-1 output jumps around quite a lot. The individual words and small phrases are often things that actually occurred in the book, but there isn't much sentence-level logic. For example, `"the chimney?--Nay, I to get out of his way you go round"` is made from locally valid pieces but doesn't really make sense as a sentence.

Order-2 starts producing more readable passages. In this particular run, it ended up around the Mock Turtle's section and reproduced several consecutive lines almost intact.

Order-3 produced a much more coherent passage, including a long exchange between Alice and the Duchess that is very close to the original book. This is the main tradeoff with increasing the order: giving the model more context makes its predictions more specific, but it also gives it fewer possible choices. A 3-word sequence might only appear once in the entire training text, meaning there is only one recorded word that can come after it. At that point, the generator starts looking more like it is following the original text than creating something new.

I also ran into a real bug while making `generate_text`. My first version always turned the newly generated word into a **1-element** tuple (`(next_word,)`) before doing the next lookup, no matter what `order` was. This happened to work for order=1, but broke for order=2 and order=3 because a 1-element tuple can never match a 2- or 3-element dictionary key. Python compares tuples by length and corresponding values, so it doesn't treat `(word,)` as the beginning of a longer tuple.

At first I thought the problem was that my training text wasn't long enough, so I tried using longer and more repetitive texts. The output still stopped after only a few words. Eventually I found that the actual problem was the lookup key being the wrong length.

The fix was to always rebuild the key from the last `order` words:

`tuple(result[-order:])`

I also passed `order` directly into `generate_text` instead of trying to figure it out indirectly. This made the code easier to understand and also made it harder to accidentally use the wrong context size.

It was a useful debugging lesson because the symptom was pretty misleading. The generator producing only a few words made me think I didn't have enough training data, but the actual problem was just that I was constructing the dictionary key incorrectly.

One other thing I found interesting is that the word frequencies basically give you the probability weighting automatically. If `"the"` occurs 50 times after some particular context and `"and"` occurs 5 times, then `"the"` appears 50 times in the list of possible next words while `"and"` appears 5 times. Since `random.choice()` chooses from that list uniformly, `"the"` will be selected roughly 10 times as often as `"and"` over many generations. I don't need to explicitly calculate those probabilities.

## Why I Built This

This project came from the same general interest in randomness and probability that I had with my [Russian Roulette Simulator](link) and [Huffman Coding Compressor](link).

The Russian roulette project was a very simple fixed probability experiment, while Huffman coding uses the frequency of symbols to assign shorter or longer codes. Here, I'm using frequencies to make predictions about what comes next in a sequence.

A Markov chain text generator is a pretty common beginner project, so I wanted to do a little more than just make one that outputs random-looking text. I compared different orders, actually looked at the outputs, and documented a bug that I ran into while making it instead of only showing the output when everything worked.

## Tech Stack

* Python (standard library only — `dict`, `random`)
