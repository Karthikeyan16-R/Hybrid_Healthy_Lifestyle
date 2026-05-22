# app/ai_core/pdf_report_generator.py
from datetime import datetime, timedelta
from typing import Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
import os

class HealthReportGenerator:
    """Generate beautiful PDF reports for health tracking"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a7f72'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#166259'),
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            spaceAfter=12
        ))
    
    def generate_weekly_report(
        self,
        user_name: str,
        dashboard_data: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate weekly health report PDF
        
        Args:
            user_name: User's name
            dashboard_data: Health dashboard data
            output_path: Optional path to save PDF (if None, generates in memory)
            
        Returns:
            Path to generated PDF or BytesIO object
        """
        
        # Setup PDF
        if output_path is None:
            output_path = f"health_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        
        # Header
        elements.append(Paragraph(
            "🏥 Health Progress Report",
            self.styles['CustomTitle']
        ))
        
        elements.append(Paragraph(
            f"<b>User:</b> {user_name}",
            self.styles['CustomBody']
        ))
        
        elements.append(Paragraph(
            f"<b>Report Period:</b> {dashboard_data.get('period', 'Last 7 Days')}",
            self.styles['CustomBody']
        ))
        
        elements.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['CustomBody']
        ))
        
        elements.append(Spacer(1, 20))
        
        # Summary section
        elements.append(Paragraph("📊 Weekly Summary", self.styles['CustomSubtitle']))
        
        summary = dashboard_data.get('summary', {})
        
        # Nutrition summary
        nutrition = summary.get('nutrition', {})
        elements.append(Paragraph("<b>🍽️ Nutrition</b>", self.styles['CustomBody']))
        
        nutrition_data = [
            ['Metric', 'Value', 'Target'],
            ['Average Daily Calories', 
             f"{nutrition.get('avg_daily_calories', 0)} kcal",
             f"{nutrition.get('target', 2000)} kcal"],
            ['Average Daily Protein', 
             f"{nutrition.get('avg_daily_protein', 0)}g",
             f"{nutrition.get('protein_target', 150)}g"],
            ['Days Tracked', 
             str(nutrition.get('days_tracked', 0)),
             '7 days']
        ]
        
        nutrition_table = Table(nutrition_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        nutrition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a7f72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fefc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d3ebe3'))
        ]))
        
        elements.append(nutrition_table)
        elements.append(Spacer(1, 15))
        
        # Fitness summary
        fitness = summary.get('fitness', {})
        elements.append(Paragraph("<b>💪 Fitness & Exercise</b>", self.styles['CustomBody']))
        
        fitness_data = [
            ['Metric', 'Value', 'Goal'],
            ['Total Workouts', 
             str(fitness.get('total_workouts', 0)),
             '5 per week'],
            ['Total Duration', 
             f"{fitness.get('total_duration_minutes', 0)} minutes",
             '150 min/week'],
            ['Workout Frequency', 
             f"{fitness.get('workout_frequency', 0):.1f} days/week",
             '5 days/week']
        ]
        
        fitness_table = Table(fitness_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        fitness_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b35')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fff5f2')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffe5dc'))
        ]))
        
        elements.append(fitness_table)
        elements.append(Spacer(1, 15))
        
        # Sleep summary
        sleep = summary.get('sleep', {})
        elements.append(Paragraph("<b>😴 Sleep Quality</b>", self.styles['CustomBody']))
        
        sleep_data = [
            ['Metric', 'Value', 'Target'],
            ['Average Hours', 
             f"{sleep.get('avg_hours', 0)} hours",
             f"{sleep.get('target_hours', 7.5)} hours"],
            ['Days Tracked', 
             str(sleep.get('days_tracked', 0)),
             '7 days'],
            ['Sleep Quality', 
             'Good' if sleep.get('avg_hours', 0) >= 7 else 'Needs Improvement',
             'Good']
        ]
        
        sleep_table = Table(sleep_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        sleep_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a69bd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f7fc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d6ddeb'))
        ]))
        
        elements.append(sleep_table)
        elements.append(Spacer(1, 20))
        
        # Achievements section
        elements.append(Paragraph("🏆 Achievements & Milestones", self.styles['CustomSubtitle']))
        
        achievements = dashboard_data.get('achievements', [])
        if achievements:
            achievement_text = "<br/>".join([
                f"• {ach.get('title', 'Achievement')} {ach.get('icon', '✨')}"
                for ach in achievements
            ])
        else:
            achievement_text = "• Keep going! Your first achievement is just around the corner! 💪"
        
        elements.append(Paragraph(achievement_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 20))
        
        # Recommendations section
        elements.append(Paragraph("💡 Recommendations", self.styles['CustomSubtitle']))
        
        recommendations = self._generate_recommendations(summary)
        rec_text = "<br/>".join([f"• {rec}" for rec in recommendations])
        elements.append(Paragraph(rec_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        
        # Footer
        elements.append(Paragraph(
            "<i>This report is for informational purposes only and does not constitute medical advice. "
            "Please consult with healthcare professionals for medical concerns.</i>",
            self.styles['CustomBody']
        ))
        
        # Build PDF
        doc.build(elements)
        
        return output_path
    
    def generate_monthly_report(
        self,
        user_name: str,
        dashboard_data: Dict,
        trends_data: Dict,
        challenges_data: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """Generate comprehensive monthly report"""
        
        if output_path is None:
            output_path = f"monthly_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            "📈 Monthly Health Report",
            self.styles['CustomTitle']
        ))
        
        elements.append(Paragraph(
            f"<b>User:</b> {user_name}",
            self.styles['CustomBody']
        ))
        
        elements.append(Paragraph(
            f"<b>Report Period:</b> {datetime.now().strftime('%B %Y')}",
            self.styles['CustomBody']
        ))
        
        elements.append(Spacer(1, 30))
        
        # Executive Summary
        elements.append(Paragraph("🎯 Executive Summary", self.styles['CustomSubtitle']))
        
        summary_text = self._create_executive_summary(dashboard_data, trends_data, challenges_data)
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        
        # Weight Progress
        if trends_data.get('trends', {}).get('weight'):
            elements.append(Paragraph("⚖️ Weight Progress", self.styles['CustomSubtitle']))
            
            weight_change = trends_data['trends']['weight'].get('change', 0)
            weight_text = f"Weight change this month: <b>{weight_change:+.1f} kg</b>"
            
            if weight_change < 0:
                weight_text += " - Great job! 👏"
            elif weight_change > 0:
                weight_text += " - Keep working towards your goal! 💪"
            else:
                weight_text += " - Maintaining your weight! 👍"
            
            elements.append(Paragraph(weight_text, self.styles['CustomBody']))
            elements.append(Spacer(1, 15))
        
        # Challenges Progress
        if challenges_data.get('challenges'):
            elements.append(Paragraph("🏆 Challenges Progress", self.styles['CustomSubtitle']))
            
            for challenge in challenges_data['challenges']:
                challenge_text = (
                    f"<b>{challenge.get('title')}</b><br/>"
                    f"Progress: {challenge.get('completion_percentage', 0):.1f}% | "
                    f"Streak: {challenge.get('current_streak', 0)} days"
                )
                elements.append(Paragraph(challenge_text, self.styles['CustomBody']))
            
            elements.append(Spacer(1, 15))
        
        # Build PDF
        doc.build(elements)
        
        return output_path
    
    def _generate_recommendations(self, summary: Dict) -> list:
        """Generate personalized recommendations"""
        
        recommendations = []
        
        # Nutrition recommendations
        nutrition = summary.get('nutrition', {})
        avg_cals = nutrition.get('avg_daily_calories', 0)
        target_cals = nutrition.get('target', 2000)
        
        if avg_cals < target_cals - 300:
            recommendations.append("Consider increasing calorie intake to meet your daily target")
        elif avg_cals > target_cals + 300:
            recommendations.append("Focus on portion control to align with calorie goals")
        
        # Fitness recommendations
        fitness = summary.get('fitness', {})
        if fitness.get('total_workouts', 0) < 3:
            recommendations.append("Aim for at least 3-5 workouts per week for optimal results")
        
        # Sleep recommendations
        sleep = summary.get('sleep', {})
        if sleep.get('avg_hours', 0) < 7:
            recommendations.append("Prioritize 7-8 hours of sleep for better recovery")
        
        if not recommendations:
            recommendations.append("Keep up the excellent work! You're on track with your goals!")
        
        return recommendations
    
    def _create_executive_summary(self, dashboard: Dict, trends: Dict, challenges: Dict) -> str:
        """Create executive summary paragraph"""
        
        summary = f"""
        This month, you've made significant progress on your health journey. 
        You've logged {dashboard.get('summary', {}).get('nutrition', {}).get('days_tracked', 0)} days of nutrition data 
        and completed {dashboard.get('summary', {}).get('fitness', {}).get('total_workouts', 0)} workouts. 
        Your consistency and dedication are commendable! Keep up the great work and continue tracking your progress.
        """
        
        return summary.strip()


# Create global instance
report_generator = HealthReportGenerator()


# Example usage
if __name__ == "__main__":
    print("📄 PDF Report Generator Test\n")
    
    sample_data = {
        'period': 'Jan 20 - Jan 27, 2025',
        'summary': {
            'nutrition': {
                'avg_daily_calories': 1950,
                'avg_daily_protein': 145,
                'days_tracked': 7,
                'target': 2000,
                'protein_target': 150
            },
            'fitness': {
                'total_workouts': 5,
                'total_duration_minutes': 180,
                'workout_frequency': 0.71
            },
            'sleep': {
                'avg_hours': 7.5,
                'days_tracked': 7,
                'target_hours': 7.5
            }
        },
        'achievements': [
            {'title': '5-Day Workout Streak', 'icon': '🔥'}
        ]
    }
    
    output = report_generator.generate_weekly_report(
        user_name="Test User",
        dashboard_data=sample_data,
        output_path="test_health_report.pdf"
    )
    
    print(f"✅ Report generated: {output}")