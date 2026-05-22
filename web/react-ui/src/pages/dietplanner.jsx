import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from "../app/api";

const DietPlanner = () => {
  const navigate = useNavigate();
  
  // Form state
  const [formData, setFormData] = useState({
    age: 28,
    weight: 70,
    height: 175,
    gender: 'male',
    activity_level: 'moderate',
    goal: 'muscle_gain',
    cuisine_preference: 'north_indian'
  });

  // Loading and result states
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // ✅ SINGLE handleInputChange function
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // ✅ SINGLE handleSubmit function with enhanced logging
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      console.log('🚀 Sending request to /ai/diet with:', formData);
      const response = await API.post("/ai/diet", formData);
      
      console.log('✅ Received response:', response.data);
      
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.message || 'Failed to generate meal plan');
      }
    } catch (err) {
      console.error('❌ Diet API Error:', err);
      console.error('Error response:', err.response?.data);
      
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

  // Activity level options
  const activityOptions = [
    { value: 'sedentary', label: 'Sedentary (Little/no exercise)' },
    { value: 'light', label: 'Light (1-3 days/week)' },
    { value: 'moderate', label: 'Moderate (3-5 days/week)' },
    { value: 'active', label: 'Active (6-7 days/week)' },
    { value: 'very_active', label: 'Very Active (Hard exercise + physical job)' }
  ];

  // Goal options
  const goalOptions = [
    { value: 'weight_loss', label: 'Weight Loss' },
    { value: 'muscle_gain', label: 'Muscle Gain' },
    { value: 'maintain', label: 'Maintenance' }
  ];

  // Cuisine options
  const cuisineOptions = [
    { value: '', label: 'Any Cuisine' },
    { value: 'north_indian', label: 'North Indian' },
    { value: 'south_indian', label: 'South Indian' },
    { value: 'vegetarian', label: 'Vegetarian' },
    { value: 'non_vegetarian', label: 'Non-Vegetarian' },
    { value: 'healthy', label: 'Healthy' },
    { value: 'sweets', label: 'Sweets (Limited)' }
  ];

  // ✅ Safe Progress Circle Component
  const ProgressCircle = ({ accuracy, size = 60 }) => {
    const numAccuracy = parseInt(accuracy) || 0;
    const radius = size / 2 - 6;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (numAccuracy / 100) * circumference;

    return (
      <div style={{ width: size, height: size, display: 'inline-block' }}>
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
          <circle
            r={radius}
            cx={size / 2}
            cy={size / 2}
            fill="none"
            stroke="#e0e0e0"
            strokeWidth="12"
          />
          <circle
            r={radius}
            cx={size / 2}
            cy={size / 2}
            fill="none"
            stroke="#4CAF50"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
          />
          <text
            x={size / 2}
            y={size / 2}
            textAnchor="middle"
            dy=".3em"
            fontSize="16"
            fontWeight="bold"
            fill="#333"
          >
            {numAccuracy}%
          </text>
        </svg>
      </div>
    );
  };

  // ✅ IMPROVED SAFE GETTER - Only returns default if final value is missing
  const safeGet = (obj, path, defaultValue = 0) => {
    try {
      const keys = path.split('.');
      let value = obj;
      for (const key of keys) {
        value = value?.[key];
      }
      // Check ONLY the final value
      return (value !== undefined && value !== null) ? value : defaultValue;
    } catch {
      return defaultValue;
    }
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
        <header style={styles.header}>
          <h1 style={styles.title}>🚀 AI Diet Planner</h1>
          <p style={styles.subtitle}>Precision meal planning with 98-100% target accuracy</p>
        </header>

        {/* Input Form */}
        <div style={styles.formCard}>
          <div style={styles.formGrid}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                min="16"
                max="80"
                required
                style={styles.input}
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
                max="200"
                step="0.1"
                required
                style={styles.input}
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
                required
                style={styles.input}
              />
            </div>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Gender</label>
              <select 
                name="gender" 
                value={formData.gender} 
                onChange={handleInputChange} 
                required
                style={styles.select}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            
            <div style={styles.formGroupFull}>
              <label style={styles.label}>Activity Level</label>
              <select 
                name="activity_level" 
                value={formData.activity_level} 
                onChange={handleInputChange} 
                required
                style={styles.select}
              >
                {activityOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
            
            <div style={styles.formGroupFull}>
              <label style={styles.label}>Goal</label>
              <select 
                name="goal" 
                value={formData.goal} 
                onChange={handleInputChange} 
                required
                style={styles.select}
              >
                {goalOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
            
            <div style={styles.formGroupFull}>
              <label style={styles.label}>Cuisine Preference</label>
              <select 
                name="cuisine_preference" 
                value={formData.cuisine_preference} 
                onChange={handleInputChange}
                style={styles.select}
              >
                {cuisineOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
          </div>
          
          <button 
            onClick={handleSubmit}
            disabled={loading} 
            style={{
              ...styles.submitButton,
              opacity: loading ? 0.6 : 1,
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? '🤖 Generating Perfect Plan...' : '🚀 Generate Meal Plan'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div style={styles.errorMessage}>
            ❌ {error}
          </div>
        )}

        {/* Results - ✅ SAFE RENDERING WITH OPTIONAL CHAINING */}
        {result && result.success && (
          <>
            {/* Daily Targets - ✅ FIXED: Access through "plan" object */}
            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>📊 Daily Targets</h2>
              <div style={styles.targetsGrid}>
                {/* Calories */}
                <div style={styles.targetCard}>
                  <div style={styles.targetValue}>
                    {(result?.plan?.daily_targets?.calories || 0).toLocaleString()}
                  </div>
                  <div style={styles.targetLabel}>Calories</div>
                </div>
                
                {/* Protein */}
                <div style={styles.targetCard}>
                  <div style={styles.targetValue}>
                    {result?.plan?.daily_targets?.protein || 0}g
                  </div>
                  <div style={styles.targetLabel}>Protein</div>
                </div>
                
                {/* Macros */}
                <div style={styles.targetCard}>
                  <div style={styles.targetValue}>
                    {(result?.plan?.daily_targets?.macronutrients?.protein_g || 0)}g P |{' '}
                    {(result?.plan?.daily_targets?.macronutrients?.carbs_g || 0)}g C |{' '}
                    {(result?.plan?.daily_targets?.macronutrients?.fat_g || 0)}g F
                  </div>
                  <div style={styles.targetLabel}>Macros</div>
                </div>
                
                {/* Overall Accuracy */}
                <div style={{...styles.targetCard, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
                  <div style={styles.targetValue}>
                    {result?.plan?.daily_summary?.overall_accuracy || '0%'}
                  </div>
                  <div style={styles.targetLabel}>Accuracy</div>
                </div>
              </div>
            </section>

            {/* Meal Plan - ✅ FIXED: Access through "plan" object */}
            {result?.plan?.meal_plan && typeof result.plan.meal_plan === 'object' && (
              <section style={styles.section}>
                <h2 style={styles.sectionTitle}>🍽️ Your Perfect Meal Plan</h2>
                <div style={styles.mealsGrid}>
                  {Object.entries(result.plan.meal_plan).map(([mealName, mealData]) => {
                    if (!mealData || typeof mealData !== 'object') return null;
                    
                    return (
                      <div key={mealName} style={styles.mealCard}>
                        <div style={styles.mealHeader}>
                          <h3 style={styles.mealName}>{mealName.toUpperCase()}</h3>
                          <div style={styles.mealAccuracy}>
                            <ProgressCircle accuracy={mealData.accuracy || 0} />
                          </div>
                        </div>
                        
                        <div style={styles.mealTargets}>
                          <div style={styles.targetRow}>
                            🎯 Target: {mealData.target_calories || 0} cal | {mealData.target_protein || 0}g protein
                          </div>
                          <div style={styles.achievedRow}>
                            ✅ Achieved: {mealData.achieved?.calories || 0} cal | {mealData.achieved?.protein || 0}g protein
                          </div>
                        </div>
                        
                        <div style={styles.mealFoods}>
                          {Array.isArray(mealData.foods) && mealData.foods.map((food, idx) => (
                            <div key={idx} style={styles.foodItem}>
                              <div style={styles.foodHeader}>
                                <span style={styles.foodName}>{food?.name || 'Unknown Food'}</span>
                                <span style={styles.foodServing}>{food?.serving || ''}</span>
                              </div>
                              <div style={styles.foodNutrition}>
                                {food?.calories || 0} cal | {food?.protein || 0}g P | {food?.carbs || 0}g C | {food?.fat || 0}g F
                              </div>
                            </div>
                          ))}
                          
                          {(!mealData.foods || mealData.foods.length === 0) && (
                            <div style={{ textAlign: 'center', color: '#999', padding: '20px' }}>
                              No foods available for this meal
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            )}

            {/* Recommendations - ✅ FIXED: Access through "plan" object */}
            {Array.isArray(result?.plan?.recommendations) && result.plan.recommendations.length > 0 && (
              <section style={styles.section}>
                <h2 style={styles.sectionTitle}>💡 Smart Recommendations</h2>
                <div style={styles.recList}>
                  {result.plan.recommendations.map((rec, idx) => (
                    <div key={idx} style={styles.recommendation}>
                      ✨ {rec}
                    </div>
                  ))}
                </div>
              </section>
            )}


          </>
        )}
      </div>
    </div>
  );
};

// Inline styles
const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    position: 'relative'
  },
  backButton: {
    position: 'absolute',
    top: '20px',
    left: '20px',
    padding: '10px 20px',
    background: 'rgba(255,255,255,0.2)',
    color: 'white',
    border: '2px solid rgba(255,255,255,0.3)',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    transition: 'all 0.3s',
    backdropFilter: 'blur(10px)',
    zIndex: 100
  },
  innerContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    paddingTop: '40px'
  },
  header: {
    textAlign: 'center',
    color: 'white',
    marginBottom: '30px'
  },
  title: {
    fontSize: '3rem',
    fontWeight: '800',
    margin: '0 0 10px 0'
  },
  subtitle: {
    fontSize: '1.2rem',
    opacity: 0.9
  },
  formCard: {
    background: 'white',
    borderRadius: '20px',
    padding: '30px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
    marginBottom: '30px'
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
    marginBottom: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column'
  },
  formGroupFull: {
    gridColumn: '1 / -1',
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    fontWeight: '600',
    marginBottom: '8px',
    color: '#333'
  },
  input: {
    padding: '12px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '16px',
    transition: 'border-color 0.3s',
    outline: 'none'
  },
  select: {
    padding: '12px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '16px',
    backgroundColor: 'white',
    cursor: 'pointer',
    outline: 'none'
  },
  submitButton: {
    width: '100%',
    padding: '18px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    fontSize: '18px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'transform 0.2s'
  },
  errorMessage: {
    background: '#fee',
    color: '#c33',
    padding: '15px',
    borderRadius: '10px',
    marginBottom: '20px',
    fontWeight: '600',
    border: '2px solid #fcc'
  },
  section: {
    background: 'white',
    borderRadius: '20px',
    padding: '30px',
    marginBottom: '30px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
  },
  sectionTitle: {
    fontSize: '2rem',
    fontWeight: '700',
    marginBottom: '20px',
    color: '#333'
  },
  targetsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px'
  },
  targetCard: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '25px',
    borderRadius: '15px',
    textAlign: 'center'
  },
  targetValue: {
    fontSize: '2rem',
    fontWeight: '800',
    marginBottom: '5px'
  },
  targetLabel: {
    fontSize: '0.9rem',
    opacity: 0.9
  },
  mealsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px'
  },
  mealCard: {
    border: '2px solid #e0e0e0',
    borderRadius: '15px',
    padding: '20px',
    background: '#fafafa'
  },
  mealHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
    paddingBottom: '15px',
    borderBottom: '2px solid #e0e0e0'
  },
  mealName: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#667eea',
    margin: 0
  },
  mealAccuracy: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  },
  mealTargets: {
    marginBottom: '15px',
    fontSize: '0.9rem'
  },
  targetRow: {
    marginBottom: '5px',
    color: '#666'
  },
  achievedRow: {
    color: '#4CAF50',
    fontWeight: '600'
  },
  mealFoods: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px'
  },
  foodItem: {
    background: 'white',
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #e0e0e0'
  },
  foodHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '5px'
  },
  foodName: {
    fontWeight: '600',
    color: '#333'
  },
  foodServing: {
    color: '#999',
    fontSize: '0.85rem'
  },
  foodNutrition: {
    fontSize: '0.85rem',
    color: '#666'
  },
  recList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  recommendation: {
    background: '#f0f7ff',
    padding: '15px',
    borderRadius: '10px',
    borderLeft: '4px solid #667eea',
    fontSize: '1rem',
    color: '#333'
  }
};

export default DietPlanner;