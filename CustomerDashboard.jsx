import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const CustomerDashboard = () => {
  // Mock data for demonstration
  const [customerData] = useState({
    name: "Sarah Johnson",
    age: 28,
    height: "165 cm",
    wellnessCenter: "FitLife Wellness Center",
    coachName: "Mike Rodriguez",
    referredBy: "Dr. Emily Chen",
    trialStartDate: "2024-01-15",
    weightLost: 2.3,
    currentWeight: 68.5,
    idealWeight: 65.0,
    currentBodyFat: 22.5,
    idealBodyFat: 18.0,
    currentMuscle: 35.2,
    idealMuscle: 38.0,
    currentBMI: 25.1,
    idealBMI: 23.9,
    attendanceStreak: 7,
    trialDay: 10,
    totalTrialDays: 21
  });

  const [motivationalQuotes] = useState([
    "Discipline beats motivation. Show up today!",
    "Your body can do it. It's your mind you have to convince.",
    "The only bad workout is the one that didn't happen.",
    "Progress, not perfection.",
    "You're stronger than you think you are.",
    "Every expert was once a beginner.",
    "The pain you feel today is the strength you feel tomorrow."
  ]);

  const [currentQuote, setCurrentQuote] = useState(motivationalQuotes[0]);

  // Generate mock body composition data for the last 30 days
  const generateBodyCompositionData = () => {
    const data = [];
    const today = new Date();
    
    for (let i = 29; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      // Simulate realistic progress with some variation
      const baseFat = 25 - (i * 0.08) + (Math.random() - 0.5) * 0.5;
      const baseMuscle = 32 + (i * 0.06) + (Math.random() - 0.5) * 0.3;
      
      data.push({
        date: date.toISOString().split('T')[0],
        fatPercentage: Math.max(18, Math.round(baseFat * 10) / 10),
        musclePercentage: Math.min(40, Math.round(baseMuscle * 10) / 10)
      });
    }
    return data;
  };

  const [bodyCompositionData] = useState(generateBodyCompositionData());

  // Generate mock attendance data for the last 30 days
  const generateAttendanceData = () => {
    const attendance = [];
    const today = new Date();
    
    for (let i = 29; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      // Simulate attendance with higher probability for recent days
      const isPresent = Math.random() > (i > 7 ? 0.3 : 0.1);
      attendance.push({
        date: date.toISOString().split('T')[0],
        present: isPresent
      });
    }
    return attendance;
  };

  const [attendanceData] = useState(generateAttendanceData());

  // Change motivational quote weekly
  useEffect(() => {
    const quoteIndex = Math.floor(Date.now() / (7 * 24 * 60 * 60 * 1000)) % motivationalQuotes.length;
    setCurrentQuote(motivationalQuotes[quoteIndex]);
  }, [motivationalQuotes]);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getProgressPercentage = () => {
    return Math.round((customerData.trialDay / customerData.totalTrialDays) * 100);
  };

  const getDaysLeft = () => {
    return customerData.totalTrialDays - customerData.trialDay;
  };

  return (
    <div className="customer-dashboard">
      {/* Top Greeting Section */}
      <div className="greeting-section">
        <div className="greeting-content">
          <h1 className="welcome-title">Welcome back, {customerData.name}</h1>
          <p className="welcome-subtitle">Your consistency is building your future body.</p>
          <div className="progress-card">
            <div className="progress-icon">💪</div>
            <div className="progress-text">
              You've lost {customerData.weightLost} kg since your last analysis — keep it up!
            </div>
          </div>
        </div>
      </div>

      {/* Personal Info Card */}
      <div className="personal-info-card">
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Age</span>
            <span className="info-value">{customerData.age}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Height</span>
            <span className="info-value">{customerData.height}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Wellness Center</span>
            <span className="info-value">{customerData.wellnessCenter}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Coach</span>
            <span className="info-value">{customerData.coachName}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Referred By</span>
            <span className="info-value">{customerData.referredBy}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Trial Start</span>
            <span className="info-value">{new Date(customerData.trialStartDate).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {/* Body Composition Progress */}
      <div className="body-composition-section">
        <h2 className="section-title">Body Composition Progress</h2>
        
        {/* Current vs Ideal Comparison */}
        <div className="comparison-cards">
          <div className="comparison-card current">
            <h3>Current</h3>
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Weight</span>
                <span className="metric-value">{customerData.currentWeight} kg</span>
              </div>
              <div className="metric">
                <span className="metric-label">Body Fat</span>
                <span className="metric-value">{customerData.currentBodyFat}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Muscle</span>
                <span className="metric-value">{customerData.currentMuscle}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">BMI</span>
                <span className="metric-value">{customerData.currentBMI}</span>
              </div>
            </div>
          </div>
          
          <div className="comparison-card ideal">
            <h3>Target</h3>
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Weight</span>
                <span className="metric-value">{customerData.idealWeight} kg</span>
              </div>
              <div className="metric">
                <span className="metric-label">Body Fat</span>
                <span className="metric-value">{customerData.idealBodyFat}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Muscle</span>
                <span className="metric-value">{customerData.idealMuscle}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">BMI</span>
                <span className="metric-value">{customerData.idealBMI}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Target Badge */}
        <div className="target-badge">
          <span className="target-text">
            Goal: -{customerData.currentBodyFat - customerData.idealBodyFat}% Body Fat, 
            +{customerData.idealMuscle - customerData.currentMuscle}% Muscle
          </span>
        </div>

        {/* Weekly Data Table */}
        <div className="data-table-container">
          <h3>Recent Progress</h3>
          <div className="data-table">
            <div className="table-header">
              <span>Date</span>
              <span>Fat %</span>
              <span>Muscle %</span>
            </div>
            {bodyCompositionData.slice(-7).map((entry, index) => (
              <div key={index} className="table-row">
                <span>{formatDate(entry.date)}</span>
                <span className="fat-value">{entry.fatPercentage}%</span>
                <span className="muscle-value">{entry.musclePercentage}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Main Line Chart */}
        <div className="chart-container">
          <h3>Body Composition Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={bodyCompositionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => formatDate(value)}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                domain={[15, 45]}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                labelFormatter={(value) => formatDate(value)}
                formatter={(value, name) => [`${value}%`, name === 'fatPercentage' ? 'Body Fat' : 'Muscle']}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="fatPercentage" 
                stroke="#ff6b6b" 
                strokeWidth={3}
                name="Body Fat %"
                dot={{ fill: '#ff6b6b', strokeWidth: 2, r: 4 }}
              />
              <Line 
                type="monotone" 
                dataKey="musclePercentage" 
                stroke="#51cf66" 
                strokeWidth={3}
                name="Muscle %"
                dot={{ fill: '#51cf66', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Attendance Streaks Section */}
      <div className="attendance-section">
        <h2 className="section-title">Attendance Streaks</h2>
        
        <div className="streak-info">
          <div className="streak-counter">
            <span className="fire-emoji">🔥</span>
            <span className="streak-text">You're on a {customerData.attendanceStreak}-day streak!</span>
          </div>
          
          <div className="motivational-quote">
            <p>"{currentQuote}"</p>
          </div>
        </div>

        {/* Calendar View */}
        <div className="calendar-container">
          <h3>Recent Attendance</h3>
          <div className="calendar-grid">
            {attendanceData.slice(-14).map((day, index) => (
              <div 
                key={index} 
                className={`calendar-day ${day.present ? 'present' : 'absent'}`}
                title={`${formatDate(day.date)} - ${day.present ? 'Present' : 'Absent'}`}
              >
                <span className="day-number">{new Date(day.date).getDate()}</span>
                <span className="day-status">
                  {day.present ? '✓' : '✗'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Trial Pack Progress Section */}
      <div className="trial-progress-section">
        <h2 className="section-title">Trial Pack Progress</h2>
        
        <div className="progress-container">
          <div className="progress-info">
            <div className="progress-text">
              Day {customerData.trialDay} of {customerData.totalTrialDays} — {getProgressPercentage()}% complete
            </div>
            <div className="progress-details">
              <span>Started: {new Date(customerData.trialStartDate).toLocaleDateString()}</span>
              <span>Days completed: {customerData.trialDay}</span>
              <span>Days left: {getDaysLeft()}</span>
            </div>
          </div>
          
          <div className="progress-bar-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${getProgressPercentage()}%` }}
              ></div>
            </div>
            <div className="progress-percentage">{getProgressPercentage()}%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;



