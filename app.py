from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('./dados/dados.csv')