# Markov Chain Text Generator

A text generator built from scratch in Python that models word sequences as a Markov chain — predicting the next word based on the previous 1, 2, or 3 words — and compares how output coherence changes as that context window grows.

## How It Works

A Markov chain assumes the next word in a sequence depends only on a fixed-size "state" of recent words, not the full history. Here, the state is the last *n* words (the "order"). The generator:

1. Splits training text into words
2. Builds a mapping from every sequence of *n* consecutive words to the word(s) that followed it in the source text
3. Generates new text by starting at a given phrase and repeatedly picking a random "next word" from the mapped options, sliding the window forward each time

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

The clearest pattern across all three orders was a steady increase in local coherence. Order-1 output jumps between grammatically loose fragments with little sentence-level logic ("the chimney?--Nay, I to get out of his way you go round"). Order-2 starts forming genuinely readable passages — in this run, it landed almost entirely inside the Mock Turtle's lobster poem, reproducing several consecutive lines nearly intact. Order-3 produced a long, grammatically complete exchange between Alice and the Duchess that reads almost indistinguishably from the original book. This is the core tradeoff of increasing order: more context per key means fewer, more specific continuations are available, so output becomes more coherent but also drifts from "generating new text" toward "reciting the source" — a 3-word key is often unique enough in the training text to have only one recorded continuation.

I also ran into a real bug while building this. My first version of `generate_text` always converted the newly generated word into a **1-element** tuple (`(next_word,)`) before the next lookup, regardless of what `order` I was using. This worked by coincidence for order=1, but silently broke for order=2 and order=3, since a 1-element tuple can never equal a 2- or 3-element dictionary key — Python tuple equality requires exact length and content matches, not partial overlap. I initially assumed the problem was my training text being too short and tried swapping in longer, more repetitive texts, but the output stayed stuck at just a few words regardless. The actual fix was to always reconstruct the key from the last `order` words generated so far — `tuple(result[-order:])` — and pass `order` explicitly into `generate_text` rather than trying to infer it, which made the logic easier to follow and less error-prone. It was a useful reminder that a symptom (short output) can have a completely different root cause (a type/length mismatch) than the one it first suggests (not enough data).

A smaller but interesting detail: word frequency in the training text naturally becomes probability weighting for free. If a word is followed by "the" 50 times and by "and" 5 times in the source text, "the" appears 50 times in that word's list of possible next-words, so `random.choice()` picks it roughly 10x more often — without any explicit probability calculation needed.

## Why I Built This

Part of a broader interest in how randomness and probability can be modeled computationally — alongside a [Russian Roulette Simulator](link) (probability as a fixed-odds game mechanic) and a [Huffman Coding Compressor](link) (probability as symbol-frequency weighting). This project explores probability applied to sequence prediction.

A Markov chain text generator is a fairly common beginner project, so what I focused on here was going past a basic working version — extending it to compare multiple orders side by side, documenting the actual results (including a run where output was legitimately shorter than expected, rather than only showing the cleanest examples), and tracking down a real bug in my own logic along the way (see "What I Learned" above).

## Tech Stack

- Python (standard library only — `dict`, `random`)
