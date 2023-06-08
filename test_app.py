from unittest import TestCase 
import streamlit as st
import mock

class TestApp(TestCase):
  def test_summarize_resume(self):
      pass 
  def test_answer(self):
      pass
  @mock.patch('profile_bot.ChatOpenAI') 
  def test_summarize_resume_with_jd(self, mock_chatopenai):
      pass

