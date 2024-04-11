# 🎓 StudyLLM - Your Ultimate Study Pal 📚

## 🌟 What's It All About?
-----------------
Tired of skimming through heaps of notes? Let StudyLLM handle that! This app doesn't just chat with your PDF notes, textbooks, and study materials - it also whips up a 10-question practice exam based on them, complete with solutions! Dive in, ask questions about your PDF content, and prep for exams, all in one place. Language model wizardry at its finest! 🪄💬

## 🚀 The Magic Behind the Curtain
------------------

Here's how StudyLLM weaves its magic:

1. **PDF Party**: Upload your PDFs and let the app munch through the content.
2. **Slice 'n' Dice**: Texts are transformed into digestible pieces, ready for action!
3. **Brain Gains**: Our language model gets all brainy, digesting each chunk.
4. **Perfect Match**: Pop a question! StudyLLM hunts for the best match.
5. **Quick Wits**: Receive a snappy, relevant answer from your PDFs.
6. **Test Prep**: Fancy a mock test? Get a 10-question practice exam tailored from your content with solutions. 📝✅

## 🛠 Get Your Study Space Ready!
----------------------------
Eager to dive in? Here's the drill:

1. Clone this repository to kick things off. 🚀
2. Gear up with:
```bash
pip install -r requirements.txt
```

3. Share your secret OpenAI API passphrase in your `.env` file:
```commandline
OPENAI_API_KEY=keep_this_hush_hush
```

#### Or Use Docker if you want!

1. Build the image:
```bash
docker build -t studyllm .
```

2. Run the container:
```bash
docker run -e OPENAI_API_KEY=keep_this_hush_hush -p 8501:8501 studyllm
```


## 🎈 Quiz and Chat Time!

Let's get you started with StudyLLM:

1. Equip yourself with the needed tools and your secret API key.

2. Ignite the fun:
```bash
streamlit run app.py
```

3. 🚀 Your web browser springs to life with StudyLLM all set.

4. Load up your PDF notes, textbooks, or any study material.

5. Ask, learn, and when ready, generate a mock test to challenge yourself!

## 🤓 Share, Learn, But Keep It Here...

Crafted with love for all you learners! This repository, though, is primarily educational. We're not taking any more assignments (aka contributions). However, feel free to customize it for your learning spree!

## 📜 That Legal Bit

StudyLLM is at your service under the **MIT License**. Dive deep, stay inquisitive, and here's to acing those exams! 🎓🚀📚
