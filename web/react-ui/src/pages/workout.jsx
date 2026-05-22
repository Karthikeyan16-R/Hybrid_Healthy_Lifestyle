import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, Heart, Target, TrendingUp, Dumbbell, Calendar, Flame, Award, AlertCircle, CheckCircle } from 'lucide-react';
import API from "../app/api";

const WorkoutRecommender = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    age: '',
    height: '',
    weight: '',
    activity_level: 'medium',
    goal: 'maintain',
    has_injury: false,
    is_beginner: false
  });

  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      console.log('🚀 Sending workout request:', formData);
      
      // Prepare the request body
      const requestBody = {
        age: parseInt(formData.age),
        height: parseFloat(formData.height),
        weight: parseFloat(formData.weight),
        activity_level: formData.activity_level,
        goal: formData.goal,
        has_injury: formData.has_injury,
        is_beginner: formData.is_beginner
      };
      
      console.log('📦 Request body:', requestBody);
      
      // Try different possible endpoints
      let response;
      try {
        // Try the most likely endpoint first
        response = await API.post('/ai/workout', requestBody);
      } catch (err1) {
        console.log('❌ /ai/workout failed, trying /workout/recommend...');
        try {
          response = await API.post('/workout/recommend', requestBody);
        } catch (err2) {
          console.log('❌ /workout/recommend failed, trying /api/workout/recommend...');
          response = await API.post('/api/workout/recommend', requestBody);
        }
      }

      console.log('✅ Received workout response:', response.data);

      if (response.data.success) {
        setRecommendation(response.data);
      } else {
        setError(response.data.message || 'Failed to generate recommendation');
      }
    } catch (err) {
      console.error('❌ Workout API Error:', err);
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        setError(err.response?.data?.detail || err.response?.data?.message || 'Network error. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getTierColor = (tier) => {
    const colors = {
      'Recovery': { bg: '#dbeafe', text: '#1e40af', border: '#93c5fd' },
      'Foundation': { bg: '#dcfce7', text: '#166534', border: '#86efac' },
      'Progression': { bg: '#fed7aa', text: '#9a3412', border: '#fdba74' },
      'Performance': { bg: '#fecaca', text: '#991b1b', border: '#fca5a5' }
    };
    return colors[tier] || { bg: '#f3f4f6', text: '#374151', border: '#d1d5db' };
  };

  const getBMIColor = (category) => {
    const colors = {
      'Underweight': '#2563eb',
      'Normal': '#16a34a',
      'Overweight': '#ea580c',
      'Obese': '#dc2626'
    };
    return colors[category] || '#6b7280';
  };

  return (
    <div style={styles.container}>
      {/* Back Button */}
      <button 
        onClick={() => navigate('/')} 
        style={styles.backButton}
      >
        ← Back to Home
      </button>

      <div style={styles.innerContainer}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.headerContent}>
            <Dumbbell style={{ width: '48px', height: '48px', color: '#4f46e5', marginRight: '12px' }} />
            <h1 style={styles.title}>AI Workout Recommender</h1>
          </div>
          <p style={styles.subtitle}>Get personalized workout plans powered by Fitbit data & AI</p>
        </div>

        {/* Input Panel */}
        <div style={styles.formCard}>
          <h2 style={styles.formTitle}>
            <Activity style={{ width: '24px', height: '24px', marginRight: '8px', color: '#4f46e5' }} />
            Your Profile
          </h2>

          <div style={styles.formContent}>
            <div style={styles.gridThree}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Age (years)</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  min="15"
                  max="100"
                  style={styles.input}
                  placeholder="28"
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Height (cm)</label>
                <input
                  type="number"
                  name="height"
                  value={formData.height}
                  onChange={handleInputChange}
                  min="100"
                  max="250"
                  style={styles.input}
                  placeholder="175"
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Weight (kg)</label>
                <input
                  type="number"
                  name="weight"
                  value={formData.weight}
                  onChange={handleInputChange}
                  min="30"
                  max="300"
                  step="0.1"
                  style={styles.input}
                  placeholder="75"
                />
              </div>
            </div>

            <div style={styles.gridTwo}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Activity Level</label>
                <select
                  name="activity_level"
                  value={formData.activity_level}
                  onChange={handleInputChange}
                  style={styles.select}
                >
                  <option value="low">Low (Sedentary)</option>
                  <option value="medium">Medium (Moderately Active)</option>
                  <option value="high">High (Very Active)</option>
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Fitness Goal</label>
                <select
                  name="goal"
                  value={formData.goal}
                  onChange={handleInputChange}
                  style={styles.select}
                >
                  <option value="weight_loss">Weight Loss</option>
                  <option value="muscle_gain">Muscle Gain</option>
                  <option value="maintain">Maintain Fitness</option>
                  <option value="endurance">Build Endurance</option>
                </select>
              </div>
            </div>

            <div style={styles.checkboxContainer}>
              <label style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  name="has_injury"
                  checked={formData.has_injury}
                  onChange={handleInputChange}
                  style={styles.checkbox}
                />
                <span style={styles.checkboxText}>I have an injury or limitation</span>
              </label>

              <label style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  name="is_beginner"
                  checked={formData.is_beginner}
                  onChange={handleInputChange}
                  style={styles.checkbox}
                />
                <span style={styles.checkboxText}>I'm new to fitness</span>
              </label>
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading || !formData.age || !formData.height || !formData.weight}
              style={{
                ...styles.submitButton,
                opacity: loading || !formData.age || !formData.height || !formData.weight ? 0.5 : 1,
                cursor: loading || !formData.age || !formData.height || !formData.weight ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? (
                <div style={styles.buttonContent}>
                  <div style={styles.spinner}></div>
                  Generating Plan...
                </div>
              ) : (
                <div style={styles.buttonContent}>
                  <TrendingUp style={{ width: '20px', height: '20px', marginRight: '8px' }} />
                  Get My Workout Plan
                </div>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div style={styles.errorCard}>
            <AlertCircle style={{ width: '20px', height: '20px', color: '#dc2626', marginRight: '12px', flexShrink: 0 }} />
            <div>
              <h3 style={styles.errorTitle}>Error</h3>
              <p style={styles.errorText}>{error}</p>
            </div>
          </div>
        )}

        {/* Recommendation Results */}
        {recommendation && (
          <div style={styles.resultsContainer}>
            {/* User Profile Summary */}
            <div style={styles.section}>
              <h2 style={styles.sectionTitle}>
                <Target style={{ width: '24px', height: '24px', marginRight: '8px', color: '#4f46e5' }} />
                Your Profile Summary
              </h2>
              <div style={styles.gridFour}>
                <div style={styles.statCard}>
                  <p style={styles.statLabel}>BMI</p>
                  <p style={{ ...styles.statValue, color: getBMIColor(recommendation?.user_profile?.bmi_category) }}>
                    {recommendation?.user_profile?.bmi || 0}
                  </p>
                  <p style={styles.statSubtext}>{recommendation?.user_profile?.bmi_category || 'N/A'}</p>
                </div>
                <div style={styles.statCard}>
                  <p style={styles.statLabel}>Age</p>
                  <p style={styles.statValue}>{recommendation?.user_profile?.age || 0}</p>
                  <p style={styles.statSubtext}>years</p>
                </div>
                <div style={styles.statCard}>
                  <p style={styles.statLabel}>Activity</p>
                  <p style={{ ...styles.statValue, textTransform: 'capitalize' }}>
                    {recommendation?.user_profile?.activity_level || 'N/A'}
                  </p>
                </div>
                <div style={styles.statCard}>
                  <p style={styles.statLabel}>Goal</p>
                  <p style={{ ...styles.statValue, fontSize: '1.25rem' }}>
                    {(recommendation?.user_profile?.goal || '').replace('_', ' ')}
                  </p>
                </div>
              </div>
            </div>

            {/* Workout Tier */}
            <div style={styles.section}>
              <div style={styles.tierHeader}>
                <h2 style={styles.sectionTitle}>
                  <Award style={{ width: '24px', height: '24px', marginRight: '8px', color: '#4f46e5' }} />
                  Your Workout Tier
                </h2>
                {recommendation?.workout_tier && (
                  <span style={{
                    ...styles.tierBadge,
                    backgroundColor: getTierColor(recommendation.workout_tier).bg,
                    color: getTierColor(recommendation.workout_tier).text,
                    borderColor: getTierColor(recommendation.workout_tier).border
                  }}>
                    {recommendation.workout_tier}
                  </span>
                )}
              </div>
              <div style={styles.gridThree}>
                <div style={styles.metricCard}>
                  <Heart style={{ width: '20px', height: '20px', color: '#4f46e5', marginBottom: '8px' }} />
                  <p style={styles.metricLabel}>Heart Rate Zone</p>
                  <p style={styles.metricValue}>
                    {recommendation?.heart_rate_zone?.target_min || 0}-{recommendation?.heart_rate_zone?.target_max || 0} bpm
                  </p>
                  <p style={styles.metricSubtext}>{recommendation?.heart_rate_zone?.zone || 'N/A'} Intensity</p>
                </div>
                <div style={styles.metricCardGreen}>
                  <Activity style={{ width: '20px', height: '20px', color: '#16a34a', marginBottom: '8px' }} />
                  <p style={styles.metricLabel}>Daily Active Minutes</p>
                  <p style={styles.metricValue}>{recommendation?.daily_targets?.active_minutes || 0} min</p>
                </div>
                <div style={styles.metricCardOrange}>
                  <Calendar style={{ width: '20px', height: '20px', color: '#ea580c', marginBottom: '8px' }} />
                  <p style={styles.metricLabel}>Workouts per Week</p>
                  <p style={styles.metricValue}>{recommendation?.daily_targets?.workouts_per_week || 0} days</p>
                </div>
              </div>
            </div>

            {/* Workout Plan */}
            <div style={styles.section}>
              <h2 style={styles.sectionTitle}>
                <Dumbbell style={{ width: '24px', height: '24px', marginRight: '8px', color: '#4f46e5' }} />
                Your Workout Plan
              </h2>
              
              <div style={styles.planSummary}>
                <p style={styles.planFocus}>Focus: {recommendation?.workout_plan?.focus || 'N/A'}</p>
                <p style={styles.planDetail}>
                  <strong>Schedule:</strong> {recommendation?.workout_plan?.weekly_schedule || 'N/A'}
                </p>
                <p style={styles.planDetail}>
                  <strong>Goal Strategy:</strong> {recommendation?.workout_plan?.goal_specific_focus || 'N/A'}
                </p>
              </div>

              <div style={styles.exerciseGrid}>
                {Array.isArray(recommendation?.workout_plan?.exercises) && 
                  recommendation.workout_plan.exercises.map((exercise, index) => (
                    <div key={index} style={styles.exerciseCard}>
                      <div style={styles.exerciseHeader}>
                        <h3 style={styles.exerciseName}>{exercise?.name || 'Exercise'}</h3>
                        <Flame style={{ width: '16px', height: '16px', color: '#ea580c' }} />
                      </div>
                      <div style={styles.exerciseDetails}>
                        {exercise?.sets && <p style={styles.exerciseDetail}><strong>Sets:</strong> {exercise.sets}</p>}
                        {exercise?.duration && <p style={styles.exerciseDetail}><strong>Duration:</strong> {exercise.duration}</p>}
                        <p style={styles.exerciseDetail}><strong>Intensity:</strong> {exercise?.intensity || 'N/A'}</p>
                        <p style={styles.exerciseCalories}>≈ {exercise?.calories || 0} cal</p>
                      </div>
                    </div>
                  ))}
              </div>

              <div style={styles.nutritionCard}>
                <p style={styles.nutritionText}>
                  <strong>Estimated Calories per Session:</strong> {recommendation?.workout_plan?.estimated_calories_burned || 0} cal
                </p>
                <p style={styles.nutritionText}>
                  <strong>Progression:</strong> {recommendation?.workout_plan?.progression_strategy || 'N/A'}
                </p>
                <p style={styles.nutritionText}>
                  <strong>Nutrition Tip:</strong> {recommendation?.workout_plan?.nutrition_note || 'N/A'}
                </p>
              </div>
            </div>

            {/* AI Insights */}
            <div style={styles.insightsCard}>
              <h2 style={styles.insightsTitle}>
                <CheckCircle style={{ width: '24px', height: '24px', marginRight: '8px' }} />
                AI Personalized Insights
              </h2>
              
              <div style={styles.insightsMessage}>
                <p style={styles.insightsMessageText}>
                  {recommendation?.ai_insights?.personalized_message || 'Keep up the great work!'}
                </p>
              </div>

              {Array.isArray(recommendation?.ai_insights?.tips) && recommendation.ai_insights.tips.length > 0 && (
                <div style={styles.tipsContainer}>
                  <h3 style={styles.tipsTitle}>Tips for Success:</h3>
                  <div style={styles.tipsList}>
                    {recommendation.ai_insights.tips.map((tip, index) => (
                      <div key={index} style={styles.tipItem}>
                        <CheckCircle style={{ width: '20px', height: '20px', marginRight: '8px', flexShrink: 0, marginTop: '2px' }} />
                        <p style={styles.tipText}>{tip}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recommendation?.ai_insights?.motivation && (
                <div style={styles.motivationCard}>
                  <p style={styles.motivationText}>"{recommendation.ai_insights.motivation}"</p>
                </div>
              )}
            </div>

            {/* Data Source */}
            <div style={styles.dataSource}>
              <p>{recommendation?.dataset_source || 'Powered by AI'}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Inline Styles
const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    position: 'relative'
  },
  backButton: {
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '10px 20px',
    background: 'white',
    color: '#4f46e5',
    border: '2px solid #e0e7ff',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    transition: 'all 0.3s',
    zIndex: 100
  },
  innerContainer: {
    maxWidth: '1536px',
    margin: '0 auto',
    paddingTop: '40px'
  },
  header: {
    textAlign: 'center',
    marginBottom: '32px'
  },
  headerContent: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '16px'
  },
  title: {
    fontSize: '2.25rem',
    fontWeight: '700',
    color: '#1f2937'
  },
  subtitle: {
    color: '#4b5563',
    fontSize: '1.125rem'
  },
  formCard: {
    background: 'white',
    borderRadius: '16px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
    padding: '32px',
    marginBottom: '32px'
  },
  formTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: '24px',
    display: 'flex',
    alignItems: 'center'
  },
  formContent: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  gridThree: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '24px'
  },
  gridTwo: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '24px'
  },
  gridFour: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '16px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '8px'
  },
  input: {
    width: '100%',
    padding: '10px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '16px',
    outline: 'none',
    transition: 'border-color 0.2s'
  },
  select: {
    width: '100%',
    padding: '10px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '16px',
    backgroundColor: 'white',
    cursor: 'pointer',
    outline: 'none'
  },
  checkboxContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '16px'
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer'
  },
  checkbox: {
    width: '16px',
    height: '16px',
    marginRight: '8px',
    accentColor: '#4f46e5'
  },
  checkboxText: {
    fontSize: '0.875rem',
    color: '#374151'
  },
  submitButton: {
    width: '100%',
    padding: '14px 24px',
    background: '#4f46e5',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.3s'
  },
  buttonContent: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  spinner: {
    width: '20px',
    height: '20px',
    border: '2px solid rgba(255,255,255,0.3)',
    borderTopColor: 'white',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    marginRight: '8px'
  },
  errorCard: {
    background: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '32px',
    display: 'flex',
    alignItems: 'flex-start'
  },
  errorTitle: {
    fontWeight: '600',
    color: '#991b1b',
    marginBottom: '4px'
  },
  errorText: {
    color: '#b91c1c',
    fontSize: '0.875rem'
  },
  resultsContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  section: {
    background: 'white',
    borderRadius: '16px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
    padding: '24px'
  },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: '16px',
    display: 'flex',
    alignItems: 'center'
  },
  statCard: {
    textAlign: 'center',
    padding: '16px',
    background: '#f9fafb',
    borderRadius: '8px'
  },
  statLabel: {
    fontSize: '0.875rem',
    color: '#6b7280'
  },
  statValue: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#1f2937',
    margin: '8px 0'
  },
  statSubtext: {
    fontSize: '0.75rem',
    color: '#9ca3af'
  },
  tierHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px'
  },
  tierBadge: {
    padding: '8px 16px',
    borderRadius: '9999px',
    fontWeight: '700',
    fontSize: '1.125rem',
    border: '2px solid'
  },
  metricCard: {
    padding: '16px',
    background: '#eef2ff',
    borderRadius: '8px'
  },
  metricCardGreen: {
    padding: '16px',
    background: '#dcfce7',
    borderRadius: '8px'
  },
  metricCardOrange: {
    padding: '16px',
    background: '#ffedd5',
    borderRadius: '8px'
  },
  metricLabel: {
    fontSize: '0.875rem',
    color: '#6b7280'
  },
  metricValue: {
    fontSize: '1.25rem',
    fontWeight: '700',
    color: '#1f2937',
    margin: '8px 0'
  },
  metricSubtext: {
    fontSize: '0.75rem',
    color: '#9ca3af'
  },
  planSummary: {
    marginBottom: '24px',
    padding: '16px',
    background: 'linear-gradient(to right, #eef2ff, #f3e8ff)',
    borderRadius: '8px'
  },
  planFocus: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: '8px'
  },
  planDetail: {
    fontSize: '0.875rem',
    color: '#4b5563',
    marginBottom: '4px'
  },
  exerciseGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '16px',
    marginBottom: '24px'
  },
  exerciseCard: {
    padding: '16px',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    transition: 'border-color 0.3s'
  },
  exerciseHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '8px'
  },
  exerciseName: {
    fontWeight: '600',
    color: '#1f2937'
  },
  exerciseDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px'
  },
  exerciseDetail: {
    fontSize: '0.875rem',
    color: '#6b7280'
  },
  exerciseCalories: {
    color: '#ea580c',
    fontWeight: '500'
  },
  nutritionCard: {
    background: '#fef3c7',
    border: '1px solid #fde68a',
    borderRadius: '8px',
    padding: '16px'
  },
  nutritionText: {
    fontSize: '0.875rem',
    color: '#374151',
    marginBottom: '8px'
  },
  insightsCard: {
    background: 'linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%)',
    borderRadius: '16px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
    padding: '24px',
    color: 'white'
  },
  insightsTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    marginBottom: '16px',
    display: 'flex',
    alignItems: 'center'
  },
  insightsMessage: {
    background: 'rgba(255,255,255,0.2)',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px'
  },
  insightsMessageText: {
    fontSize: '1.125rem',
    lineHeight: '1.6'
  },
  tipsContainer: {
    marginBottom: '16px'
  },
  tipsTitle: {
    fontWeight: '600',
    marginBottom: '12px',
    fontSize: '1.125rem'
  },
  tipsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px'
  },
  tipItem: {
    display: 'flex',
    alignItems: 'flex-start',
    background: 'rgba(255,255,255,0.1)',
    borderRadius: '8px',
    padding: '12px'
  },
  tipText: {
    fontSize: '0.875rem'
  },
  motivationCard: {
    background: 'rgba(255,255,255,0.2)',
    borderRadius: '8px',
    padding: '16px',
    textAlign: 'center'
  },
  motivationText: {
    fontSize: '1.25rem',
    fontWeight: '700',
    fontStyle: 'italic'
  },
  dataSource: {
    textAlign: 'center',
    fontSize: '0.875rem',
    color: '#9ca3af'
  }
};

export default WorkoutRecommender;