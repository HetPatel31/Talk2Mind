class QuestionnaireAssessment:
    """
    Talk2Mind Questionnaire Assessment Module

    Components:
    - PHQ-9 (Depression)
    - GAD-7 (Anxiety)
    - Sleep Assessment
    - Lifestyle Assessment
    - Mental Wellness Score
    """

    def __init__(self):

        # -------------------------
        # PHQ-9 Depression Questions
        # -------------------------
        self.phq9_questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself",
            "Trouble concentrating on things",
            "Moving or speaking slowly or being restless",
            "Thoughts that you would be better off dead or hurting yourself"
        ]

        # -------------------------
        # GAD-7 Anxiety Questions
        # -------------------------
        self.gad7_questions = [
            "Feeling nervous, anxious or on edge",
            "Not being able to stop worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it is hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid as if something awful might happen"
        ]

        # -------------------------
        # Sleep Assessment
        # -------------------------
        self.sleep_questions = [
            "How many hours do you sleep on average?",
            "Do you wake up feeling refreshed?",
            "Do you have difficulty falling asleep?"
        ]

        # -------------------------
        # Lifestyle Assessment
        # -------------------------
        self.lifestyle_questions = [
            "How often do you exercise?",
            "How often do you socialize with friends or family?",
            "How stressed do you feel during a typical week?"
        ]

    # ======================================
    # PHQ-9
    # ======================================

    def calculate_phq9_score(self, responses):

        if len(responses) != 9:
            raise ValueError("PHQ-9 requires exactly 9 responses.")

        return sum(responses)

    def get_depression_level(self, score):

        if score <= 4:
            return "Minimal"

        elif score <= 9:
            return "Mild"

        elif score <= 14:
            return "Moderate"

        elif score <= 19:
            return "Moderately Severe"

        return "Severe"

    # ======================================
    # GAD-7
    # ======================================

    def calculate_gad7_score(self, responses):

        if len(responses) != 7:
            raise ValueError("GAD-7 requires exactly 7 responses.")

        return sum(responses)

    def get_anxiety_level(self, score):

        if score <= 4:
            return "Minimal"

        elif score <= 9:
            return "Mild"

        elif score <= 14:
            return "Moderate"

        return "Severe"

    # ======================================
    # Sleep Assessment
    # ======================================

    def calculate_sleep_score(self, sleep_hours,
                              refreshed_score,
                              difficulty_score):

        score = 100

        if sleep_hours < 6:
            score -= 30

        elif sleep_hours < 7:
            score -= 15

        score -= difficulty_score * 10
        score += refreshed_score * 5

        return max(0, min(score, 100))

    # ======================================
    # Lifestyle Assessment
    # ======================================

    def calculate_lifestyle_score(self,
                                  exercise_score,
                                  social_score,
                                  stress_score):

        score = (
            exercise_score * 10 +
            social_score * 10 +
            (10 - stress_score) * 10
        )

        return max(0, min(score, 100))

    # ======================================
    # Wellness Score
    # ======================================

    def calculate_wellness_score(self,
                                 depression_score,
                                 anxiety_score,
                                 sleep_score=80,
                                 lifestyle_score=80):

        score = 100

        score -= depression_score * 2
        score -= anxiety_score * 2

        score += (sleep_score - 50) * 0.2
        score += (lifestyle_score - 50) * 0.2

        return round(max(0, min(score, 100)), 2)

    # ======================================
    # Risk Level
    # ======================================

    def get_risk_level(self, wellness_score):

        if wellness_score >= 80:
            return "Low Risk"

        elif wellness_score >= 60:
            return "Moderate Risk"

        elif wellness_score >= 40:
            return "High Risk"

        return "Critical Risk"

    # ======================================
    # Complete Assessment
    # ======================================

    def generate_assessment(self,
                            phq_responses,
                            gad_responses,
                            sleep_score=80,
                            lifestyle_score=80):

        depression_score = self.calculate_phq9_score(phq_responses)
        anxiety_score = self.calculate_gad7_score(gad_responses)

        wellness_score = self.calculate_wellness_score(
            depression_score,
            anxiety_score,
            sleep_score,
            lifestyle_score
        )

        return {
            "depression_score": depression_score,
            "depression_level": self.get_depression_level(depression_score),

            "anxiety_score": anxiety_score,
            "anxiety_level": self.get_anxiety_level(anxiety_score),

            "sleep_score": sleep_score,
            "lifestyle_score": lifestyle_score,

            "wellness_score": wellness_score,
            "risk_level": self.get_risk_level(wellness_score)
        }