#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import streamlit as st
import re

# Set up OpenAI API key
openai.api_key = "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"

def create_the_quiz_prompt_template():
    """Create the prompt template for the quiz app."""
    
    template = """
You are an expert quiz maker for technical fields. Let's think step by step and
create a quiz with {num_questions} multiple-choice questions about the following concept/content: {quiz_context}.

- Multiple-choice: 
- Questions:
    <Question1>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    <Question2>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    ....
- Answers:
    <Answer1>: <a|b|c|d>
    <Answer2>: <a|b|c|d>
    ....
    Example:
    - Questions:
    - 1. What is the time complexity of a binary search tree?
        a. O(n)
        b. O(log n)
        c. O(n^2)
        d. O(1)
    - Answers: 
        1. b
"""

    prompt = PromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_context="Data Structures in Python Programming")
    
    return prompt


def create_quiz_chain(prompt_template, llm):
    """Creates the chain for the quiz app."""
    return LLMChain(llm=llm, prompt=prompt_template)


def split_questions_answers(quiz_response):
    """Function that splits the questions and answers from the quiz response."""
    questions = quiz_response.split("Answers:")[0]
    answers = quiz_response.split("Answers:")[1]
    return questions, answers


def main():
    st.title("Multiple Choice Quiz App")
    st.write("This app generates a multiple-choice quiz based on a given concept.")
    
    prompt_template = create_the_quiz_prompt_template()
    llm = ChatOpenAI(api_key=openai.api_key)
    chain = create_quiz_chain(prompt_template, llm)
    
    context = st.text_area("Enter the concept for the quiz")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=10, value=3)
    
    if st.button("Generate Quiz"):
        quiz_response = chain.run(num_questions=num_questions, quiz_type="multiple-choice", quiz_context=context)
        st.session_state.answers = split_questions_answers(quiz_response)[1]
        st.session_state.questions = split_questions_answers(quiz_response)[0]
        st.write("Quiz Generated!")
        st.markdown(st.session_state.questions)

    user_answers = []
    for i in range(num_questions):
        user_answer = st.radio(f"Select the correct answer for Question {i + 1}", ["a", "b", "c", "d"])
        user_answers.append(user_answer)

    if st.button("Submit Quiz"):
        correct_answers = st.session_state.answers.split("\n")
        score = sum([1 for user, correct in zip(user_answers, correct_answers) if user == correct])
        st.write(f"Your Score: {score}/{num_questions}")
        st.write("Correct Answers:")
        st.markdown(st.session_state.answers)


if __name__ == "__main__":
    main()

