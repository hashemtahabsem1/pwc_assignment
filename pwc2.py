#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import streamlit as st



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

def init_session_state():
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = []

def main():
    st.title("Multiple Choice Quiz App")
    st.write("This app generates a multiple-choice quiz based on a given concept.")
    
    prompt_template = create_the_quiz_prompt_template()
    llm = ChatOpenAI(api_key=openai.api_key)
    chain = create_quiz_chain(prompt_template, llm)
    
    context = st.text_area("Enter the concept for the quiz")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=10, value=3)
    
    init_session_state()

    if st.button("Generate Quiz"):
        quiz_response = chain.run(num_questions=num_questions, quiz_type="multiple-choice", quiz_context=context)
        st.session_state.correct_answers = split_questions_answers(quiz_response)[1].split("\n")
        st.session_state.questions = split_questions_answers(quiz_response)[0]
        st.write("Quiz Generated!")
        st.text(st.session_state.questions)

    user_answers = []
    for i in range(num_questions):
        user_answer = st.radio(f"Select the correct answer for Question {i + 1}", ["a", "b", "c", "d"])
        user_answers.append(user_answer)

    st.write(f"User Answers: {user_answers}")
    

    if st.button("Submit Quiz"):
        correct_answers = [answer.split(".")[1].strip() for answer in st.session_state.correct_answers if answer]
        st.write(f"User Answers: {user_answers}")

    # Calculate and display the score
        score = sum([1 for user, correct in zip(user_answers, correct_answers) if user == correct])
        st.write(f"Your Score: {score}/{num_questions}")

    # Do not display correct answers here
        st.write("Thank you for taking the quiz!")

    # Optionally, you can display the correct answers after submission
        with st.expander("Show Correct Answers", expanded=False):
            st.markdown("\n".join(st.session_state.correct_answers))
    
if __name__ == "__main__":
    main()

