!pip install pandas_ta


import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os
import yfinance as yf
import numpy as np
import time
from datetime import timedelta
import pandas_ta as ta
import matplotlib.pyplot as plt


from google.colab import drive
drive.mount('/content/drive')