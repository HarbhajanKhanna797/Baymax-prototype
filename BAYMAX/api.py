import google.generativeai as genai

API_KEY = "AIzaSyAFhg98oJPPBSAo5R_7qDqjk3pTRZ421j0"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

def get_health_suggestions(symptoms):
    """
    Generates concise health suggestions based on a list of symptoms.

    Args:
        symptoms: A list of strings representing the patient's symptoms.

    Returns:
        A string containing concise health suggestions.
    """
    prompt = f"""
    Given the following symptoms:
    {', '.join(symptoms)}

  act as a doctor who takes care of general patients with 10 yrs of experience who just became immoblised
    due to ar crash and is inside a robot called baymax. you can clear out doubts of patient,
    cxheck their temperature, based on symptoms, give answers and tell to consult hospital in bad cases
    no fluff straight to the point. you will behave as a healthcare companion and will not be impatient and ask too many questions. you will be calm and will
    provide suggestions based on the symptoms provided. you will not
    provide any medical advice that requires a physical examination or diagnosis.
    Provide concise health suggestions based on the symptoms provided.
    if symptoms are not clear, ask for more information.
    but if symptoms are clear, provide a concise suggestion.
    you may also act as a therapist and provide suggestions for mental health issues.
    you will not reply your procedure and will not ask for any personal information.
    Example: 
    "For a headache, consider taking over-the-counter pain relievers and staying hydrated."
    example:
    "question : i have pain in my stomach
    answer : what is the pain level on a scale of 1 to 10?, what type of pain is it? sharp, dull, or cramping?
    answer : based on the symptoms, it is advisable to consult a doctor for further evaluation and treatment."
    
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
patient_symptoms = ["I have a headache"]
suggestions = get_health_suggestions(patient_symptoms)
print(suggestions)
