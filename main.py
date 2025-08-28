import yfinance as yf
import pandas as pd
from tqdm import tqdm
from model import run_analysis
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import datetime
# ========= STEP 1: Define Ticker List (Top 100 from NIFTY 200) =========

tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "LT.NS", "SBIN.NS", "BHARTIARTL.NS",
    "KOTAKBANK.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "AXISBANK.NS",
    "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "WIPRO.NS", "TITAN.NS", "POWERGRID.NS",
    "ULTRACEMCO.NS", "NTPC.NS", "TECHM.NS", "BAJAJFINSV.NS", "NESTLEIND.NS",
    "JSWSTEEL.NS", "ADANIENT.NS", "HDFCLIFE.NS", "INDUSINDBK.NS", "COALINDIA.NS",
    "TATASTEEL.NS", "GRASIM.NS", "ADANIPORTS.NS", "ONGC.NS", "PIDILITIND.NS",
    "BPCL.NS", "DIVISLAB.NS", "DRREDDY.NS", "CIPLA.NS", "BRITANNIA.NS",
    "BAJAJ_AUTO.NS", "HINDALCO.NS", "HEROMOTOCO.NS", "EICHERMOT.NS", "TATAMOTORS.NS",
    "SHREECEM.NS", "DABUR.NS", "ICICIPRULI.NS", "GAIL.NS", "M&M.NS",
    "AMBUJACEM.NS", "SBILIFE.NS", "HAVELLS.NS", "SIEMENS.NS", "COLPAL.NS",
    "UBL.NS", "APOLLOHOSP.NS", "LTIM.NS", "TORNTPHARM.NS", "AUROPHARMA.NS",
    "BERGEPAINT.NS", "IDFCFIRSTB.NS", "BANKBARODA.NS", "VOLTAS.NS", "TVSMOTOR.NS",
    "BEL.NS", "INDIGO.NS", "PAGEIND.NS", "ICICIGI.NS", "PETRONET.NS",
    "SAIL.NS", "SRF.NS", "TATACOMM.NS", "ZYDUSLIFE.NS", "PIIND.NS",
    "NAVINFLUOR.NS", "MUTHOOTFIN.NS", "RECLTD.NS", "LUPIN.NS", "BOSCHLTD.NS",
    "ALKEM.NS", "ACC.NS", "TRENT.NS", "PNB.NS", "VARUNBEVER.NS",
    "GODREJCP.NS", "ASHOKLEY.NS", "CANBK.NS", "IDBI.NS", "BHEL.NS",
    "PFC.NS", "BANKINDIA.NS", "AUBANK.NS", "ABFRL.NS", "LICI.NS",
    "INDHOTEL.NS", "MPHASIS.NS", "L&TFH.NS", "MFSL.NS", "NHPC.NS"
]
# ========== STEP 2: Connect to Google Sheets ==========
print("🔗 Connecting to Google Sheets...")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("NSE Price Table")
worksheet = sheet.sheet1

# ========== STEP 3: Check if today's data already exists ==========
today = datetime.datetime.now().strftime("%Y-%m-%d")

try:
    existing_dates = [row[0] for row in worksheet.get_all_values()[1:]]  # Skip header
except Exception as e:
    existing_dates = []
    print("⚠️ Could not fetch existing dates from Google Sheet:", e)

if today in existing_dates:
    print("✅ Today's data already exists. Skipping upload.")
else:
    print("📥 Downloading 45-day closing prices...")
    closing_data = pd.DataFrame()

    for ticker in tqdm(tickers):
        try:
            df = yf.download(ticker, period="45d", interval="1d", progress=False)
            closing_data[ticker] = df["Close"]
        except Exception as e:
            print(f"❌ Failed for {ticker}: {e}")

    closing_data.index.name = "Date"
    closing_data.dropna(how="all", inplace=True)

    print("📤 Uploading new data to Google Sheets...")
    set_with_dataframe(worksheet, closing_data.reset_index())
    print("✅ Uploaded new data.")

# ========== STEP 4: Read back the entire data from Google Sheets ==========
print("📥 Fetching data from Google Sheets...")
data = worksheet.get_all_records()
df_from_google_sheet = pd.DataFrame(data)
df_from_google_sheet["Date"] = pd.to_datetime(df_from_google_sheet["Date"])

# ========== STEP 5: Run the model ==========
print("🧠 Running prediction model...")
top_predictions = run_analysis(tickers, df_from_google_sheet)

# ========== STEP 6: Output the results ==========
# ========== STEP 6: Output the results ==========
if top_predictions.empty:
    print("⚠️ No profitable prediction found.")
else:
    print("📈 Suggested Stocks to Invest (Next 5 Days):")
    print(top_predictions.to_string(index=False))

    # ========== STEP 7: Write results to Sheet2 ==========
    print("📝 Writing predictions to Sheet2...")

    try:
        worksheet_output = sheet.worksheet("Sheet2")
    except gspread.exceptions.WorksheetNotFound:
        worksheet_output = sheet.add_worksheet(title="Sheet2", rows="100", cols="20")

    set_with_dataframe(worksheet_output, top_predictions.reset_index(drop=True))
    print("✅ Predictions written to Sheet2.")
