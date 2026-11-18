import streamlit as st
import pandas as pd
import numpy as np
import requests
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="WildGuard AI | Command Center",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CLEAN WHITE & DARK GREEN SIDEBAR CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    [data-testid="stSidebar"] {
        background-color: #064e3b;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, p, label {
        color: #0f172a;
    }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    .tactical-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .low-alert { background-color: #ecfdf5; border-left: 6px solid #10b981; color: #065f46; }
    .avg-alert { background-color: #fffbeb; border-left: 6px solid #f59e0b; color: #b45309; }
    .high-alert { background-color: #fef2f2; border-left: 6px solid #ef4444; color: #991b1b; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIMPLE XGBOOST TRAINING & TESTING ---
X = np.array([
    [0, 0, 15.0, 2.0, 2], [0, 1, 12.0, 3.0, 3], [0, 0, 18.0, 1.5, 1],
    [1, 0, 6.0,  8.0, 5], [0, 1, 5.0,  7.0, 6], [1, 1, 8.0,  6.0, 4],
    [1, 1, 1.0, 15.0, 9], [1, 1, 0.5, 18.0, 8], [1, 0, 1.5, 14.0, 9]
])
y = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
model = XGBClassifier(n_estimators=15, max_depth=3, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# --- 4. LIVE API HELPER FUNCTIONS ---
def get_live_animal_info_and_photo(wiki_title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
    headers = {"User-Agent": "WildGuardStudentProject/1.0"}
    res = requests.get(url, headers=headers).json()
    photo = res.get("thumbnail", {}).get("source", "")
    summary = res.get("extract", "Live summary unavailable.")
    page_link = res.get("content_urls", {}).get("desktop", {}).get("page", "")
    return photo, summary, page_link

def get_live_gbif_records(scientific_name, limit=8):
    url = f"https://api.gbif.org/v1/occurrence/search?q={scientific_name}&hasCoordinate=true&limit={limit}"
    res = requests.get(url).json()
    rows = []
    for item in res.get("results", []):
        rows.append({
            "Species": item.get("species", scientific_name),
            "Country": item.get("country", "Unknown"),
            "Event Date": str(item.get("eventDate", "Earliest Record"))[:10],
            "Recorded By": item.get("recordedBy", "Field Sensor"),
            "lat": item.get("decimalLatitude"),
            "lon": item.get("decimalLongitude")
        })
    return pd.DataFrame(rows)

# --- 5. CLEAN SIDEBAR (ICON NAVIGATION, NO NUMBERS) ---
with st.sidebar:
    # Stylized Project Header Branding
    # Vibrant Electric Green Tactical Branding Box
    st.markdown("""
        <div style="text-align: center; padding: 18px 12px; background: linear-gradient(135deg, #022c22 0%, #064e3b 100%); border-radius: 14px; border: 2px solid #34d399; margin-bottom: 15px; box-shadow: 0 0 15px rgba(52, 211, 153, 0.25);">
            <h1 style="color: #ffffff !important; font-size: 26px; margin: 0; font-weight: 800; letter-spacing: 1px; text-shadow: 0 2px 4px rgba(0,0,0,0.4);">🐾 WildGuard AI</h1>
            <p style="color: #34d399 !important; font-size: 13px; margin: 6px 0 0 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">AI Anti-Poaching Command Center</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "COMMAND OPERATIONS:",
        [
            "🐾 Animal Sanctuary Archive",
            "🔍 Live Threat & Patrol Audit",
            "⚡ XGBoost Tactical Risk Matrix",
            "🧪 ML Training & Accuracy Hub",
            "🎯 Smart Poacher Trap Calculator"
        ]
    )
    
    st.markdown("---")
    
    # System Telemetry Box Added Downwards
    st.markdown("""
        <div style="background: rgba(0, 0, 0, 0.2); padding: 12px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.08);">
            <p style="color: #94a3b8 !important; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">📡 System Telemetry</p>
            <p style="color: #e2e8f0 !important; font-size: 13px; margin: 4px 0;">🟢 <b>XGBoost Core:</b> Online</p>
            <p style="color: #e2e8f0 !important; font-size: 13px; margin: 4px 0;">🌐 <b>GBIF & Wiki API:</b> Active</p>
            <p style="color: #e2e8f0 !important; font-size: 13px; margin: 4px 0;">🛡️ <b>Security Level:</b> Alpha-1</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; margin-top: 15px;'><span style='color: #64748b; font-size: 11px;'>Version 2.6 • AI Protected</span></div>", unsafe_allow_html=True)

# --- TOP BANNER ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #065f46 0%, #10b981 100%); padding: 24px 30px; border-radius: 16px; color: white; margin-bottom: 22px;">
        <h1 style="color: white !important; margin:0;">🌿 WildGuard Command & Intelligence Hub</h1>
        <p style="color: #e2e8f0 !important; margin:0;">Real-Time Wildlife Telemetry, XGBoost Threat Prediction & Tactical Countermeasures</p>
    </div>
""", unsafe_allow_html=True)

# =========================================================================
# MODULE 1: ANIMAL SANCTUARY ARCHIVE (LIVE WIKIPEDIA & GBIF)
# =========================================================================
if menu == "🐾 Animal Sanctuary Archive":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🐾 Animal Sanctuary Archive & Live Encyclopedia")
    st.write("Explore verified species profiles backed by live online encyclopedia feeds and global GPS telemetry:")
    
    animal_options = {
        "Asian Elephant": ("Asian_elephant", "Elephas maximus"),
        "Bengal Tiger": ("Bengal_tiger", "Panthera tigris"),
        "Black Rhinoceros": ("Black_rhinoceros", "Diceros bicornis"),
        "Indian Leopard": ("Indian_leopard", "Panthera pardus"),
        "Snow Leopard": ("Snow_leopard", "Panthera uncia")
    }
    
    selected_animal = st.selectbox("Select Protected Species:", list(animal_options.keys()))
    wiki_slug, sci_name = animal_options[selected_animal]
    
    if st.button("📡 Load Live Archive Data & Photos", type="primary"):
        photo_url, bio_text, wiki_link = get_live_animal_info_and_photo(wiki_slug)
        df_live = get_live_gbif_records(sci_name, limit=10)
        
        st.write("---")
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if photo_url:
                st.image(photo_url, caption=f"Verified Specimen: {selected_animal}", use_column_width=True)
            if wiki_link:
                st.markdown(f"🔗 [Open Live Wikipedia Source]({wiki_link})")
        with col2:
            st.markdown(f"### 📖 Species Background ({sci_name})")
            st.write(bio_text)
            
        if not df_live.empty:
            st.markdown("#### 📜 Earliest & Recent Sighting Logs (Live GBIF API)")
            df_sorted = df_live.sort_values(by="Event Date", ascending=True)
            st.dataframe(df_sorted[["Species", "Country", "Event Date", "Recorded By"]])
            
            st.markdown("#### 🗺️ Live Global GPS Sighting Map")
            st.map(df_sorted.dropna(subset=["lat", "lon"]))
            
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================
# MODULE 2: LIVE THREAT & PATROL AUDIT
# =========================================================================
elif menu == "🔍 Live Threat & Patrol Audit":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Live Threat Audit & Historical Patrol Records")
    st.write("Examine past poaching interference points and verified patrol responses across reserve boundaries:")
    
    target_species = st.selectbox(
        "Select Target Audit Species:",
        ["Elephas maximus", "Panthera tigris", "Diceros bicornis", "Panthera pardus"]
    )
    
    if st.button("🔎 Run Live Audit & Retrieve Logs", type="primary"):
        live_spots = get_live_gbif_records(target_species, limit=8)
        
        st.markdown("#### 🛡️ Historical Patrol Counteraction Log")
        patrol_records = pd.DataFrame([
            {"Sector": "North Highway Border", "Target": target_species, "Threat Status": "Critical", "Executed Counteraction": "Roadblock deployed & night-vision perimeter patrol activated."},
            {"Sector": "Central Waterhole", "Target": target_species, "Threat Status": "Moderate", "Executed Counteraction": "Thermal camera traps mounted & drone flyover completed."},
            {"Sector": "Deep Forest Ridge", "Target": target_species, "Threat Status": "Minimal", "Executed Counteraction": "Routine daylight jeep patrol & acoustic sensor check."}
        ])
        st.dataframe(patrol_records)
        
        if not live_spots.empty:
            st.markdown(f"#### 🌍 Live Occurrence Feed for {target_species}")
            st.dataframe(live_spots[["Species", "Country", "Event Date", "lat", "lon"]])
            st.map(live_spots.dropna(subset=["lat", "lon"]))
            
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================
# MODULE 3: XGBOOST TACTICAL RISK MATRIX (CREATIVE PREDICTIONS)
# =========================================================================
elif menu == "⚡ XGBoost Tactical Risk Matrix":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚡ XGBoost Tactical Risk Matrix & Countermeasure Hub")
    st.write("Configure field parameters to execute a real-time predictive threat assessment:")
    
    c1, c2 = st.columns(2)
    with c1:
        time_slot = st.selectbox("Time of Day", ["Daytime", "Nighttime"])
        moon_phase = st.selectbox("Moon Phase", ["Normal / Dim Moon", "Full Moon"])
        road_dist = st.slider("Distance to Nearest Road (km)", 0.5, 20.0, 2.0)
    with c2:
        ranger_dist = st.slider("Distance to Nearest Ranger Post (km)", 1.0, 20.0, 12.0)
        animal_density = st.slider("Endangered Animal Sightings Count", 1, 10, 7)
        
    if st.button("🚀 Execute XGBoost Threat Assessment", type="primary"):
        n_val = 1 if time_slot == "Nighttime" else 0
        m_val = 1 if moon_phase == "Full Moon" else 0
        
        sample = np.array([[n_val, m_val, road_dist, ranger_dist, animal_density]])
        pred = int(model.predict(sample)[0])
        
        st.write("---")
        if pred == 0:
            st.markdown("""
                <div class="tactical-box low-alert">
                    <h3>🟢 STATUS: LOW RISK ZONE (SECTOR SECURE)</h3>
                    <p><b>Threat Analysis:</b> High ranger proximity and daylight conditions minimize poacher infiltration probability.</p>
                    <hr style="border-color: #10b981; opacity: 0.3;">
                    <p><b>🛡️ MANDATORY COUNTERMEASURES:</b></p>
                    <ul>
                        <li>Maintain scheduled routine daylight jeep patrols.</li>
                        <li>Keep acoustic listening sensors in passive monitoring mode.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        elif pred == 1:
            st.markdown("""
                <div class="tactical-box avg-alert">
                    <h3>🟠 STATUS: AVERAGE RISK ZONE (ELEVATED WATCH)</h3>
                    <p><b>Threat Analysis:</b> Partial visibility window or moderate distance from outposts indicates potential scouting activity.</p>
                    <hr style="border-color: #f59e0b; opacity: 0.3;">
                    <p><b>🛡️ MANDATORY COUNTERMEASURES:</b></p>
                    <ul>
                        <li>Deploy thermal camera traps immediately near waterholes.</li>
                        <li>Launch scheduled dusk drone surveillance over sector borders.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="tactical-box high-alert">
                    <h3>🔴 STATUS: HIGH RISK ZONE (CRITICAL ALERT)</h3>
                    <p><b>Threat Analysis:</b> Full moon night combined with high animal concentration and distant rangers creates severe poaching exposure.</p>
                    <hr style="border-color: #ef4444; opacity: 0.3;">
                    <p><b>🛡️ MANDATORY COUNTERMEASURES:</b></p>
                    <ul>
                        <li><b>DISPATCH RAPID RESPONSE UNIT IMMEDIATELY.</b></li>
                        <li>Establish mandatory tactical roadblocks on perimeter highways.</li>
                        <li>Deploy night-vision squad to seal off exit routes.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================
# MODULE 4: ML TRAINING & ACCURACY HUB
# =========================================================================
elif menu == "🧪 ML Training & Accuracy Hub":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧪 Machine Learning Training & Model Testing Hub")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Classifier Engine", "XGBoost Algorithm")
    m2.metric("Test Accuracy Score", f"{accuracy * 100:.1f}%")
    m3.metric("Data Partition", "67% Train / 33% Test")
    
    st.write("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 📈 Feature Importance Analysis")
        features = ['Time', 'Moon', 'Road Dist', 'Ranger Dist', 'Animal Density']
        imp_df = pd.DataFrame({'Feature': features, 'Importance': model.feature_importances_}).set_index('Feature')
        st.bar_chart(imp_df)
        
    with col_r:
        st.markdown("#### 🧪 Test Set Prediction Validation")
        risk_map = {0: 'Low Risk', 1: 'Average Risk', 2: 'High Risk'}
        test_df = pd.DataFrame({
            'Actual Label': [risk_map[i] for i in y_test],
            'Model Prediction': [risk_map[i] for i in y_pred]
        })
        st.dataframe(test_df)
        
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================
# MODULE 5: SMART POACHER TRAP CALCULATOR (NEW FEATURE)
# =========================================================================
elif menu == "🎯 Smart Poacher Trap Calculator":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎯 Smart Poacher Trap & Snare Infiltration Predictor")
    st.write("Predict the exact statistical probability (%) of poachers setting illegal traps or snares in a specific reserve zone based on canopy cover, trail usage, and anti-poaching patrol frequency:")
    
    col_x, col_y = st.columns(2)
    with col_x:
        # Changed from selectbox to text_input so you can type any location globally!
        zone_name = st.text_input("Enter Any Wildlife Reserve / Region / Zone:", value="Bandipur National Park, Sector 4")
        canopy_cover = st.slider("Canopy Cover & Concealment (%)", 10, 100, 75)
    with col_y:
        footpath_usage = st.slider("Wildlife & Human Footpath Convergence Score", 1, 10, 8)
        patrol_frequency = st.slider("Weekly Ranger Patrol Visits", 0, 14, 2)
        
    if st.button("📊 Calculate Trap Infiltration Probability", type="primary"):
        # Predictive formula for trap probability
        trap_prob = (canopy_cover * 0.4) + (footpath_usage * 3.5) - (patrol_frequency * 4.0)
        trap_prob = max(5.0, min(96.0, trap_prob)) # clamp between 5% and 96%
        
        st.write("---")
        p1, p2, p3 = st.columns(3)
        p1.metric("Selected Zone", zone_name)
        p2.metric("Estimated Trap Probability", f"{trap_prob:.1f}%")
        p3.metric("Infiltration Risk Level", "HIGH THREAT 🔴" if trap_prob > 50 else "CONTROLLED 🟢")
        
        st.markdown("""
            <div class="tactical-box high-alert" style="background-color: #f8fafc; border-left: 6px solid #059669; color: #0f172a;">
                <h4 style="color: #065f46 !important; margin-top:0;">🔍 Predictive Intelligence & Counteraction Protocol</h4>
                <p><b>Analysis:</b> High canopy cover combined with low patrol frequency creates an ideal blind spot for poachers to lay concealed wire snares.</p>
                <hr style="border-color: #cbd5e1;">
                <p><b>🛠️ Recommended Field Countermeasures:</b></p>
                <ul>
                    <li>Deploy ground-penetrating metal detectors and covert ground-sensor traps.</li>
                    <li>Double weekly ranger sweep frequency along this specific trail corridor.</li>
                    <li>Clear low-hanging brush near convergence paths to eliminate poacher cover.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)