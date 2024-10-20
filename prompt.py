def gs_query_prompt(description, words=0):
    info_sys = {
        "role": "system",
        "content": "You are a research assistant, I want to you read a paper description and I will ask you a question.",
    }
    if words == 0:
        info_user = {
            "role": "user",
            "content": "This is my paper's description: ["
            + description
            + "] I want to search for paper that similar to my paper. What should be my query in google scholar? Can you suggest a single query with the format <your suggested query>?",
        }
    else:
        info_user = {
            "role": "user",
            "content": "This is my paper's description: ["
            + description
            + "] I want to search for paper that similar to my paper. What should be my query in google scholar? Can you suggest a single query with the format <your suggested query>? Make sure the query has less than "
            + str(words)
            + " words.",
        }
    return [info_sys, info_user]


def html_parsing_prompt(html_text):
    info_sys = {
        "role": "system",
        "content": "You are a document parser, I want to you extract information in a text document",
    }
    info_user = {
        "role": "user",
        "content": "This is a text document extracted from a webpage: ["
        + html_text
        + "] can you extract paper title, paper author, publication venue, abstract and link to pdf (if available) from the document? Please return the answer in a json format, the keys in json are <title>, <authors>, <venue>, <abstract>. Please make sure to extract the full abstract withou using '...'.",
    }
    return [info_sys, info_user]


def read_abstract_prompt(abstract, my_topic):
    info_sys = {
        "role": "system",
        "content": "You are an academic researcher's assistant, I want to you read a paper and tell me whether it is relevant to my idea or not.",
    }

    info_user = {
        "role": "user",
        "content": "Here is the abstract of a paper: ["
        + abstract
        + "]. Here is the description of my paper:["
        + my_topic
        + "].  Please read them and answer my question: [Q1: What are the similarities between this paper and my idea? Q2: What are the difference between the paper and my idea? Q3: Please provide a similarity score from 1 to 5, where a higher score indicates greater relevance between two research papers. Use the following calibration for the scores: 1 - Not relevant: Papers from different fields with no shared methodologies or insights, e.g., one paper on natural language processing and the other on computer graphics. 2 - Somewhat relevant: Papers from the same subfield, such as adversarial learning, neural rendering, or tangible input interfaces. 3 - Relevant: Papers addressing similar problems (e.g., increasing the robustness of adversarial learning, tangible input interfaces in AR), or using similar methodologies to solve different problems. Papers with this level of similarity should be considered for citation. 4 - Very relevant: Papers addressing similar problems and using similar techniques. 5 - Mostly relevant: Papers addressing almost identical problems and using similar techniques.] Please provide your answer in .json format, the keys are <Similarity>, <Difference>, <Score>",
    }
    return [info_sys, info_user]


def read_abstract_prompt2(abstract, my_topic):
    info_sys = {
        "role": "system",
        "content": "You are an academic researcher's assistant, I want to you read a paper and tell me how it is relevant to my idea.",
    }

    info_user = {
        "role": "user",
        "content": f"""####Begin Questions####
        Q1: Write a one-sentence summary of the input paper.
        Q2: What are the similarities between this paper and my idea?
        Q3: What are the differences between the paper and my idea?
        Q4: Please provide a similarity score from 0 to 100, where a higher score indicates greater relevance between two research papers. Use the following calibration for the scores:
        0-20: Not relevant; Papers from different fields with no shared methodologies or insights, e.g., one paper on natural language processing and the other on computer graphics.
        20-40: Somewhat relevant; Papers from the same subfield, such as adversarial learning, neural rendering, or tangible input interfaces.
        40-60: Relevant; Papers addressing similar problems (e.g., increasing the robustness of adversarial learning, tangible input interfaces in AR), or using similar methodologies to solve different problems. Papers with this level of similarity should be considered for citation.
        60-80: Very relevant; Papers addressing similar problems and using similar techniques.
        80-100: Mostly relevant; Papers addressing almost identical problems and using similar techniques.
        Make sure the score is a number between 0 and 100 e.g., 81, 23, 45, 90, 98...
        Q5: Please briefly state the reason for your score.
        ####End Questions####
        ####Begin Instructions####
        Please provide your answer in .json format. The keys are <Summary>, <Similarity>, <Difference>, <Score>, <Reason>.
        <Summary> is a one-sentence summary of the input paper (Q1).
        <Similarity> is the similarities between this paper and my idea (Q2).
        <Difference> is the differences between the paper and my idea (Q3).
        <Score> is the similarity score (Q4).
        <Reason> is the reason for your score (Q5).
        ####End Instructions####
        ####Begin Input####
        This is the information of a paper I found: [{abstract}].
        This is the description of my idea: [{my_topic}].
        ####End Input####
        """,
    }
    return [info_sys, info_user]


def pdf_section_extraction_prompt(pdf_text):
    info_sys = {
        "role": "system",
        "content": "You are a PDF parser, I want you to extract particular sections bases on my instructions.",
    }

    info_user = {
        "role": "user",
        "content": "Here is the part text extracted from the pdf: ["
        + pdf_text
        + "]. I want you to parse me the Introduction section and Related work section. Please return your answer in .json format, with keys <Introduction> and <Related Work>. If either Introduction or Related work is not found, return empty string in corresponding json field. If found, extract full paragraph in both section. Do not use ... as I need the full paragraph for both introduction and related work.",
    }
    return [info_sys, info_user]
