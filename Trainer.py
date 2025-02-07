import streamlit as st
import cv2
import mediapipe as mp
from langchain.llms import Ollama


def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)


def get_diet_plan(gender, age, bmi, height, weight, goal, budget):
    llm = Ollama(model="deepseek-r1:1.5b")
    prompt = (f"Create a diet plan for someone who wants to {goal} weight with a budget of {budget} "
              f"INR per month with their basic detailes are Gender: "
              f"{gender}, Age: {age}, BMI: {bmi}, Height: {height}, Weight: {weight}. "
              f"The plan should have food, meals, nutrients, then calories, a full diet plan for the person. with excersice plans.")
    res = ""
    temp =  llm.invoke(prompt)
    if "</think>" in temp:
        res = temp.split("</think>", 1)[1]
    return res


def count_reps(exercise, landmarks):
    if exercise == "Push-up":
        return landmarks[11].y > landmarks[13].y and landmarks[12].y > landmarks[14].y
    elif exercise == "Pull-up":
        return landmarks[11].y < landmarks[13].y and landmarks[12].y < landmarks[14].y
    elif exercise == "Squat":
        return abs(landmarks[23].y - landmarks[25].y) < 0.05 and abs(landmarks[24].y - landmarks[26].y) < 0.05
    elif exercise == "Bench Press":
        return landmarks[13].y > landmarks[11].y and landmarks[14].y > landmarks[12].y
    return False


st.title("Personalized Fitness Guide")
name = st.text_input("Enter your name")
gender = st.selectbox("Select your gender", ["Male", "Female", "LGBTQ++ Ultra HD"])
age = st.number_input("Enter your age", min_value=1, step=1)
height = st.number_input("Enter your height (cm)", min_value=50, step=1)
weight = st.number_input("Enter your weight (kg)", min_value=10, step=1)
bmi = calculate_bmi(weight, height) if height > 0 else 0
st.write(f"Your BMI: {bmi:.2f}")
if bmi<=16:
    st.write("BRUHHH!!!! GAIN SOME WEIGHT")
elif bmi<=18.5:
    st.write("Underweight")
elif bmi<=25:
    st.write("Healthy")
elif bmi<=30:
    st.write("Overweight")
elif bmi>30:
    st.write("BRUHHH!!!! LOSE SOME WEIGHT")
goal = st.selectbox("What is your goal?", ["Lose weight", "Gain weight"])
budget = st.number_input("Enter your budget in INR", min_value=1000, step=100)

plan = ""

if st.button("Get Diet Plan"):
    plan = get_diet_plan(gender, age, bmi, height, weight, goal, budget)
st.write(plan)

if st.button("Go to Exercise Tracker"):
    st.session_state.page = "exercise"

if "page" in st.session_state and st.session_state.page == "exercise":
    st.title("Exercise Tracker")
    exercise = st.selectbox("Choose an exercise", ["Push-up", "Pull-up", "Squat", "Bench Press"])

    cap = cv2.VideoCapture(0)
    pose = mp.solutions.pose.Pose()
    mpdraw = mp.solutions.drawing_utils
    count = 0
    prev_state = False

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            mpdraw.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            curr_state = count_reps(exercise, landmarks)
            if curr_state and not prev_state:
                count += 1
            prev_state = curr_state

        cv2.putText(img, f"Count: {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Exercise", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
