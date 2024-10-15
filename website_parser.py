# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT

import json
import logging
import re
import time

import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import config
import gpt_config
import prompt
from logging_config import setup_logging
from scholar_parser import GScholarParser, GSEntry


class GenericWebsiteParser:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        chrome_options.add_argument("--headless")
        driver_path = gpt_config.get_driver_path()
        chrome_service = webdriver.ChromeService(executable_path=driver_path)
        self.browser = webdriver.Chrome(
            service=chrome_service, options=chrome_options
        )
        self.browser.implicitly_wait(5)
        self.logger = logging.getLogger(__name__)

    def visit_url_and_parse(self, url):
        """
        This function parse url and return the paper information.

        Parameters:
        url (str): The target url to be parsed.

        Returns:
        dict: A dict contains paper title, authors, venue and abstract.
        """
        if url.endswith(".pdf"):
            return self.parse_pdf(url)

        self.browser.get(url)
        logging.debug("Processing url: " + url)
        html = self.browser.page_source
        txt = self.browser.find_element(By.XPATH, "/html/body").text
        # self.logger.info('extracted text for '+url+': '+txt)

        ans = GenericWebsiteParser.parsing_html_by_gpt(txt)
        return ans

    def parse_pdf(self, url, text_len_limit=10000):
        return None

    @staticmethod
    def parsing_html_by_gpt(html_text, text_len_limit=10000, max_tryout=3):
        openai.api_key = config.openai_api_key
        openai.api_base = config.openai_api_base
        if len(html_text) >= text_len_limit:
            html_text = html_text[0:text_len_limit]

        tryout = 0
        while tryout < max_tryout:
            res = openai.ChatCompletion.create(
                model=gpt_config.html_parse_model,
                messages=prompt.html_parsing_prompt(html_text),
            )
            ans = res["choices"][0]["message"]["content"]
            try:
                jans = json.loads(ans, strict=False)
                print("gpt ans:" + str(jans))
                logging.info("gpt ans: " + str(jans))
                return jans
            except json.decoder.JSONDecodeError as e:
                logging.debug(str(e))
                logging.debug("information extracted failed. ans:" + str(ans))
                logging.debug("input html text:" + str(html_text))
                tryout += 1
        return None

    def parsing_html_by_rule(self, html_text):
        raise NotImplementedError

    @staticmethod
    def read_abstract_by_gpt(abstract: str, my_topic: str, max_tryout=3):
        """
        This function parse the abstract based on the prompt.

        Parameters:
        abstract (str): The target abstract to be parsed.
        my_topic (str): The instruction on how to parse the abstract.

        Returns:
        str: Parsing results.
        """
        tryout = 0
        while tryout < max_tryout:
            logging.info(
                "tryout: "
                + str(tryout)
                + ". Analyzing abstract for "
                + abstract
            )
            openai.api_key = config.openai_api_key
            openai.api_base = config.openai_api_base
            res = openai.ChatCompletion.create(
                model=gpt_config.abstract_parse_model,
                messages=prompt.read_abstract_prompt2(abstract, my_topic),
            )

            ans = res["choices"][0]["message"]["content"]
            try:
                ans = json.loads(ans, strict=False)
                # print('gpt ans for similarity:'+str(ans))
                logging.info("gpt ans for similarity: " + str(ans))
                return ans
            except json.decoder.JSONDecodeError as e:
                logging.debug("output parsing failed for input: " + abstract)
                tryout += 1

        return None


def unit_test():
    setup_logging()
    parser = GenericWebsiteParser()
    parser.visit_url_and_parse("https://arxiv.org/abs/2304.08448")


def unit_test_prompt():
    my_topic = "This paper presents a comprehensive survey of ChatGPT and GPT-4, state-of-the-art large language models (LLM) from the GPT series, and their prospective applications across diverse domains. Indeed, key innovations such as large-scale pre-training that captures knowledge across the entire world wide web, instruction fine-tuning and Reinforcement Learning from Human Feedback (RLHF) have played significant roles in enhancing LLMs' adaptability and performance. We performed an in-depth analysis of 194 relevant papers on arXiv, encompassing trend analysis, word cloud representation, and distribution analysis across various application domains. The findings reveal a significant and increasing interest in ChatGPT/GPT-4 research, predominantly centered on direct natural language processing applications, while also demonstrating considerable potential in areas ranging from education and history to mathematics, medicine, and physics. This study endeavors to furnish insights into ChatGPT's capabilities, potential implications, ethical concerns, and offer direction for future advancements in this field."

    abstract = 'The digitization of healthcare has facilitated the sharing and re-using of medical data but has also raised concerns about confidentiality and privacy. HIPAA (Health Insurance Portability and Accountability Act) mandates removing re-identifying information before the dissemination of medical records. Thus, effective and efficient solutions for de-identifying medical data, especially those in free-text forms, are highly needed. While various computer-assisted de-identification methods, including both rule-based and learning-based, have been developed and used in prior practice, such solutions still lack generalizability or need to be fine-tuned according to different scenarios, significantly imposing restrictions in wider use. The advancement of large language models (LLM), such as ChatGPT and GPT-4, have shown great potential in processing text data in the medical domain with zero-shot in-context learning, especially in the task of privacy protection, as these models can identify confidential information by their powerful named entity recognition (NER) capability. In this work, we developed a novel GPT4-enabled de-identification framework ("DeID-GPT") to automatically identify and remove the identifying information. Compared to existing commonly used medical text data de-identification methods, our developed DeID-GPT showed the highest accuracy and remarkable reliability in masking private information from the unstructured medical text while preserving the original structure and meaning of the text. This study is one of the earliest to utilize ChatGPT and GPT-4 for medical text data processing and de-identification, which provides insights for further research and solution development on the use of LLMs such as ChatGPT/GPT-4 in healthcare. Codes and benchmarking data information are available at this https URL.'

    ans = GenericWebsiteParser.read_abstract_by_gpt(abstract, my_topic)
    print(ans)
    pass


if __name__ == "__main__":
    unit_test_prompt()
