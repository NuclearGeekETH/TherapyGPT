import gradio as gr
from modules.get_openai_response import chat_response
from modules.utility import form_load, form_save, get_patient_history_text, system_prompt

with gr.Blocks(theme=gr.themes.Soft(), title="TherapyGPT") as demo:
    gr.Markdown(f"<h1 style='text-align: center; display:block'>{'TherapyGPT'}</h1>")
    with gr.Tab("TherapyGPT Chat"):
        with gr.Column("Chat"):
            gr.Markdown(f"<p>{'Chat with your custom therapist'}</p>")

            bot = gr.Chatbot(render=False, type='messages')

            dropdown = gr.Dropdown(
                ["gpt-4o-2024-11-20", "gpt-4.1-2025-04-14"],
                label = "Model",
                value = "gpt-4.1-2025-04-14",
                render = False
            )

            system = gr.Textbox(
                lines = 2,
                label = "System Message",
                value = "",
                render = False
                )

            chat = gr.ChatInterface(
                fn = chat_response,
                chatbot = bot,
                type='messages',
                additional_inputs = [dropdown, system]
            )

            # Function to prep the system prompt text
            def prep_system_message():
                return f"{system_prompt}. Review your patient history and start the session. Patient history:\n\n{get_patient_history_text()}"

            # Fill the system textbox on load
            demo.load(prep_system_message, outputs=system)
 
    with gr.Tab("TherapyGPT Patient Form"):
        with gr.Column("Intake Form"):
            gr.Markdown("### Basic Info")
            full_name = gr.Textbox(label="Full Name")
            preferred_name = gr.Textbox(label="Preferred Name")
            pronouns = gr.Textbox(label="Pronouns")
            date_of_birth = gr.Textbox(label="Date of Birth")
            contact_email = gr.Textbox(label="Email")
            contact_phone = gr.Textbox(label="Phone")
            contact_address = gr.Textbox(label="Address")
            em_name = gr.Textbox(label="Emergency Contact Name")
            em_relationship = gr.Textbox(label="Emergency Contact Relationship")
            em_phone = gr.Textbox(label="Emergency Contact Phone")

            gr.Markdown("### Presenting Issues & Goals")
            presenting_issues = gr.Textbox(lines=3, label="Presenting Issues (one per line)")
            goals = gr.Textbox(lines=3, label="Goals for Therapy (one per line)")

            gr.Markdown("### Mental Health History")
            diagnoses = gr.Dataframe(headers=["Diagnosis","Diagnosed By","Date Diagnosed","Current Status","Notes"], label="Diagnoses",
                                    row_count=(1,"dynamic"), col_count=(5,"fixed"), datatype=["str"]*5)
            symptoms = gr.Dataframe(headers=["Symptom","Onset","Severity","Frequency","Triggers","Coping Strategies"], label="Symptoms",
                                    row_count=(1,"dynamic"), col_count=(6,"fixed"), datatype=["str"]*6)
            mh_meds = gr.Dataframe(headers=["Name","Dosage","Prescriber","Start Date","End Date","Side Effects","Effectiveness"], label="Mental Health Medications",
                                    row_count=(1,"dynamic"), col_count=(7,"fixed"), datatype=["str"]*7)
            past_treatments = gr.Dataframe(headers=["Type","Provider","Duration","Outcome","Reason Stopped"], label="Past Treatments",
                                    row_count=(1,"dynamic"), col_count=(5,"fixed"), datatype=["str"]*5)
            hospitalizations = gr.Dataframe(headers=["Reason","Facility","Date","Duration","Outcome"], label="Hospitalizations",
                                    row_count=(1,"dynamic"), col_count=(5,"fixed"), datatype=["str"]*5)

            gr.Markdown("### Medical History")
            chronic = gr.Textbox(lines=2, label="Chronic Conditions (one per line)")
            current_meds = gr.Dataframe(headers=["Name","Dosage","Condition"], label="Current Medications",
                                    row_count=(1,"dynamic"), col_count=(3,"fixed"), datatype=["str"]*3)
            past_illness = gr.Textbox(lines=2, label="Past Significant Illnesses/Injuries (one per line)")

            gr.Markdown("### Substance Use")
            substance = gr.Dataframe(headers=["Substance","Use Pattern","Duration","Amount","Last Use","Concerns"], label="Substance Use",
                                    row_count=(1,"dynamic"), col_count=(6,"fixed"), datatype=["str"]*6)

            gr.Markdown("### Family History")
            fam_mi = gr.Dataframe(headers=["Relation","Diagnosis","Details"], label="Family Mental Illness", row_count=(1,"dynamic"), col_count=(3,"fixed"), datatype=["str"]*3)
            fam_mc = gr.Dataframe(headers=["Relation","Condition","Details"], label="Family Medical Conditions", row_count=(1,"dynamic"), col_count=(3,"fixed"), datatype=["str"]*3)
            fam_dyn = gr.Dataframe(headers=["Relation","Dynamic","Impact on You"], label="Family Relationship Dynamics", row_count=(1,"dynamic"), col_count=(3,"fixed"), datatype=["str"]*3)

            gr.Markdown("### Trauma History")
            trauma = gr.Dataframe(headers=["Type","Age at Time","Impact","Support Received","Current Effects"], label="Trauma",
                                    row_count=(1,"dynamic"), col_count=(5,"fixed"), datatype=["str"]*5)

            gr.Markdown("### Social History")
            living = gr.Textbox(label="Living Situation")
            relstat = gr.Textbox(label="Relationship Status")
            children = gr.Textbox(label="Children")
            support = gr.Textbox(lines=2, label="Close Support Systems (one per line)")
            work_edu = gr.Dataframe(headers=["Role","Institution","Duration","Satisfaction"], label="Work/Education History",
                                    row_count=(1,"dynamic"), col_count=(4,"fixed"), datatype=["str"]*4)
            legal = gr.Textbox(lines=2, label="Legal Issues (one per line)")

            gr.Markdown("### Strengths and Interests")
            strengths = gr.Dataframe(headers=["Strength/Interest","Notes"], label="Strengths & Interests", row_count=(1,"dynamic"), col_count=(2,"fixed"), datatype=["str"]*2)

            gr.Markdown("### Values and Beliefs")
            values = gr.Textbox(lines=2,label="Values & Beliefs (one per line)")

            gr.Markdown("### Cultural Identity")
            ethnicity = gr.Textbox(label="Ethnicity")
            religion = gr.Textbox(label="Religion")
            gender_identity = gr.Textbox(label="Gender Identity")
            sex_orientation = gr.Textbox(label="Sexual Orientation")
            other_culture = gr.Textbox(label="Other Important Cultural Factors")

            gr.Markdown("### Preferences")
            prefs = gr.Textbox(lines=2, label="Preferred Therapy Styles (one per line)")
            what_helps = gr.Textbox(lines=2, label="What Helps (one per line)")
            what_doesnt = gr.Textbox(lines=2, label="What Doesn't Help (one per line)")
            therapist_gender = gr.Textbox(label="Therapist Preference: Gender")
            therapist_age = gr.Textbox(label="Therapist Preference: Age")
            therapist_culture = gr.Textbox(label="Therapist Preference: Cultural Background")
            therapist_languages = gr.Textbox(label="Therapist Preference: Languages")

            gr.Markdown("### Questions/Concerns for Therapist")
            questions = gr.Textbox(lines=2, label="Questions or Concerns (one per line)")

            gr.Markdown("### Other Notes")
            notes = gr.Textbox(lines=2, label="Other Notes")

            state = gr.State()
            status = gr.Markdown()
            fields = [
                full_name, preferred_name, pronouns, date_of_birth, contact_email, contact_phone, contact_address,
                em_name, em_relationship, em_phone,
                presenting_issues, goals,
                diagnoses, symptoms, mh_meds, past_treatments, hospitalizations,
                chronic, current_meds, past_illness,
                substance,
                fam_mi, fam_mc, fam_dyn,
                trauma,
                living, relstat, children, support, work_edu, legal,
                strengths, values,
                ethnicity, religion, gender_identity, sex_orientation, other_culture,
                prefs, what_helps, what_doesnt, therapist_gender, therapist_age, therapist_culture, therapist_languages,
                questions, notes, state
            ]
            demo.load(form_load, outputs=fields)
            gr.Button("Save Changes").click(form_save, inputs=fields, outputs=status)


if __name__ == "__main__":
    demo.queue()
    # # Toggle this on if you want to share your app, change the username and password
    # demo.launch(server_port=7862, share=True, auth=("nuke", "password"))

    # Toggle this on if you want to only run local
    demo.launch()
