import streamlit as st
import numpy as np
import math

# Configure matplotlib for Streamlit
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
plt.style.use('default')  # Ensure consistent styling

from scipy import stats
import pandas as pd

st.set_page_config(page_title="MathCraft | Normal Distribution", layout="wide")
st.title("📊 MathCraft: Exploring the Normal Distribution")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Choose a section:", [
    "📚 Introduction", 
    "🔍 Interactive Explorer", 
    "🛠️ Physical Manipulatives", 
    "🌍 Real-World Applications", 
    "📝 Problem Solving",
    "🧪 Hypothesis Testing"
])

if section == "📚 Introduction":
    st.markdown("""
    ### 📈 What is the Normal Distribution?
    The **normal distribution** (also called the Gaussian distribution or bell curve) is one of the most important probability distributions in statistics. It describes how data values are distributed around a central mean value.
    
    **Key Characteristics:**
    - **Bell-shaped curve** that is symmetric around the mean
    - **Mean (μ)**: The center point of the distribution
    - **Standard deviation (σ)**: Controls the spread or width of the curve
    - **Total area under the curve = 1** (representing 100% probability)
    - **68-95-99.7 Rule**: Approximately 68% of data falls within 1σ, 95% within 2σ, and 99.7% within 3σ
    """)
    
    # Basic normal distribution properties table
    st.markdown("""
    ### 📐 Normal Distribution Properties
    | Property | Description | Mathematical Expression |
    |----------|-------------|------------------------|
    | Mean (μ) | Center of the distribution | E[X] = μ |
    | Standard Deviation (σ) | Measure of spread | σ > 0 |
    | Variance (σ²) | Square of standard deviation | Var[X] = σ² |
    | Probability Density Function | Formula for the curve | $f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}(\\frac{x-\\mu}{\\sigma})^2}$ |
    | Standard Normal | Special case with μ=0, σ=1 | Z ~ N(0,1) |
    """)
    
    # Create a basic normal distribution plot
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)
    
    ax.plot(x, y, 'b-', linewidth=3, label='Standard Normal (μ=0, σ=1)')
    ax.fill_between(x, y, alpha=0.3)
    
    # Add vertical lines for standard deviations
    for i in range(-3, 4):
        ax.axvline(i, color='red', linestyle='--', alpha=0.5)
        if i != 0:
            ax.text(i, 0.05, f'{i}σ', ha='center', fontsize=10)
    
    ax.axvline(0, color='red', linestyle='-', linewidth=2, label='Mean (μ)')
    ax.set_xlabel('Standard Deviations from Mean')
    ax.set_ylabel('Probability Density')
    ax.set_title('The Standard Normal Distribution')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    st.pyplot(fig)

elif section == "🔍 Interactive Explorer":
    st.header("🔍 Interactive Normal Distribution Explorer")
    
    st.markdown("""
    **Investigate how changing the mean (μ) and standard deviation (σ) affects the normal curve!**
    Use the sliders below to manipulate the parameters and observe the changes.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        
        # Interactive controls
        mu = st.slider("Mean (μ)", -5.0, 5.0, 0.0, 0.1, help="Controls the center of the distribution")
        sigma = st.slider("Standard Deviation (σ)", 0.1, 3.0, 1.0, 0.1, help="Controls the spread of the distribution")
        
        # Comparison mode
        show_comparison = st.checkbox("Compare with Standard Normal", help="Show both your curve and the standard normal")
        
        # Display current parameters
        st.markdown(f"""
        **Current Distribution:**
        - Mean (μ) = {mu}
        - Standard Deviation (σ) = {sigma}
        - Variance (σ²) = {sigma**2:.2f}
        """)
        
        # Calculate key statistics
        x_range = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
        y_values = stats.norm.pdf(x_range, mu, sigma)
        max_height = np.max(y_values)
        
        st.markdown(f"""
        **Curve Properties:**
        - Maximum height: {max_height:.3f}
        - 68% of data between: [{mu-sigma:.1f}, {mu+sigma:.1f}]
        - 95% of data between: [{mu-2*sigma:.1f}, {mu+2*sigma:.1f}]
        - 99.7% of data between: [{mu-3*sigma:.1f}, {mu+3*sigma:.1f}]
        """)
    
    with col2:
        # Create the interactive plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot the current distribution
        x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
        y = stats.norm.pdf(x, mu, sigma)
        
        ax.plot(x, y, 'b-', linewidth=3, label=f'Normal(μ={mu}, σ={sigma})')
        ax.fill_between(x, y, alpha=0.3, color='blue')
        
        # Show comparison with standard normal if requested
        if show_comparison:
            x_std = np.linspace(-5, 5, 1000)
            y_std = stats.norm.pdf(x_std, 0, 1)
            ax.plot(x_std, y_std, 'r--', linewidth=2, label='Standard Normal (μ=0, σ=1)')
        
        # Add mean line
        ax.axvline(mu, color='red', linestyle='-', linewidth=2, label=f'Mean (μ={mu})')
        
        # Add standard deviation markers
        for i in range(1, 4):
            ax.axvline(mu + i*sigma, color='orange', linestyle=':', alpha=0.7)
            ax.axvline(mu - i*sigma, color='orange', linestyle=':', alpha=0.7)
            if mu + i*sigma <= ax.get_xlim()[1]:
                ax.text(mu + i*sigma, max_height*0.1, f'+{i}σ', ha='center', fontsize=9)
            if mu - i*sigma >= ax.get_xlim()[0]:
                ax.text(mu - i*sigma, max_height*0.1, f'-{i}σ', ha='center', fontsize=9)
        
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density f(x)')
        ax.set_title(f'Normal Distribution: μ={mu}, σ={sigma}')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Set reasonable axis limits
        x_min = min(mu - 4*sigma, -5 if show_comparison else mu - 4*sigma)
        x_max = max(mu + 4*sigma, 5 if show_comparison else mu + 4*sigma)
        ax.set_xlim(x_min, x_max)
        
        st.pyplot(fig)
    
    # Conjecture testing section
    st.markdown("---")
    st.subheader("🧪 Test These Conjectures!")
    
    with st.expander("Conjecture Testing Activity"):
        st.markdown("""
        Use the sliders above to test these conjectures. Which ones are TRUE and which are FALSE?
        
        **A.** As the mean increases, the normal curve shifts to the left.
        **B.** The standard deviation determines the width of the normal distribution.
        **C.** A normal curve with a very large mean and large standard deviation is tall and wide.
        **D.** The area between a normal curve with a small standard deviation and the horizontal axis is much less than the area between a normal curve with a large standard deviation and the horizontal axis.
        """)
        
        if st.button("Show Answers"):
            st.markdown("""
            **Answers:**
            - **A. FALSE** - As the mean increases, the curve shifts to the RIGHT, not left.
            - **B. TRUE** - Larger σ = wider curve, smaller σ = narrower curve.
            - **C. FALSE** - Large standard deviation makes curves SHORTER and wider, not tall and wide.
            - **D. FALSE** - The total area under ANY normal curve is always 1 (100%).
            """)

elif section == "🛠️ Physical Manipulatives":
    st.header("🛠️ Hands-On Activities & Physical Manipulatives")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📏 Bean Machine", "📊 Data Collection", "🎯 Probability Games", "📐 Paper Models"])
    
    with tab1:
        st.subheader("Galton Board (Bean Machine)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔧 Build Your Own Galton Board:**
            1. **Materials**: Pegboard, marbles/beans, funnel, collection bins
            2. **Setup**: Arrange pegs in triangular pattern
            3. **Process**: Drop marbles through the top
            4. **Observe**: They collect in bins forming a bell curve
            
            **🎯 Learning Objectives:**
            - Visualize random processes creating normal distributions
            - Connect probability to physical phenomena
            - Understand central limit theorem basics
            """)
        
        with col2:
            st.markdown("""
            **📝 Investigation Questions:**
            - What happens with 10 marbles vs 100 marbles?
            - How does the number of peg rows affect the distribution?
            - What if you change the peg spacing?
            - Can you predict where most marbles will land?
            
            **🔍 Extensions:**
            - Graph the results and compare to theoretical normal curve
            - Calculate mean and standard deviation of your data
            - Repeat experiment and compare results
            """)
    
    with tab2:
        st.subheader("Real Data Collection Activities")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📊 Height Measurement Project:**
            1. Measure heights of all students in class
            2. Create histogram of the data
            3. Calculate mean and standard deviation
            4. Compare to theoretical normal curve
            5. Discuss why heights follow normal distribution
            
            **🕐 Reaction Time Experiment:**
            1. Use online reaction time tests
            2. Each student takes 20 measurements
            3. Pool all class data together
            4. Analyze the distribution shape
            """)
        
        with col2:
            st.markdown("""
            **🎲 Dice Sum Investigation:**
            1. Roll two dice 100 times
            2. Record the sum each time
            3. Create frequency table and histogram
            4. Compare to normal distribution
            5. Try with 3 dice, then 4 dice
            
            **📏 Paper Airplane Distance:**
            1. Each student makes identical paper airplane
            2. Fly 10 times, measure distances
            3. Combine all flight data
            4. Analyze the resulting distribution
            """)
    
    with tab3:
        st.subheader("Probability Games & Simulations")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🎰 Coin Flip Proportions:**
            1. Flip 10 coins, count heads
            2. Repeat 50 times
            3. Graph proportion of heads
            4. Observe normal distribution emergence
            
            **🎯 Basketball Free Throws:**
            1. Students attempt 20 free throws
            2. Record number of successful shots
            3. Compile class data
            4. Analyze distribution of success rates
            """)
        
        with col2:
            st.markdown("""
            **🌡️ Temperature Tracking:**
            1. Record daily high temperatures for 30 days
            2. Calculate daily average temperature
            3. Look at distribution of temperatures
            4. Compare different seasons
            
            **⏱️ Traffic Light Timing:**
            1. Time how long students wait at traffic lights
            2. Collect data over several days
            3. Analyze wait time distribution
            4. Discuss real-world applications
            """)
    
    with tab4:
        st.subheader("Paper and Cardboard Models")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📊 3D Bell Curve Model:**
            1. **Materials**: Cardboard, graph paper, scissors
            2. **Process**: 
               - Plot normal curve on graph paper
               - Cut out multiple identical curves
               - Stack to create 3D model
            3. **Learning**: Visualize area under curve concepts
            
            **📏 Sliding Scale Model:**
            1. Create paper strips with different normal curves
            2. Use sliders to change μ and σ parameters
            3. Observe how curves shift and stretch
            """)
        
        with col2:
            st.markdown("""
            **🎨 Area Visualization:**
            1. Draw normal curve on large paper
            2. Color regions for 68-95-99.7 rule
            3. Cut out pieces to compare areas
            4. Stack pieces to show probability
            
            **📐 Standard Deviation Ruler:**
            1. Create ruler marked in standard deviations
            2. Use with different normal curves
            3. Measure areas between standard deviations
            4. Verify the empirical rule
            """)

elif section == "🌍 Real-World Applications":
    st.header("🌍 Real-World Applications of Normal Distribution")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 Medicine & Health", "📈 Business & Economics", "🔬 Science & Research", "🎓 Education & Testing"])
    
    with tab1:
        st.subheader("Medicine & Health Applications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🩺 Medical Measurements:**
            - **Blood pressure**: Systolic and diastolic readings
            - **Cholesterol levels**: Risk assessment and treatment
            - **BMI distribution**: Population health studies
            - **Drug effectiveness**: Clinical trial analysis
            
            **🧬 Biological Measurements:**
            - **Birth weights**: Identifying at-risk infants
            - **Height and weight**: Growth charts and percentiles
            - **Reaction times**: Neurological assessments
            - **Heart rate variability**: Cardiovascular health
            """)
        
        with col2:
            st.markdown("""
            **🧪 Laboratory Testing:**
            - **Reference ranges**: Establishing normal vs abnormal values
            - **Quality control**: Ensuring test accuracy
            - **Diagnostic thresholds**: Setting cutoff points
            - **Population screening**: Identifying health trends
            
            **📊 Epidemiology:**
            - **Disease incidence**: Tracking outbreak patterns
            - **Treatment outcomes**: Measuring intervention success
            - **Risk factors**: Identifying population vulnerabilities
            - **Vaccine efficacy**: Clinical trial analysis
            """)
    
    with tab2:
        st.subheader("Business & Economics Applications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **💰 Financial Markets:**
            - **Stock returns**: Risk assessment and portfolio management
            - **Currency fluctuations**: Exchange rate modeling
            - **Credit scores**: Loan approval and risk pricing
            - **Insurance claims**: Premium calculation and reserves
            
            **📊 Quality Control:**
            - **Manufacturing tolerances**: Product specification limits
            - **Service times**: Customer satisfaction metrics
            - **Error rates**: Process improvement initiatives
            - **Employee performance**: Evaluation and benchmarking
            """)
        
        with col2:
            st.markdown("""
            **🛒 Market Research:**
            - **Consumer spending**: Purchasing behavior analysis
            - **Survey responses**: Opinion polling and market studies
            - **Product ratings**: Customer satisfaction measurement
            - **Sales forecasting**: Demand prediction models
            
            **📈 Operations Research:**
            - **Wait times**: Queue management and staffing
            - **Inventory levels**: Supply chain optimization
            - **Demand variability**: Production planning
            - **Resource allocation**: Efficiency maximization
            """)
    
    with tab3:
        st.subheader("Science & Research Applications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔬 Experimental Science:**
            - **Measurement errors**: Instrument calibration and precision
            - **Hypothesis testing**: Statistical significance determination
            - **Sample means**: Central limit theorem applications
            - **Data analysis**: Identifying outliers and patterns
            
            **🌡️ Environmental Science:**
            - **Temperature variations**: Climate change analysis
            - **Pollution levels**: Environmental monitoring
            - **Species populations**: Ecological modeling
            - **Weather patterns**: Meteorological predictions
            """)
        
        with col2:
            st.markdown("""
            **🧬 Research Methods:**
            - **Sample size calculation**: Study design and power analysis
            - **Confidence intervals**: Parameter estimation
            - **Regression analysis**: Relationship modeling
            - **Meta-analysis**: Combining multiple studies
            
            **🔭 Physical Sciences:**
            - **Quantum mechanics**: Probability distributions
            - **Thermal physics**: Molecular motion and energy
            - **Astronomy**: Star brightness and distance measurements
            - **Engineering**: Signal processing and noise analysis
            """)
    
    with tab4:
        st.subheader("Education & Testing Applications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📝 Standardized Testing:**
            - **SAT/ACT scores**: College admissions and comparisons
            - **IQ testing**: Intelligence measurement and interpretation
            - **Achievement tests**: Academic performance assessment
            - **Professional exams**: Certification and licensing
            
            **📊 Educational Assessment:**
            - **Grade distributions**: Course difficulty and fairness
            - **Test item analysis**: Question validity and reliability
            - **Student performance**: Progress monitoring and intervention
            - **School comparisons**: Accountability and improvement
            """)
        
        with col2:
            st.markdown("""
            **🎯 Psychometrics:**
            - **Personality testing**: Psychological assessment tools
            - **Aptitude tests**: Career guidance and selection
            - **Survey research**: Social science data collection
            - **Program evaluation**: Effectiveness measurement
            
            **📈 Data-Driven Decisions:**
            - **Admissions criteria**: Selection and placement
            - **Resource allocation**: Budget and staffing decisions
            - **Curriculum development**: Content and pacing guides
            - **Teacher evaluation**: Performance measurement systems
            """)

elif section == "📝 Problem Solving":
    st.header("📝 Real-World Problem Solving")
    
    problem_type = st.selectbox("Choose a problem category:", [
        "🏥 Medical Diagnosis", 
        "📊 Quality Control", 
        "📈 Financial Analysis", 
        "🎓 Educational Assessment"
    ])
    
    if problem_type == "🏥 Medical Diagnosis":
        st.subheader("Medical Reference Ranges")
        
        st.markdown("""
        **Problem:** A medical laboratory establishes reference ranges for cholesterol levels. In a healthy population,
        total cholesterol follows a normal distribution with mean 190 mg/dL and standard deviation 35 mg/dL.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Given Information:**
            - Population: Healthy adults
            - Mean cholesterol: 190 mg/dL
            - Standard deviation: 35 mg/dL
            - Distribution: Normal
            """)
            
            # Interactive parameters
            mu_chol = st.slider("Mean cholesterol (mg/dL)", 150, 250, 190)
            sigma_chol = st.slider("Standard deviation (mg/dL)", 20, 50, 35)
            
            # Calculate key values
            low_normal = mu_chol - 2*sigma_chol
            high_normal = mu_chol + 2*sigma_chol
            
            st.markdown(f"""
            **Calculated Reference Ranges:**
            - Normal range (±2σ): {low_normal:.0f} - {high_normal:.0f} mg/dL
            - Borderline high (>1σ): >{mu_chol + sigma_chol:.0f} mg/dL
            - High risk (>2σ): >{high_normal:.0f} mg/dL
            
            **Clinical Interpretation:**
            - 95% of healthy people: {low_normal:.0f} - {high_normal:.0f} mg/dL
            - 2.5% have levels > {high_normal:.0f} mg/dL
            - 2.5% have levels < {low_normal:.0f} mg/dL
            """)
        
        with col2:
            # Plot cholesterol distribution
            x = np.linspace(mu_chol - 4*sigma_chol, mu_chol + 4*sigma_chol, 1000)
            y = stats.norm.pdf(x, mu_chol, sigma_chol)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Color different regions
            ax.fill_between(x, y, alpha=0.3, color='green', label='Normal range')
            
            # Highlight risk zones
            x_high = x[x > high_normal]
            y_high = stats.norm.pdf(x_high, mu_chol, sigma_chol)
            ax.fill_between(x_high, y_high, alpha=0.6, color='red', label='High risk')
            
            x_low = x[x < low_normal]
            y_low = stats.norm.pdf(x_low, mu_chol, sigma_chol)
            ax.fill_between(x_low, y_low, alpha=0.6, color='orange', label='Low (unusual)')
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.axvline(mu_chol, color='black', linestyle='-', linewidth=2, label=f'Mean ({mu_chol})')
            ax.axvline(high_normal, color='red', linestyle='--', label=f'High threshold ({high_normal:.0f})')
            ax.axvline(low_normal, color='orange', linestyle='--', label=f'Low threshold ({low_normal:.0f})')
            
            ax.set_xlabel('Cholesterol Level (mg/dL)')
            ax.set_ylabel('Probability Density')
            ax.set_title('Cholesterol Distribution and Reference Ranges')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
    
    elif problem_type == "📊 Quality Control":
        st.subheader("Manufacturing Quality Control")
        
        st.markdown("""
        **Problem:** A factory produces bolts with a target diameter of 10.00 mm. The manufacturing process
        has natural variation with standard deviation 0.15 mm. Bolts outside ±0.30 mm are rejected.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            target_diameter = st.slider("Target diameter (mm)", 9.5, 10.5, 10.0, 0.01)
            process_std = st.slider("Process std dev (mm)", 0.05, 0.25, 0.15, 0.01)
            tolerance = st.slider("Tolerance (±mm)", 0.1, 0.5, 0.3, 0.01)
            
            # Calculate quality metrics
            lower_spec = target_diameter - tolerance
            upper_spec = target_diameter + tolerance
            
            # Calculate probabilities
            p_reject_low = stats.norm.cdf(lower_spec, target_diameter, process_std)
            p_reject_high = 1 - stats.norm.cdf(upper_spec, target_diameter, process_std)
            p_reject_total = p_reject_low + p_reject_high
            p_accept = 1 - p_reject_total
            
            st.markdown(f"""
            **Quality Specifications:**
            - Target: {target_diameter:.2f} mm
            - Tolerance: ±{tolerance:.2f} mm
            - Acceptable range: {lower_spec:.2f} - {upper_spec:.2f} mm
            
            **Process Performance:**
            - Acceptance rate: {p_accept*100:.1f}%
            - Rejection rate: {p_reject_total*100:.1f}%
            - Daily production (10,000 bolts): {int(p_accept*10000)} good, {int(p_reject_total*10000)} rejected
            
            **Cost Analysis:**
            - Material waste: {p_reject_total*100:.1f}%
            - Process capability: {'Good' if p_reject_total < 0.05 else 'Needs improvement'}
            """)
        
        with col2:
            # Plot quality control chart
            x = np.linspace(target_diameter - 4*process_std, target_diameter + 4*process_std, 1000)
            y = stats.norm.pdf(x, target_diameter, process_std)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Color regions
            x_good = x[(x >= lower_spec) & (x <= upper_spec)]
            y_good = stats.norm.pdf(x_good, target_diameter, process_std)
            ax.fill_between(x_good, y_good, alpha=0.4, color='green', label=f'Acceptable ({p_accept*100:.1f}%)')
            
            x_reject_low = x[x < lower_spec]
            y_reject_low = stats.norm.pdf(x_reject_low, target_diameter, process_std)
            ax.fill_between(x_reject_low, y_reject_low, alpha=0.6, color='red', label=f'Too small ({p_reject_low*100:.1f}%)')
            
            x_reject_high = x[x > upper_spec]
            y_reject_high = stats.norm.pdf(x_reject_high, target_diameter, process_std)
            ax.fill_between(x_reject_high, y_reject_high, alpha=0.6, color='red', label=f'Too large ({p_reject_high*100:.1f}%)')
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.axvline(target_diameter, color='black', linestyle='-', linewidth=2, label='Target')
            ax.axvline(lower_spec, color='red', linestyle='--', label='Lower limit')
            ax.axvline(upper_spec, color='red', linestyle='--', label='Upper limit')
            
            ax.set_xlabel('Bolt Diameter (mm)')
            ax.set_ylabel('Probability Density')
            ax.set_title('Quality Control Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
    
    elif problem_type == "📈 Financial Analysis":
        st.subheader("Investment Risk Analysis")
        
        st.markdown("""
        **Problem:** An investment portfolio has historically returned 8% annually with a standard deviation of 12%.
        An investor wants to understand the probability of different return scenarios.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            expected_return = st.slider("Expected annual return (%)", 0, 20, 8)
            volatility = st.slider("Volatility (std dev) (%)", 5, 25, 12)
            
            # Calculate probabilities for different scenarios
            prob_loss = stats.norm.cdf(0, expected_return, volatility) * 100
            prob_double_digit = (1 - stats.norm.cdf(10, expected_return, volatility)) * 100
            prob_large_loss = stats.norm.cdf(-20, expected_return, volatility) * 100
            
            # Value at Risk (5% probability of loss exceeding this amount)
            var_5 = stats.norm.ppf(0.05, expected_return, volatility)
            
            st.markdown(f"""
            **Risk Analysis:**
            - Expected return: {expected_return}%
            - Volatility: {volatility}%
            
            **Probability Scenarios:**
            - Loss (return < 0%): {prob_loss:.1f}%
            - Double-digit return (>10%): {prob_double_digit:.1f}%
            - Large loss (<-20%): {prob_large_loss:.1f}%
            
            **Risk Metrics:**
            - Value at Risk (5%): {var_5:.1f}%
            - 95% confident return will exceed: {var_5:.1f}%
            - Risk-return ratio: {expected_return/volatility:.2f}
            """)
        
        with col2:
            # Plot return distribution
            x = np.linspace(expected_return - 4*volatility, expected_return + 4*volatility, 1000)
            y = stats.norm.pdf(x, expected_return, volatility)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Color different return regions
            x_loss = x[x < 0]
            y_loss = stats.norm.pdf(x_loss, expected_return, volatility)
            ax.fill_between(x_loss, y_loss, alpha=0.6, color='red', label=f'Losses ({prob_loss:.1f}%)')
            
            x_modest = x[(x >= 0) & (x <= 10)]
            y_modest = stats.norm.pdf(x_modest, expected_return, volatility)
            ax.fill_between(x_modest, y_modest, alpha=0.4, color='yellow', label='Modest gains (0-10%)')
            
            x_good = x[x > 10]
            y_good = stats.norm.pdf(x_good, expected_return, volatility)
            ax.fill_between(x_good, y_good, alpha=0.4, color='green', label=f'Strong gains (>{prob_double_digit:.1f}%)')
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.axvline(expected_return, color='black', linestyle='-', linewidth=2, label=f'Expected ({expected_return}%)')
            ax.axvline(0, color='red', linestyle='--', label='Break-even')
            ax.axvline(var_5, color='purple', linestyle='--', label=f'VaR 5% ({var_5:.1f}%)')
            
            ax.set_xlabel('Annual Return (%)')
            ax.set_ylabel('Probability Density')
            ax.set_title('Investment Return Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
    
    elif problem_type == "🎓 Educational Assessment":
        st.subheader("Standardized Test Analysis")
        
        st.markdown("""
        **Problem:** The SAT Math section has a mean score of 528 with a standard deviation of 117.
        A college wants to analyze admission criteria and student performance.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            sat_mean = st.slider("SAT Math Mean", 400, 600, 528)
            sat_std = st.slider("SAT Math Std Dev", 80, 150, 117)
            admission_cutoff = st.slider("College admission cutoff", 400, 700, 600)
            
            # Calculate percentiles and probabilities
            percentile_cutoff = stats.norm.cdf(admission_cutoff, sat_mean, sat_std) * 100
            prob_qualify = (1 - stats.norm.cdf(admission_cutoff, sat_mean, sat_std)) * 100
            
            # Calculate score ranges
            score_25th = stats.norm.ppf(0.25, sat_mean, sat_std)
            score_75th = stats.norm.ppf(0.75, sat_mean, sat_std)
            score_90th = stats.norm.ppf(0.90, sat_mean, sat_std)
            
            st.markdown(f"""
            **Test Statistics:**
            - Mean score: {sat_mean}
            - Standard deviation: {sat_std}
            - Admission cutoff: {admission_cutoff}
            
            **Admission Analysis:**
            - Students qualifying: {prob_qualify:.1f}%
            - Cutoff percentile: {percentile_cutoff:.1f}th
            - Selectivity level: {'Highly selective' if prob_qualify < 25 else 'Moderately selective' if prob_qualify < 50 else 'Less selective'}
            
            **Score Benchmarks:**
            - 25th percentile: {score_25th:.0f}
            - 75th percentile: {score_75th:.0f}
            - 90th percentile: {score_90th:.0f}
            """)
        
        with col2:
            # Plot SAT score distribution
            x = np.linspace(sat_mean - 4*sat_std, sat_mean + 4*sat_std, 1000)
            y = stats.norm.pdf(x, sat_mean, sat_std)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Color admission regions
            x_qualify = x[x >= admission_cutoff]
            y_qualify = stats.norm.pdf(x_qualify, sat_mean, sat_std)
            ax.fill_between(x_qualify, y_qualify, alpha=0.4, color='green', label=f'Qualify ({prob_qualify:.1f}%)')
            
            x_not_qualify = x[x < admission_cutoff]
            y_not_qualify = stats.norm.pdf(x_not_qualify, sat_mean, sat_std)
            ax.fill_between(x_not_qualify, y_not_qualify, alpha=0.4, color='lightcoral', label=f'Below cutoff ({100-prob_qualify:.1f}%)')
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.axvline(sat_mean, color='black', linestyle='-', linewidth=2, label=f'Mean ({sat_mean})')
            ax.axvline(admission_cutoff, color='red', linestyle='--', linewidth=2, label=f'Cutoff ({admission_cutoff})')
            ax.axvline(score_75th, color='orange', linestyle=':', label=f'75th percentile ({score_75th:.0f})')
            
            ax.set_xlabel('SAT Math Score')
            ax.set_ylabel('Probability Density')
            ax.set_title('SAT Score Distribution and Admission Criteria')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)

elif section == "🧪 Hypothesis Testing":
    st.header("🧪 Hypothesis Testing with Normal Distribution")
    
    st.markdown("""
    **Learn how the normal distribution is used in statistical hypothesis testing!**
    This section demonstrates how researchers use normal distributions to make decisions about populations.
    """)
    
    test_type = st.selectbox("Choose a hypothesis test:", [
        "One-sample z-test",
        "Two-sample comparison", 
        "Quality control testing",
        "Clinical trial analysis"
    ])
    
    if test_type == "One-sample z-test":
        st.subheader("One-Sample Z-Test")
        
        st.markdown("""
        **Scenario:** A manufacturer claims their light bulbs last 1000 hours on average. 
        We test a sample of bulbs to verify this claim.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            # Test parameters
            claimed_mean = st.slider("Claimed mean (hours)", 800, 1200, 1000)
            population_std = st.slider("Known std dev (hours)", 50, 200, 100)
            sample_size = st.slider("Sample size", 10, 100, 36)
            sample_mean = st.slider("Sample mean (hours)", 800, 1200, 950)
            alpha = st.selectbox("Significance level (α)", [0.01, 0.05, 0.10], index=1)
            
            # Calculate test statistic and p-value
            standard_error = population_std / math.sqrt(sample_size)
            z_score = (sample_mean - claimed_mean) / standard_error
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # Two-tailed test
            
            # Critical values
            z_critical = stats.norm.ppf(1 - alpha/2)
            
            # Decision
            reject_null = abs(z_score) > z_critical
            
            st.markdown(f"""
            **Hypothesis Test:**
            - H₀: μ = {claimed_mean} hours
            - H₁: μ ≠ {claimed_mean} hours
            - α = {alpha}
            
            **Test Results:**
            - Sample mean: {sample_mean} hours
            - Standard error: {standard_error:.2f}
            - Z-score: {z_score:.3f}
            - P-value: {p_value:.4f}
            - Critical value: ±{z_critical:.3f}
            
            **Decision:**
            - {'Reject' if reject_null else 'Fail to reject'} the null hypothesis
            - Evidence: {'Significant' if reject_null else 'Not significant'} at α = {alpha}
            - Conclusion: {'The claim is likely false' if reject_null else 'Insufficient evidence against the claim'}
            """)
        
        with col2:
            # Plot hypothesis test
            x = np.linspace(-4, 4, 1000)
            y = stats.norm.pdf(x, 0, 1)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot standard normal
            ax.plot(x, y, 'b-', linewidth=2, label='Standard Normal (H₀ true)')
            
            # Shade critical regions
            x_left = x[x < -z_critical]
            y_left = stats.norm.pdf(x_left, 0, 1)
            ax.fill_between(x_left, y_left, alpha=0.3, color='red', label=f'Critical region (α/2 = {alpha/2})')
            
            x_right = x[x > z_critical]
            y_right = stats.norm.pdf(x_right, 0, 1)
            ax.fill_between(x_right, y_right, alpha=0.3, color='red')
            
            # Mark test statistic
            ax.axvline(z_score, color='green', linestyle='--', linewidth=3, label=f'Test statistic (z = {z_score:.3f})')
            ax.axvline(-z_critical, color='red', linestyle=':', label=f'Critical values (±{z_critical:.3f})')
            ax.axvline(z_critical, color='red', linestyle=':')
            
            ax.set_xlabel('Z-score')
            ax.set_ylabel('Probability Density')
            ax.set_title('Hypothesis Test Visualization')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)

# Educational Standards and Resources Section
st.markdown("---")
st.header("📋 Educational Standards & Cognitive Development")

# Common Core Standards breakdown
with st.expander("📚 Common Core Standards Alignment"):
    st.markdown("""
    ### High School Statistics & Probability Standards:
    
    **S-ID (Interpreting Categorical and Quantitative Data):**
    - S-ID.A.4: Use the mean and standard deviation of a data set to fit it to a normal distribution
    - S-ID.B.6: Represent data on two quantitative variables and describe the relationship
    
    **S-IC (Making Inferences and Justifying Conclusions):**
    - S-IC.A.1: Understand statistics as a process for making inferences about population parameters
    - S-IC.A.2: Decide if a specified model is consistent with results from a given data-generating process
    - S-IC.B.4: Use data from a sample survey to estimate a population mean or proportion
    - S-IC.B.5: Use data from a randomized experiment to compare two treatments
    
    **A-CED (Creating Equations):**
    - A-CED.A.3: Represent constraints by systems of equations and interpret solutions
    
    **F-IF (Interpreting Functions):**
    - F-IF.C.7: Graph functions expressed symbolically and show key features
    - F-IF.B.4: Interpret key features of graphs and tables in context
    
    **Mathematical Practices:**
    - MP1: Make sense of problems and persevere in solving them
    - MP2: Reason abstractly and quantitatively  
    - MP3: Construct viable arguments and critique reasoning of others
    - MP4: Model with mathematics
    - MP5: Use appropriate tools strategically
    - MP6: Attend to precision
    - MP7: Look for and make use of structure
    - MP8: Look for and express regularity in repeated reasoning
    """)

# Cognitive Abilities Development
with st.expander("🧠 Cognitive Abilities Development"):
    st.markdown("""
    ### Statistical Reasoning:
    - **Probabilistic Thinking**: Understanding uncertainty and likelihood in real-world contexts
    - **Distribution Concepts**: Visualizing how data spreads around central tendencies
    - **Parameter Relationships**: Connecting mathematical parameters to real-world meanings
    
    ### Logical-Mathematical Intelligence:
    - **Pattern Recognition**: Identifying normal distribution patterns in diverse contexts
    - **Proportional Reasoning**: Understanding percentiles, z-scores, and standardization
    - **Algebraic Manipulation**: Working with formulas for mean, standard deviation, and probability
    
    ### Critical Thinking Skills:
    - **Hypothesis Evaluation**: Testing claims using statistical evidence
    - **Data Interpretation**: Drawing valid conclusions from statistical analyses
    - **Model Validation**: Assessing whether normal distribution assumptions are reasonable
    
    ### Problem-Solving Strategies:
    - **Statistical Modeling**: Applying normal distribution to real-world problems
    - **Decision Making**: Using probability to inform choices under uncertainty
    - **Quality Assessment**: Evaluating processes and outcomes using statistical criteria
    
    ### Spatial and Visual Intelligence:
    - **Graph Interpretation**: Reading and analyzing distribution curves and areas
    - **Parameter Visualization**: Understanding how μ and σ affect curve shape and position
    - **Area Relationships**: Connecting geometric areas to probability concepts
    
    ### Executive Function Development:
    - **Multi-step Problem Solving**: Following complex statistical procedures
    - **Attention to Detail**: Precision in calculations and interpretations
    - **Working Memory**: Managing multiple statistical concepts simultaneously
    """)

# Educational Resource Links
with st.expander("🔗 Educational Resources & Practice"):
    st.markdown("""
    ### Khan Academy Resources:
    
    **Normal Distribution Foundation:**
    - [Introduction to Normal Distribution](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/introduction-to-the-normal-distribution)
    - [Empirical Rule (68-95-99.7)](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/ck12-the-empirical-rule)
    - [Standard Normal Distribution](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/standard-normal-distribution-and-the-empirical-rule)
    - [Z-scores and Percentiles](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/z-scores/v/z-score-introduction)
    
    **Advanced Applications:**
    - [Normal Distribution Problems](https://www.khanacademy.org/math/statistics-probability/modeling-distributions-of-data/normal-distributions-library/v/qualitative-sense-of-normal-distributions)
    - [Central Limit Theorem](https://www.khanacademy.org/math/statistics-probability/sampling-distributions-library/sample-means/v/central-limit-theorem)
    - [Hypothesis Testing](https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample/idea-of-significance-tests/v/simple-hypothesis-testing)
    
    ### IXL Practice Modules:
    
    **Algebra 2 Level:**
    - [Identify Normal Distributions](https://www.ixl.com/math/algebra-2/identify-normal-distributions)
    - [Find Values Using Normal Distribution](https://www.ixl.com/math/algebra-2/find-values-using-normal-distributions)
    - [Calculate Z-scores](https://www.ixl.com/math/algebra-2/calculate-z-scores)
    - [Use Empirical Rule](https://www.ixl.com/math/algebra-2/use-normal-distributions-to-approximate-binomial-distributions)
    
    **Statistics Level:**
    - [Normal Distribution Applications](https://www.ixl.com/math/statistics/normal-distribution-calculations)
    - [Confidence Intervals](https://www.ixl.com/math/statistics/confidence-intervals-for-the-mean-sigma-known)
    - [Hypothesis Testing](https://www.ixl.com/math/statistics/test-a-claim-about-a-mean-sigma-known)
    - [Sample Size Calculations](https://www.ixl.com/math/statistics/find-the-sample-size-needed-to-estimate-a-population-mean)
    
    ### Additional Online Resources:
    - **Desmos Graphing Calculator**: Interactive normal distribution exploration
    - **GeoGebra Statistics**: Dynamic probability and statistics simulations
    - **StatCrunch**: Real data analysis and hypothesis testing
    - **Wolfram Alpha**: Statistical calculations and probability computations
    - **PhET Simulations**: Plinko Probability for hands-on normal distribution
    """)

# Assessment and Progress Tracking
with st.expander("📊 Assessment & Progress Tracking"):
    st.markdown("""
    ### Formative Assessment Strategies:
    - **Parameter Prediction**: Guess μ and σ from graph appearance before calculating
    - **Real-Data Collection**: Measure class data and test for normality
    - **Probability Estimation**: Estimate areas before using calculators
    - **Conjecture Testing**: Use interactive tools to verify/disprove statistical claims
    
    ### Summative Assessment Options:
    - **Case Study Projects**: Apply normal distribution to student-chosen real-world context
    - **Statistical Consulting**: Role-play as statistician solving business/medical problems
    - **Data Analysis Portfolio**: Collection of normal distribution applications across subjects
    - **Hypothesis Testing Lab**: Design and conduct original statistical investigations
    
    ### Differentiation Strategies:
    - **Visual Learners**: Graphical emphasis, color-coded regions, area comparisons
    - **Kinesthetic Learners**: Physical manipulatives, data collection, simulation activities
    - **Analytical Learners**: Formula derivations, mathematical proofs, computational focus
    - **Creative Learners**: Real-world connections, story problems, cross-curricular applications
    - **English Language Learners**: Visual supports, bilingual statistical glossaries
    
    ### Technology Integration:
    - **Spreadsheet Skills**: Excel/Google Sheets for statistical calculations
    - **Programming Introduction**: Python/R for advanced statistical analysis
    - **Online Simulations**: Interactive probability demonstrations
    - **Graphing Calculator**: Ti-84 statistical functions and applications
    """)

st.markdown("---")
st.markdown("""
### 🎯 Learning Extensions:
- **Collect Real Data**: Measure heights, test scores, or reaction times to create actual normal distributions
- **Research Applications**: Investigate how normal distribution is used in your career interest area
- **Statistical Software**: Learn Excel, R, or Python for advanced statistical analysis
- **Historical Context**: Study the contributions of Gauss, Pearson, and other statistical pioneers
- **Cross-Curricular Connections**: Apply normal distribution concepts in science labs and social studies research

*MathCraft modules are designed to meet rigorous academic standards while fostering deep conceptual understanding through hands-on exploration and real-world applications.*
""")
