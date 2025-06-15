import streamlit as st
import numpy as np
import math

# Configure matplotlib for Streamlit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from scipy import stats
import pandas as pd

# Set page config
st.set_page_config(page_title="MathCraft | Interactive Normal Distribution", layout="wide")

# Clear matplotlib configurations
plt.style.use('default')
plt.rcParams.update({'figure.max_open_warning': 0})

st.title("🎯 MathCraft: Interactive Normal Distribution Explorer")

# Main Interactive Tool
st.header("🔧 Interactive Normal Distribution Calculator")

# Create main columns for the interface
control_col, plot_col1, plot_col2 = st.columns([1, 1, 1])

with control_col:
    st.subheader("🎛️ Controls")
    
    # Distribution 1 Controls
    st.markdown("**📊 Distribution 1**")
    mu1 = st.slider("μ₁ (Mean)", -5.0, 5.0, 0.0, 0.1, key="mu1")
    sigma1 = st.slider("σ₁ (Std Dev)", 0.1, 3.0, 1.0, 0.1, key="sigma1")
    show_dist1 = st.toggle("Show Distribution 1", value=True, key="show1")
    color1 = st.selectbox("Color 1", ["blue", "red", "green", "purple"], key="color1")
    
    st.markdown("---")
    
    # Distribution 2 Controls
    st.markdown("**📊 Distribution 2**")
    mu2 = st.slider("μ₂ (Mean)", -5.0, 5.0, 1.0, 0.1, key="mu2")
    sigma2 = st.slider("σ₂ (Std Dev)", 0.1, 3.0, 0.5, 0.1, key="sigma2")
    show_dist2 = st.toggle("Show Distribution 2", value=False, key="show2")
    color2 = st.selectbox("Color 2", ["red", "blue", "green", "orange"], key="color2")
    
    st.markdown("---")
    
    # Display Options
    st.markdown("**🎨 Display Options**")
    show_grid = st.toggle("Show Grid", value=True, key="grid")
    show_std_lines = st.toggle("Show Standard Deviation Lines", value=True, key="std_lines")
    show_area = st.toggle("Shade Area Under Curve", value=True, key="area")
    show_labels = st.toggle("Show Value Labels", value=True, key="labels")
    
    # Area Calculation
    st.markdown("---")
    st.markdown("**📐 Area Calculator**")
    calc_area = st.toggle("Calculate Area Between Values", key="calc_area")
    
    if calc_area:
        which_dist = st.radio("Which distribution?", ["Distribution 1", "Distribution 2"], key="which_dist")
        lower_bound = st.number_input("Lower bound:", value=-1.0, key="lower")
        upper_bound = st.number_input("Upper bound:", value=1.0, key="upper")
        
        # Calculate area
        if which_dist == "Distribution 1":
            area = stats.norm.cdf(upper_bound, mu1, sigma1) - stats.norm.cdf(lower_bound, mu1, sigma1)
            st.metric("Area (Probability)", f"{area:.4f}", f"{area*100:.2f}%")
        else:
            area = stats.norm.cdf(upper_bound, mu2, sigma2) - stats.norm.cdf(lower_bound, mu2, sigma2)
            st.metric("Area (Probability)", f"{area:.4f}", f"{area*100:.2f}%")

# Create the plots
with plot_col1:
    st.subheader("📈 Distribution 1 View")
    if show_dist1:
        try:
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            
            # Plot distribution 1
            x1 = np.linspace(mu1 - 4*sigma1, mu1 + 4*sigma1, 1000)
            y1 = stats.norm.pdf(x1, mu1, sigma1)
            
            ax1.plot(x1, y1, color=color1, linewidth=3, label=f'N(μ={mu1}, σ={sigma1})')
            
            if show_area:
                ax1.fill_between(x1, y1, alpha=0.3, color=color1)
            
            # Add mean line
            ax1.axvline(mu1, color='black', linestyle='-', linewidth=2, alpha=0.7)
            
            if show_labels:
                max_y = np.max(y1)
                ax1.text(mu1, max_y * 1.1, f'μ = {mu1}', ha='center', fontsize=12, weight='bold')
            
            # Add standard deviation lines
            if show_std_lines:
                for i in range(1, 4):
                    ax1.axvline(mu1 + i*sigma1, color='orange', linestyle='--', alpha=0.6)
                    ax1.axvline(mu1 - i*sigma1, color='orange', linestyle='--', alpha=0.6)
                    if show_labels:
                        ax1.text(mu1 + i*sigma1, max_y * 0.1, f'+{i}σ', ha='center', fontsize=10)
                        ax1.text(mu1 - i*sigma1, max_y * 0.1, f'-{i}σ', ha='center', fontsize=10)
            
            # Highlight area if calculating
            if calc_area and which_dist == "Distribution 1":
                x_area = x1[(x1 >= lower_bound) & (x1 <= upper_bound)]
                y_area = stats.norm.pdf(x_area, mu1, sigma1)
                ax1.fill_between(x_area, y_area, alpha=0.7, color='yellow', label=f'Area = {area:.4f}')
                ax1.axvline(lower_bound, color='red', linestyle=':', linewidth=2)
                ax1.axvline(upper_bound, color='red', linestyle=':', linewidth=2)
            
            ax1.set_xlabel('x')
            ax1.set_ylabel('Probability Density')
            ax1.set_title(f'Normal Distribution: μ={mu1}, σ={sigma1}')
            if show_grid:
                ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            st.pyplot(fig1)
            plt.close(fig1)
            
            # Show key statistics
            st.markdown(f"""
            **📊 Statistics for Distribution 1:**
            - Mean (μ): {mu1}
            - Standard Deviation (σ): {sigma1}
            - Variance (σ²): {sigma1**2:.3f}
            - Max Height: {np.max(y1):.3f}
            - 68% Range: [{mu1-sigma1:.2f}, {mu1+sigma1:.2f}]
            - 95% Range: [{mu1-2*sigma1:.2f}, {mu1+2*sigma1:.2f}]
            """)
            
        except Exception as e:
            st.error(f"Error creating plot: {e}")
    else:
        st.info("👆 Turn on 'Show Distribution 1' to see the plot")

with plot_col2:
    st.subheader("📈 Distribution 2 View")
    if show_dist2:
        try:
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            
            # Plot distribution 2
            x2 = np.linspace(mu2 - 4*sigma2, mu2 + 4*sigma2, 1000)
            y2 = stats.norm.pdf(x2, mu2, sigma2)
            
            ax2.plot(x2, y2, color=color2, linewidth=3, label=f'N(μ={mu2}, σ={sigma2})')
            
            if show_area:
                ax2.fill_between(x2, y2, alpha=0.3, color=color2)
            
            # Add mean line
            ax2.axvline(mu2, color='black', linestyle='-', linewidth=2, alpha=0.7)
            
            if show_labels:
                max_y = np.max(y2)
                ax2.text(mu2, max_y * 1.1, f'μ = {mu2}', ha='center', fontsize=12, weight='bold')
            
            # Add standard deviation lines
            if show_std_lines:
                for i in range(1, 4):
                    ax2.axvline(mu2 + i*sigma2, color='orange', linestyle='--', alpha=0.6)
                    ax2.axvline(mu2 - i*sigma2, color='orange', linestyle='--', alpha=0.6)
                    if show_labels:
                        ax2.text(mu2 + i*sigma2, max_y * 0.1, f'+{i}σ', ha='center', fontsize=10)
                        ax2.text(mu2 - i*sigma2, max_y * 0.1, f'-{i}σ', ha='center', fontsize=10)
            
            # Highlight area if calculating
            if calc_area and which_dist == "Distribution 2":
                x_area = x2[(x2 >= lower_bound) & (x2 <= upper_bound)]
                y_area = stats.norm.pdf(x_area, mu2, sigma2)
                ax2.fill_between(x_area, y_area, alpha=0.7, color='yellow', label=f'Area = {area:.4f}')
                ax2.axvline(lower_bound, color='red', linestyle=':', linewidth=2)
                ax2.axvline(upper_bound, color='red', linestyle=':', linewidth=2)
            
            ax2.set_xlabel('x')
            ax2.set_ylabel('Probability Density')
            ax2.set_title(f'Normal Distribution: μ={mu2}, σ={sigma2}')
            if show_grid:
                ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            st.pyplot(fig2)
            plt.close(fig2)
            
            # Show key statistics
            st.markdown(f"""
            **📊 Statistics for Distribution 2:**
            - Mean (μ): {mu2}
            - Standard Deviation (σ): {sigma2}
            - Variance (σ²): {sigma2**2:.3f}
            - Max Height: {np.max(y2):.3f}
            - 68% Range: [{mu2-sigma2:.2f}, {mu2+sigma2:.2f}]
            - 95% Range: [{mu2-2*sigma2:.2f}, {mu2+2*sigma2:.2f}]
            """)
            
        except Exception as e:
            st.error(f"Error creating plot: {e}")
    else:
        st.info("👆 Turn on 'Show Distribution 2' to see the plot")

# Comparison View
if show_dist1 and show_dist2:
    st.markdown("---")
    st.header("⚖️ Side-by-Side Comparison")
    
    try:
        fig_comp, ax_comp = plt.subplots(figsize=(12, 8))
        
        # Plot both distributions
        x1 = np.linspace(mu1 - 4*sigma1, mu1 + 4*sigma1, 1000)
        y1 = stats.norm.pdf(x1, mu1, sigma1)
        x2 = np.linspace(mu2 - 4*sigma2, mu2 + 4*sigma2, 1000)
        y2 = stats.norm.pdf(x2, mu2, sigma2)
        
        ax_comp.plot(x1, y1, color=color1, linewidth=3, label=f'Dist 1: N(μ={mu1}, σ={sigma1})')
        ax_comp.plot(x2, y2, color=color2, linewidth=3, label=f'Dist 2: N(μ={mu2}, σ={sigma2})')
        
        if show_area:
            ax_comp.fill_between(x1, y1, alpha=0.2, color=color1)
            ax_comp.fill_between(x2, y2, alpha=0.2, color=color2)
        
        # Add mean lines
        ax_comp.axvline(mu1, color=color1, linestyle='-', linewidth=2, alpha=0.8)
        ax_comp.axvline(mu2, color=color2, linestyle='-', linewidth=2, alpha=0.8)
        
        ax_comp.set_xlabel('x')
        ax_comp.set_ylabel('Probability Density')
        ax_comp.set_title('Comparison of Normal Distributions')
        if show_grid:
            ax_comp.grid(True, alpha=0.3)
        ax_comp.legend()
        
        st.pyplot(fig_comp)
        plt.close(fig_comp)
        
        # Comparison metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mean Difference", f"{abs(mu2 - mu1):.3f}")
        with col2:
            st.metric("Std Dev Difference", f"{abs(sigma2 - sigma1):.3f}")
        with col3:
            overlap_area = 0.5 * (stats.norm.cdf(min(mu1, mu2) + 2*max(sigma1, sigma2), mu1, sigma1) + 
                                 stats.norm.cdf(min(mu1, mu2) + 2*max(sigma1, sigma2), mu2, sigma2))
            st.metric("Approximate Overlap", f"{overlap_area:.3f}")
            
    except Exception as e:
        st.error(f"Error creating comparison plot: {e}")

# Interactive Conjecture Testing
st.markdown("---")
st.header("🧪 Test Your Conjectures!")

st.markdown("**Use the controls above to test these statements. Mark each as TRUE or FALSE:**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**A.** As the mean increases, the normal curve shifts to the left.")
    answer_a = st.radio("Your answer:", ["True", "False"], key="answer_a")
    
    st.markdown("**B.** The standard deviation determines the width of the normal distribution.")
    answer_b = st.radio("Your answer:", ["True", "False"], key="answer_b")

with col2:
    st.markdown("**C.** A normal curve with a very large mean and large standard deviation is tall and wide.")
    answer_c = st.radio("Your answer:", ["True", "False"], key="answer_c")
    
    st.markdown("**D.** The area under any normal curve is always 1.")
    answer_d = st.radio("Your answer:", ["True", "False"], key="answer_d")

if st.button("🎯 Check My Answers!"):
    results = []
    
    if answer_a == "False":
        results.append("✅ A. CORRECT! The curve shifts RIGHT as mean increases.")
    else:
        results.append("❌ A. INCORRECT. Try increasing μ₁ and watch the curve move right!")
    
    if answer_b == "True":
        results.append("✅ B. CORRECT! Larger σ = wider curve.")
    else:
        results.append("❌ B. INCORRECT. Try changing σ₁ and observe the width!")
    
    if answer_c == "False":
        results.append("✅ C. CORRECT! Large σ makes curves SHORTER and wider.")
    else:
        results.append("❌ C. INCORRECT. Try σ₁ = 3.0 and see the height decrease!")
    
    if answer_d == "True":
        results.append("✅ D. CORRECT! All normal curves have area = 1.")
    else:
        results.append("❌ D. INCORRECT. This is always true for any normal distribution!")
    
    for result in results:
        st.write(result)

# Quick Tools Section
st.markdown("---")
st.header("🛠️ Quick Tools")

tool_tabs = st.tabs(["📊 Z-Score Calculator", "📈 Percentile Finder", "🎯 Probability Calculator", "📋 68-95-99.7 Rule"])

with tool_tabs[0]:
    st.subheader("Calculate Z-Score")
    z_value = st.number_input("Enter value (x):", value=1.5, key="z_val")
    z_mu = st.number_input("Mean (μ):", value=0.0, key="z_mu")
    z_sigma = st.number_input("Std Dev (σ):", value=1.0, min_value=0.1, key="z_sigma")
    
    z_score = (z_value - z_mu) / z_sigma
    st.metric("Z-Score", f"{z_score:.4f}")
    st.write(f"This value is {abs(z_score):.2f} standard deviations {'above' if z_score > 0 else 'below'} the mean.")

with tool_tabs[1]:
    st.subheader("Find Percentile")
    p_value = st.number_input("Enter value:", value=1.0, key="p_val")
    p_mu = st.number_input("Mean:", value=0.0, key="p_mu")
    p_sigma = st.number_input("Std Dev:", value=1.0, min_value=0.1, key="p_sigma")
    
    percentile = stats.norm.cdf(p_value, p_mu, p_sigma) * 100
    st.metric("Percentile", f"{percentile:.2f}%")
    st.write(f"{percentile:.1f}% of values are below {p_value}")

with tool_tabs[2]:
    st.subheader("Calculate Probability")
    prob_mu = st.number_input("Mean:", value=0.0, key="prob_mu")
    prob_sigma = st.number_input("Std Dev:", value=1.0, min_value=0.1, key="prob_sigma")
    prob_lower = st.number_input("Lower bound:", value=-1.0, key="prob_lower")
    prob_upper = st.number_input("Upper bound:", value=1.0, key="prob_upper")
    
    probability = stats.norm.cdf(prob_upper, prob_mu, prob_sigma) - stats.norm.cdf(prob_lower, prob_mu, prob_sigma)
    st.metric("Probability", f"{probability:.4f}")
    st.metric("Percentage", f"{probability*100:.2f}%")

with tool_tabs[3]:
    st.subheader("68-95-99.7 Rule Visualizer")
    rule_mu = st.number_input("Mean:", value=0.0, key="rule_mu")
    rule_sigma = st.number_input("Std Dev:", value=1.0, min_value=0.1, key="rule_sigma")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("68% Range", f"[{rule_mu-rule_sigma:.2f}, {rule_mu+rule_sigma:.2f}]")
    with col2:
        st.metric("95% Range", f"[{rule_mu-2*rule_sigma:.2f}, {rule_mu+2*rule_sigma:.2f}]")
    with col3:
        st.metric("99.7% Range", f"[{rule_mu-3*rule_sigma:.2f}, {rule_mu+3*rule_sigma:.2f}]")

# Educational Links and Resources
st.markdown("---")
st.header("📚 Learn More")

resource_cols = st.columns(4)

with resource_cols[0]:
    st.markdown("""
    **📖 Khan Academy**
    - [Normal Distribution Intro](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library)
    - [68-95-99.7 Rule](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/ck12-the-empirical-rule)
    """)

with resource_cols[1]:
    st.markdown("""
    **🎮 Interactive Tools**
    - [Desmos Normal Distribution](https://www.desmos.com/calculator)
    - [GeoGebra Statistics](https://www.geogebra.org/statistics)
    """)

with resource_cols[2]:
    st.markdown("""
    **📊 Real Data**
    - [StatCrunch Datasets](https://www.statcrunch.com/)
    - [FiveThirtyEight Data](https://fivethirtyeight.com/data/)
    """)

with resource_cols[3]:
    st.markdown("""
    **🔬 Simulations**
    - [PhET Probability](https://phet.colorado.edu/en/simulations/category/math)
    - [Wolfram Demonstrations](https://demonstrations.wolfram.com/)
    """)

st.markdown("---")
st.markdown("*🎯 MathCraft: Making mathematics interactive, engaging, and meaningful through hands-on exploration!*")
