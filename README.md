# Customer Dashboard - Fitness/Nutrition Tracking App

A clean, minimal, and motivational React dashboard for fitness and nutrition tracking. This dashboard provides customers with a comprehensive view of their wellness journey, including body composition progress, attendance streaks, and trial pack progress.

## Features

### 🎯 Top Greeting Section
- Personalized welcome message with customer name
- Motivational subtext
- Progress card showing weight loss achievements

### 📊 Personal Information Card
- Compact display of customer details:
  - Age, Height
  - Wellness Center Name
  - Coach Name
  - Referred By
  - Trial Pack Start Date

### 📈 Body Composition Progress
- **Current vs Target Comparison**: Side-by-side cards showing current and ideal metrics
- **Target Badge**: Clear goal visualization
- **Weekly Data Table**: Scrollable table with recent progress
- **Interactive Line Chart**: Beautiful visualization using Recharts
  - Red line for Body Fat %
  - Green line for Muscle %
  - Responsive design with tooltips

### 🔥 Attendance Streaks
- **Streak Counter**: Motivational display of current streak
- **Calendar View**: Visual representation of attendance
- **Dynamic Quotes**: Weekly rotating motivational messages
- **Present/Absent Indicators**: Clear visual feedback

### 📅 Trial Pack Progress
- **Progress Bar**: Visual representation of completion
- **Detailed Information**: Start date, days completed, days remaining
- **Percentage Display**: Clear progress indication

## Design Features

- **Mobile-First Responsive Design**: Optimized for all screen sizes
- **Clean Minimal UI**: Focus on content with beautiful gradients
- **Motivational Color Scheme**: Energizing colors that inspire action
- **Smooth Animations**: Subtle transitions and hover effects
- **Accessibility**: High contrast and readable typography

## Installation

1. **Clone or download the files**
2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## Dependencies

- **React 18.2.0**: Core React library
- **Recharts 2.8.0**: For beautiful, responsive charts
- **React Scripts**: Development and build tools

## File Structure

```
├── CustomerDashboard.jsx    # Main dashboard component
├── CustomerDashboard.css    # Dashboard styling
├── App.js                  # App wrapper component
├── App.css                 # Global app styling
├── package.json            # Dependencies and scripts
└── README.md               # This file
```

## Customization

### Mock Data
The component uses mock data for demonstration. To integrate with real data:

1. **Replace mock data** in the `useState` hooks
2. **Connect to your API** endpoints
3. **Update data fetching** logic as needed

### Styling
- **Colors**: Modify CSS custom properties for brand colors
- **Layout**: Adjust grid and flex properties for different layouts
- **Typography**: Update font families and sizes in CSS

### Features
- **Add new sections** by extending the component
- **Modify chart data** by updating the data generation functions
- **Customize quotes** by editing the `motivationalQuotes` array

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- **Optimized rendering** with React hooks
- **Efficient chart rendering** with Recharts
- **Responsive images** and scalable graphics
- **Minimal bundle size** with tree-shaking

## License

MIT License - feel free to use this dashboard in your projects!

---

**Built with ❤️ for wellness and fitness tracking**