from app.forms import PortfolioGenerationForm, PortfolioReviewForm


def portfolio_generation_user_query(form: PortfolioGenerationForm):
    return f"""
   Create an Indian mutual fund portfolio based on:
   Age: {form.age}
   Risk Profile: {form.risk_level}
   Investment Horizon: {form.investment_horizon} years
   Monthly Investment: ₹{form.monthly_investment}
   Financial Goal: {form.investment_goal}

   STRICT REQUIREMENTS - FOLLOW ALL RULES:
   1. FUND ELIGIBILITY:
      - Only Direct Growth plans of mutual funds
      - Minimum AUM: ₹1000 crores (₹10 billion) or higher
      - Track record: At least 3 years
      - Should be consistently outperforming its benchmark index in 1Y, 3Y, 5Y, 10Y, Since inception
      - Fund manager experience: At least 5 years

   2. PORTFOLIO SIZE:
      - For Emergency fund, House downpayment: Maximum 2-3 funds
      - For other goals: 3-5 funds based on strategy

   INDEX FUND RULES - CRITICAL:
   1. NO index funds in mid-cap or small-cap categories
   2. For large-cap category:
      - If suggesting active large-cap fund, DO NOT include Nifty/Sensex index funds
      - Choose either active management OR index funds, not both
      - Prefer active funds with proven outperformance

   INVESTMENT HORIZON RULES - STRICTLY FOLLOW:
   1. For investment horizon < 5 years:
      - NO small-cap funds
      - NO mid-cap funds
      - Focus on large-cap/flexi-cap (choose one type only) and debt funds
      - Can allocate intenaional funds (max 10% allocation)
   2. For investment horizon > 7 years:
      - Can include small-cap (max 20% allocation)
      - Can include mid-cap (max 30% allocation)
      - Can allocate intenational funds (max 10% allocation)

   Goal-Specific Guidelines:
   - Emergency Fund: Focus on liquid and ultra-short term funds and arbitrage funds
   - House Downpayment: Balance between safety and moderate returns
   - Financial Freedom: Focus on long-term wealth creation
   - Random Investing Portfolio: Focus on long-term wealth creation

   Provide output in this exact JSON format:
   {{
       "portfolio": [
           {{
               "name": "Fund Name",
               "allocation": 50,
               "category": "Fund Category",
               "rationale": "Investment rationale"
           }}
       ],
       "strategy": "Overall investment strategy",
       "risk_analysis": "Risk analysis details"
   }}
   """


def portfolio_generation_system_prompt():
    return """
   You are an expert Indian mutual fund advisor.
   CRITICAL RULES:
   1. Only recommend Direct Growth plan funds
   2. NEVER mix Flexi-cap and Large-cap funds in same portfolio
   3. No duplicate fund catgories in same portfolio
   4. No small/mid-cap funds for < 5 year horizon
   5. No index funds in mid/small-cap categories
   6. Don't mix active large-cap and index funds
   """


def portfolio_review_user_query(form: PortfolioReviewForm):
    formatted_funds = "\n".join(
        [
            f"- Fund: {fund['name']}, Amount: ₹{fund['amount']:,.2f}"
            for fund in form.funds
        ]
    )
    total_investment = sum(fund.amount for fund in form.funds)

    allocations = []
    for fund in form.funds:
        allocations.append((fund.amount / total_investment) * 100)
    formatted_allocations = "\n".join(
        [f"- {fund['name']}: {fund['allocation']:.1f}%" for fund in form.funds]
    )

    return f"""
   Please review this Indian mutual fund portfolio and provide recommendations following these strict criteria:
   Investor Details:
   - Age: {form.age}
   - Risk Profile: {form.risk_level}
   - Investment Horizon: {form.investment_horizon} years

   Current Portfolio:
   Total Investment: ₹{total_investment:,.2f}

   Fund Details:
   {form.funds}

   Current Allocations:
   {formatted_allocations}

   Portfolio Construction Rules:
   1. Maximum 5 funds in total portfolio, follow this strict rule
   2. Each fund must have a different investment strategy (value, growth, momentum, blend)
   3. Avoid multiple funds with the same strategy
   4. Diversify across different fund houses
   5. Add intenational funds (max 10%)

   New Fund Selection Criteria:
   1. Minimum 5-year track record required
   2. Must consistently outperform its benchmark across all periods:
      - 1-year returns
      - 3-year returns
      - 5-year returns
      - 10-year returns (if applicable)
   3. Proven strategy alignment with stated investment style

   Please analyze this portfolio considering:
   1. Risk profile alignment
   2. Investment horizon suitability
   3. Portfolio diversification
   4. AMC concentration
   5. Fund category overlap
   6. Strategy diversification
   7. Any potential rebalancing needs

   Important: When suggesting new funds, recommend ONLY specific funds that:
   - Have at least 5 years of track record
   - Consistently outperform their benchmark
   - Follow a unique investment strategy not already present in the portfolio
   - Come from different fund houses when possible
   - Suggested portfolio should have only one fund from the cateogry

   Provide output in this exact JSON format:
   {{
       "portfolio_analysis": {{
           "strengths": ["List of portfolio strengths"],
           "concerns": ["List of potential issues"],
           "risk_alignment": "Analysis of risk profile alignment",
           "horizon_alignment": "Analysis of investment horizon alignment"
       }},
       "rebalancing_suggestions": {{
           "funds_to_reduce": [
               {{
                   "fund_name": "Fund to reduce",
                   "current_allocation": 50,
                   "suggested_allocation": 30,
                   "rationale": "Why reduce"
               }}
           ],
           "funds_to_increase": [
               {{
                   "fund_name": "Fund to increase",
                   "current_allocation": 20,
                   "suggested_allocation": 40,
                   "rationale": "Why increase"
               }}
           ],
           "funds_to_exit": [
               {{
                   "fund_name": "Fund to exit",
                   "rationale": "Why exit"
               }}
           ],
           "new_fund_suggestions": [
               {{
                   "fund_name": "Specific fund name with proven track record",
                   "category": "Fund category",
                   "strategy": "Investment strategy (value/growth/momentum/blend)",
                   "allocation": 20,
                   "rationale": "Why add this specific fund, including its performance history and benchmark comparison"
               }}
           ]
       }},
       "overall_recommendation": "Summary of key actions needed"
   }}
"""


def portfolio_review_system_prompt():
    return "You are an expert Indian mutual fund portfolio analyst. Provide comprehensive analysis and actionable recommendations, including specific fund names from top-rated mutual funds when suggesting new investments. Ensure all suggested funds have at least 5 years of track record and consistent benchmark outperformance."
