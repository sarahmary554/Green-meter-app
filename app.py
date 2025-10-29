import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Green Meter App", layout="wide")
st.title("🌿 Green Meter App")
st.write("Estimate and reduce your company's CO₂ emissions")

# ---------------- INPUTS ----------------
st.header("Input Data")

col1, col2 = st.columns(2)
with col1:
    cars = st.number_input("Car distance (km / year)", 0.0)
    trucks = st.number_input("Truck distance (km / year)", 0.0)
    buses = st.number_input("Bus distance (km / year)", 0.0)
    forklifts = st.number_input("Forklift hours / year", 0.0)
    planes = st.number_input("Cargo plane hours / year", 0.0)
with col2:
    lighting = st.number_input("Office lighting (kWh / year)", 0.0)
    heating = st.number_input("Heating (kWh-th / year)", 0.0)
    cooling = st.number_input("Cooling (kWh / year)", 0.0)
    computing = st.number_input("Computing (kWh / year)", 0.0)
    subcontractors = st.number_input("Subcontractor emissions (tons CO₂ / year)", 0.0)

st.header("Optimization Controls")
ev_share = st.slider("EV Share (%)", 0, 100, 0)
km_reduction = st.slider("KM Reduction for Cars (%)", 0, 50, 0)
load_factor = st.slider("Plane Load Factor (%)", 0, 100, 70)

# ---------------- CALCULATIONS ----------------
cars_co2 = cars * 0.18 * (1 - 0.7 * ev_share / 100) * (1 - km_reduction / 100)
trucks_co2 = trucks * 0.90
buses_co2 = buses * 1.10
forklift_co2 = forklifts * 4.0
planes_co2 = planes * 9000 * (load_factor / 100)
lighting_co2 = lighting * 0.42
heating_co2 = heating * 0.20
cooling_co2 = cooling * 0.42
computing_co2 = computing * 0.42
subcontractor_co2 = subcontractors * 1000  # convert tons to kg

baseline_total = (cars * 0.18 + trucks * 0.90 + buses * 1.10 +
                  forklifts * 4.0 + planes * 9000 +
                  lighting * 0.42 + heating * 0.20 +
                  cooling * 0.42 + computing * 0.42 +
                  subcontractors * 1000)

optimized_total = (cars_co2 + trucks_co2 + buses_co2 + forklift_co2 +
                   planes_co2 + lighting_co2 + heating_co2 +
                   cooling_co2 + computing_co2 + subcontractor_co2)

reduction_percent = 0
if baseline_total > 0:
    reduction_percent = (baseline_total - optimized_total) / baseline_total * 100

# ---------------- OUTPUTS ----------------
st.header("Results Dashboard")
colA, colB = st.columns(2)

with colA:
    st.subheader("Pie Chart – Emission Share by Category")
    labels = ["Cars", "Trucks", "Buses", "Forklifts", "Planes",
              "Lighting", "Heating", "Cooling", "Computing", "Subcontractors"]
    values = [cars_co2, trucks_co2, buses_co2, forklift_co2, planes_co2,
              lighting_co2, heating_co2, cooling_co2, computing_co2, subcontractor_co2]
    if sum(values) > 0:
        fig1, ax1 = plt.subplots()
        ax1.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig1)
    else:
        st.write("Enter data to view chart.")

with colB:
    st.subheader("Bar Chart – Baseline vs Optimized (tons CO₂)")
    fig2, ax2 = plt.subplots()
    ax2.bar(["Baseline", "Optimized"],
            [baseline_total/1000, optimized_total/1000],
            color=["red", "green"])
    st.pyplot(fig2)

st.metric(label="Baseline Total (tons CO₂)", value=round(baseline_total/1000, 2))
st.metric(label="Optimized Total (tons CO₂)", value=round(optimized_total/1000, 2))
st.metric(label="Reduction (%)", value=f"{round(reduction_percent, 1)} %")

# ---------------- AI INSIGHTS ----------------
st.header("AI Insights / Recommendations")
if baseline_total > 0:
    largest_idx = values.index(max(values))
    st.write(f"**Top Emitter:** {labels[largest_idx]} contributes the most CO₂.")
    if reduction_percent > 0:
        st.write(f"**Improvement:** Total emissions reduced by {round(reduction_percent,1)} %.")
    st.write("**Tip:** Increase EV share or reduce KM driven to cut transport emissions further.")
else:
    st.write("Enter activity data to view insights.")
