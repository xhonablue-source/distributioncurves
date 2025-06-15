import streamlit as st
import numpy as np
import math

# Configure matplotlib for Streamlit - moved before other matplotlib imports
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Import other libraries
from scipy import stats
import pandas as pd

# Set page config first
st.set_page_config(page_title="MathCraft | Normal Distribution", layout="wide")

# Clear any existing matplotlib configurations and set a clean style
plt.style.use('default')
plt.rcParams.update({'figure.max_open_warning': 0})

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
    | Probability Density Function | Formula for the curve | f(x) = (1/(σ√(2π))) × e^(-½((x-μ)/σ)²) |
    | Standard Normal | Special case with μ=0, σ=1 | Z ~ N(0,1) |
    """)
    
    # Create a basic normal distribution plot
    try:
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
        plt.close(fig)  # Close figure to prevent memory issues
    except Exception as e:
        st.error(f"Error creating plot: {e}")

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
        try:
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
            plt.close(fig)  # Close figure to prevent memory issues
        except Exception as e:
            st.error(f"Error creating plot: {e}")
    
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
            try:
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
                plt.close(fig)
            except Exception as e:
                st.error(f"Error creating plot: {e}")

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
            try:
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
                plt.close(fig)
            except Exception as e:
                st.error(f"Error creating plot: {e}")

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
    -
