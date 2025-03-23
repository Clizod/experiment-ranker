from string import Template

SYSTEM_PROMPT = "You are a world leading expert veterinary epidemiologist screening abstracts of scientific papers for the systematic literature review of '$topic'"

ELIGIBILITY_QUESTIONS_REFERENCE = {
    'cchf-rainfall': {
        'topic': 'Impact of Climate Change on CCHF: A Focus on Rainfall',
        'questions': [
            { 'q_no': 1, 'q_text': 'Does the study report on primary research or a meta-analysis rather than a review, opinion, or book?' },
            { 'q_no': 2, 'q_text': 'Does the study measure the incidence or prevalence or virulence or survival or transmission of Crimean-Congo haemorrhagic fever or a relevant vector (such as ticks) without specifically measuring the incidence of the pathogens?' },
            { 'q_no': 3, 'q_text': 'Does the research examine environmental factors such as rainfall, seasonality (e.g., wet vs. dry season) or regional comparisons impacting disease prevalence or vector distribution?' },
            { 'q_no': 4, 'q_text': 'Is the study focused on field-based or epidemiological research rather than laboratory method validation?' }
        ]
    },
    'ebola-rainfall': {
        'topic': 'Impact of Climate Change on Ebola: A Focus on Rainfall',
        'questions': [
            { 'q_no': 1, 'q_text': 'Does the study report on primary research or a meta-analysis rather than a review, opinion, or book?' },
            { 'q_no': 2, 'q_text': 'Does the study measure the incidence or prevalence or virulence or survival or transmission of Ebola or Marburg, a relevant vector, or reservoir hosts abundance or distribution (such as bats or primates) without specifically measuring the incidence of the pathogens?' },
            { 'q_no': 3, 'q_text': 'Does the research examine environmental factors such as rainfall, seasonality (e.g., wet vs. dry season) or regional comparisons impacting disease prevalence or vector distribution?' },
            { 'q_no': 4, 'q_text': 'Is the study focused on field-based or epidemiological research rather than laboratory method validation?' }
        ]
    },
    'lepto-rainfall': {
        'topic': 'Impact of Climate Change on Leptospirosis: A Focus on Rainfall',
        'questions': [
            { 'q_no': 1, 'q_text': 'Does the study report on primary research or a meta-analysis rather than a review, opinion, or book?' },
            { 'q_no': 2, 'q_text': 'Does the study measure the incidence or prevalence or virulence or survival or transmission of Leptospirosis, a relevant arthropod vector, or reservoir hosts (such as rodents) without specifically measuring the incidence of the pathogens?' },
            { 'q_no': 3, 'q_text': 'Does the research examine environmental factors such as rainfall, seasonality (e.g., wet vs. dry season) or regional comparisons impacting disease prevalence or vector distribution?' },
            { 'q_no': 4, 'q_text': 'Is the study focused on field-based or epidemiological research rather than laboratory method validation?' }
        ]
    },
    'rvf-rainfall': {
        'topic': 'Impact of Climate Change on Rift Valley Fever Virus: A Focus on Rainfall',
        'questions': [
            { 'q_no': 1, 'q_text': 'Does the study report on primary research or a meta-analysis rather than a review, opinion, or book?' },
            { 'q_no': 2, 'q_text': 'Does the study measure the incidence or prevalence or virulence or survival or transmission of Rift Valley fever or other vector-borne diseases (such as malaria) that share similar vectors (e.g., mosquitoes) without specifically measuring the incidence of the pathogen?' },
            { 'q_no': 3, 'q_text': 'Does the research examine environmental factors such as rainfall, seasonality (e.g., wet vs. dry season) or regional comparisons impacting disease prevalence or vector distribution?' },
            { 'q_no': 4, 'q_text': 'Is the study focused on field-based or epidemiological research rather than laboratory method validation?' }
        ]
    }   
}

CRITERIA_REFERENCE  = {
    'cchf-rainfall': {
        'topic': 'Impact of Climate Change on CCHF: A Focus on Rainfall',
        'inclusion': "Primary research or meta-analysis\n Assesses the relationship between the rainfall and either:\n Crimean-Congo haemorrhagic fever (CCHF) incidence or prevalence\n Pathogen survival\nTransmission\nVirulence\nDemonstrated vector or maintenance host survival, development or distribution",
        'exclusion' : 'Reviews, opinions, books, editorials\n Laboratory-focused studies e.g. studies to develop an appropriate culture method'
    },
    'ebola-rainfall': {
        'topic': 'Impact of Climate Change on Ebola: A Focus on Rainfall',
        'inclusion': "Primary research or meta-analysis\n Assesses the relationship between the rainfall and either:\n Ebola or Marburg incidence or prevalence\n Pathogen survival\nTransmission\nVirulence\nDemonstrated vector or maintenance host survival, development or distribution",
        'exclusion' : 'Reviews, opinions, books, editorials\n Laboratory-focused studies e.g. studies to develop an appropriate culture method'
    },
    'lepto-rainfall': {
        'topic': 'Impact of Climate Change on Leptospirosis: A Focus on Rainfall',
        'inclusion': "Primary research or meta-analysis\n Assesses the relationship between the rainfall and either:\n Leptospirosis incidence or prevalence\n Pathogen survival\nTransmission\nVirulence\nDemonstrated vector or maintenance host survival, development or distribution",
        'exclusion' : 'Reviews, opinions, books, editorials\n Laboratory-focused studies e.g. studies to develop an appropriate culture method'
    },
    'rvf-rainfall': {
        'topic': 'Impact of Climate Change on Rift Valley Fever Virus: A Focus on Rainfall',
        'inclusion': "Primary research or meta-analysis\n Assesses the relationship between the rainfall and either:\n Rift Valley Fever (RVF) virus incidence or prevalence\n Pathogen survival\nTransmission\nVirulence\nDemonstrated vector or maintenance host survival, development or distribution",
        'exclusion' : 'Reviews, opinions, books, editorials\n Laboratory-focused studies e.g. studies to develop an appropriate culture method'
    }   
}


class QAPromptGenerator:
    template_content = ""

    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.template_content = f.read()
    
    def generate(self, key, abstract):
        entries = ELIGIBILITY_QUESTIONS_REFERENCE[key]

        questions = ""
        for q in entries['questions']:  # Loop through the list of questions
            questions += f"Q{q['q_no']}: {q['q_text']}\n"

        data = {
            "topic": ELIGIBILITY_QUESTIONS_REFERENCE[key]['topic'],
            "abstract": abstract,
            "questions": questions
        }

        # Perform token replacement in system prompt template
        sys_prompt = Template(SYSTEM_PROMPT).substitute(data)
        
        # Perform token replacement in user prompt template
        user_prompt = Template(self.template_content).substitute(data)

        return [sys_prompt, user_prompt]

class CriteriaPromptGenerator:
    template_content = ""

    def __init__(self, template_path):
        with open(template_path, 'r') as f:
            self.template_content = f.read()
    
    def generate(self, key, abstract):

        data = {
            "topic": CRITERIA_REFERENCE[key]['topic'],
            "abstract": abstract,
            "inclusion": CRITERIA_REFERENCE[key]['inclusion'],
            "exclusion": CRITERIA_REFERENCE[key]['exclusion'],
        }

        # Perform token replacement in system prompt template
        sys_prompt = Template(SYSTEM_PROMPT).substitute(data)
        
        # Perform token replacement in user prompt template
        user_prompt = Template(self.template_content).substitute(data)

        return [sys_prompt, user_prompt]