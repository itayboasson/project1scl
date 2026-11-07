
import streamlit as st
import pandas as pd

# הגדרות האתר
st.set_page_config(page_title="פרויקט חיזוי מחירי בתים", page_icon="🏠", layout="wide")

# טעינת הנתונים
# יש לשנות את housing.csv לשם קובץ ה-CSV שלכם
df = pd.read_csv("House Price Prediction Dataset.csv")

# עיצוב בסיסי
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 פרויקט חיזוי מחירי בתים")
st.write("באתר זה נציג את הנתונים שבהם נשתמש בפרויקט ואת המטרה שלנו — חיזוי מחירי בתים.")

st.divider()

# חלק 1: הסבר על הדאטה
st.header("1. הסבר על הדאטה")

st.write("""
הדאטה שנבחר עוסק בבתים ובמאפיינים השונים שלהם, במטרה לבדוק אילו גורמים
עשויים להשפיע על מחיר הבית.

כל שורה בטבלה מייצגת בית אחד, וכל עמודה מתארת מאפיין אחר של אותו בית,
כמו שטח הבית, מספר חדרי השינה, מספר חדרי האמבטיה, שנת הבנייה ומחיר הבית.
""")

st.subheader("העמודות בדאטה")

column_descriptions = {
    "Id": "מספר מזהה ייחודי של הבית.",
    "Area": "שטח הבית.",
    "Bedrooms": "מספר חדרי השינה בבית.",
    "Bathrooms": "מספר חדרי האמבטיה בבית.",
    "Floors": "מספר הקומות בבית.",
    "YearBuilt": "השנה שבה הבית נבנה.",
    "Location": "המיקום של הבית.",
    "Condition": "מצבו של הבית.",
    "Garage": "מידע על קיום או סוג של חניה/מוסך.",
    "Price": "מחיר הבית."
}

description_df = pd.DataFrame(
    [(col, column_descriptions.get(col, "מאפיין של הבית.")) for col in df.columns],
    columns=["שם העמודה", "מה היא מייצגת"]
)

st.table(description_df)

st.divider()

# חלק 2: מידע על הנתונים
st.header("2. מידע על הנתונים")

col1, col2 = st.columns(2)

with col1:
    st.metric("מספר שורות", f"{df.shape[0]:,}")

with col2:
    st.metric("מספר עמודות", f"{df.shape[1]}")

st.subheader("ערכים חסרים")

missing_values = df.isnull().sum().reset_index()
missing_values.columns = ["עמודה", "מספר ערכים חסרים"]
st.dataframe(missing_values, use_container_width=True, hide_index=True)

total_missing = df.isnull().sum().sum()
if total_missing == 0:
    st.success("לא נמצאו ערכים חסרים בדאטה.")
else:
    st.warning(f"נמצאו בסך הכול {total_missing} ערכים חסרים בדאטה.")

st.subheader("ממוצעי העמודות המספריות")

# לא מציגים ממוצע של Id, כי מדובר במספר מזהה ולא במאפיין כמותי של הבית
numeric_columns = df.select_dtypes(include="number").columns.tolist()
numeric_columns = [col for col in numeric_columns if col != "Id"]

means = df[numeric_columns].mean().round(2).reset_index()
means.columns = ["עמודה", "ממוצע"]
st.dataframe(means, use_container_width=True, hide_index=True)

st.divider()

# חלק 3: מה נרצה לחזות?
st.header("3. מה נרצה לחזות?")

st.write("""
בפרויקט נרצה לחזות את **מחיר הבית (Price)**.

בחרנו במחיר כמשתנה Y, משום שזו התוצאה שאותה אנחנו מעוניינים לחזות
בהתבסס על המאפיינים השונים של הבית.
""")

st.subheader("באילו עמודות נשתמש לחיזוי?")

st.write("בחרנו בשלוש עמודות שישמשו כמשתני X:")

features = [
    {
        "name": "Area – שטח הבית",
        "reason": "ככל ששטח הבית גדול יותר, בדרך כלל יש בו יותר מקום ולכן מחירו עשוי להיות גבוה יותר."
    },
    {
        "name": "Bedrooms – מספר חדרי השינה",
        "reason": "מספר גדול יותר של חדרי שינה עשוי להפוך את הבית למתאים למשפחות גדולות יותר ולהשפיע על מחירו."
    },
    {
        "name": "YearBuilt – שנת הבנייה",
        "reason": "שנת הבנייה עשויה להשפיע על מחיר הבית, משום שבתים חדשים יותר עשויים לכלול תשתיות ומערכות חדשות יותר."
    }
]

for feature in features:
    st.markdown(f"**{feature['name']}**")
    st.write(feature["reason"])

st.info("לסיכום: נשתמש בשטח הבית, במספר חדרי השינה ובשנת הבנייה כדי לנסות לחזות את מחיר הבית.")

st.divider()

# הצצה לנתונים
st.header("הצצה לדאטה")
st.dataframe(df.head(10), use_container_width=True)
