from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import CamembertForMaskedLM, CamembertTokenizer, BertForMaskedLM, BertTokenizer
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from nltk.tokenize import sent_tokenize
