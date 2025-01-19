# Flashcard Trainer

An interactive flashcard web app built with Streamlit to help students improve grammar and vocabulary using spaced repetition.

## Table of contents
* [1. Project Overview]
* [2. Features]
* [3. Environment Variables]
* [4. Technologies Used]


  

## 1. Project Overview <a class="anchor" id="project-description"></a>
The Flashcard Trainer is designed to help students learn from their past grammar and vocabulary mistakes. It automatically generates flashcards from errors and uses spaced repetition to schedule reviews efficiently. Users rate their confidence after each flashcard, influencing how often they see it in the future.
## 2. Features <a class="anchor" id="dataset"></a>
-  Automatic Flashcard Generation – Extracts mistakes and correct answers from student data
- Spaced Repetition Algorithm – Adapts review intervals based on user confidence
- Colorful Flashcards – Engaging UI to enhance the learning experience
- Leaderboard – Tracks student progress and ranking
  

## 3. Environment <a class="anchor" id="environment"></a>

It's highly recommended to use a virtual environment for your projects, there are many ways to do this; we've outlined one such method below. Make sure to regularly update this section. This way, anyone who clones your repository will know exactly what steps to follow to prepare the necessary environment. The instructions provided here should enable a person to clone your repo and quickly get started.

### Create the new evironment 

python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows

### This is how you activate the virtual environment in a terminal and install the project dependencies

```bash
# activate the virtual environment
conda activate <env>
# install the pip package
conda install pip
# install the requirements for this project
pip install -r requirements.txt
```
## 4. Technologies used<a class="anchor" id="mlflow"></a>

- Python – Core programming language
- Streamlit – For building the interactive web app
- Pandas – For handling student mistake data
- NumPy – For data processing and calculations



### What is Streamlit?

[Streamlit](https://www.streamlit.io/)  is a framework that acts as a web server with dynamic visuals, multiple responsive pages, and robust deployment of your models.

In its own words:
> Streamlit ... is the easiest way for data scientists and machine learning engineers to create beautiful, performant apps in only a few hours!  All in pure Python. All for free.

> It’s a simple and powerful app model that lets you build rich UIs incredibly quickly.

[Streamlit](https://www.streamlit.io/)  takes away much of the background work needed in order to get a platform which can deploy your models to clients and end users. Meaning that you get to focus on the important stuff (related to the data), and can largely ignore the rest. This will allow you to become a lot more productive.  

