from transformers import pipeline
import streamlit as st
import requests

class NLPModels:
    def __init__(self):
        self.translation = None
        self.summarization = None
        self.qa_chat = None
        self.hf_api_key = "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"
        self.hf_model_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    @st.cache_resource
    def load_translation(_self):
        return pipeline("translation", model="facebook/nllb-200-distilled-600M")

    @st.cache_resource
    def load_summarization(_self):
        return pipeline("summarization", model="google/pegasus-xsum")

    @st.cache_resource
    def load_qa_chat(_self):
        return pipeline("text2text-generation", model="google/flan-t5-base")

    def translate(self, text, src_lang="eng_Latn", tgt_lang="hin_Deva"):
        if self.translation is None:
            self.translation = self.load_translation()
        result = self.translation(text, src_lang=src_lang, tgt_lang=tgt_lang)
        return result[0]['translation_text'] if result else ""

    def summarize(self, text):
        if self.summarization is None:
            self.summarization = self.load_summarization()
        result = self.summarization(text, max_length=150, min_length=40, do_sample=False)
        return result[0]['summary_text'] if result else ""

    def qa(self, question, context):
        # Use Hugging Face Inference API for Q&A
        prompt = (
            "You are an agricultural expert. Answer the following question in a clear, polite, and helpful way. "
            "If the question is about crop protection, pesticide, or fertilizer, provide specific, safe, and regionally appropriate advice. "
            "If you don't know, say so honestly.\n"
        )
        if context:
            prompt += f"Context: {context}\n"
        prompt += f"Question: {question}\nAnswer:"
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        payload = {"inputs": prompt}
        try:
            response = requests.post(self.hf_model_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
                return data[0]['generated_text'].strip()
            elif isinstance(data, dict) and 'error' in data:
                return f"Hugging Face API error: {data['error']}"
            else:
                return str(data)
        except Exception as e:
            return f"Hugging Face API error: {e}"
