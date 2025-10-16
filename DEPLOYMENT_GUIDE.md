# NextLoad Dashboard - Deployment Guide

## 🚀 Quick Start

### Local Development
1. **Run the dashboard locally:**
   ```bash
   # Option 1: Using the batch file (Windows)
   run_dashboard.bat
   
   # Option 2: Using Python directly
   python -m streamlit run app.py
   
   # Option 3: Using streamlit command (if in PATH)
   streamlit run app.py
   ```

2. **Test the application:**
   ```bash
   python test_app.py
   ```

3. **Access the dashboard:**
   - Open your browser and go to: `http://localhost:8501`
   - The dashboard will automatically load with your data

## 📊 Dashboard Features

### Interactive Visualizations
- **Geographic Analysis**: Interactive map showing load origins and destinations
- **Rate Analysis**: Rate distributions and rate vs distance analysis
- **Equipment Analysis**: Breakdown by equipment types (Dry Van, Reefer, Flatbed, etc.)
- **Company Analysis**: Performance metrics by logistics companies
- **Time Analysis**: Load postings and pickups over time

### Data Filters
- Equipment Type filter
- State filter (origin/destination)
- Company filter
- Rate range slider
- Real-time filtering with instant updates

### Key Metrics
- Total loads count
- Average rate calculations
- Total distance metrics
- Company count statistics

## 🌐 GitHub Deployment

### 1. Push to GitHub
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/nextload-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `nextload-dashboard`
5. Set main file path: `app.py`
6. Click "Deploy!"

## 📁 Project Structure
```
nextload-dashboard/
├── app.py                 # Main Streamlit application
├── nextload.json          # Data file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── test_app.py           # Test script
├── run_dashboard.bat     # Windows batch file for easy running
└── DEPLOYMENT_GUIDE.md   # This file
```

## 🔧 Configuration

### Streamlit Configuration (`.streamlit/config.toml`)
- Custom theme colors
- Server settings
- Headless mode for deployment

### Dependencies (`requirements.txt`)
- streamlit: Web app framework
- pandas: Data manipulation
- plotly: Interactive visualizations
- numpy: Numerical computing

## 📈 Data Processing

The dashboard processes your load postings data to:
- Convert timestamps to readable dates
- Convert rates from cents to dollars
- Create route strings for better visualization
- Handle missing data gracefully
- Provide real-time filtering and analysis

## 🎯 Usage Tips

1. **Use the sidebar filters** to narrow down your analysis
2. **Click on different tabs** to explore various aspects of your data
3. **Hover over charts** for detailed information
4. **Use the data table** at the bottom to see filtered results
5. **The map visualization** shows geographic distribution of loads

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use**: Change the port in the command: `--server.port 8502`
2. **Data not loading**: Check that `nextload.json` is in the same directory
3. **Dependencies missing**: Run `pip install -r requirements.txt`

### Getting Help
- Check the test script output: `python test_app.py`
- Review the console output for error messages
- Ensure all dependencies are installed correctly

## 🚀 Production Deployment

For production deployment on Streamlit Cloud:
1. Ensure your repository is public or you have Streamlit Cloud access
2. The app will automatically detect `requirements.txt`
3. Streamlit Cloud will handle the deployment automatically
4. Your app will be available at: `https://your-app-name.streamlit.app`

## 📊 Performance

- **Data Caching**: Uses Streamlit's caching for optimal performance
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Filters update instantly as you interact
- **Memory Efficient**: Processes large datasets efficiently

---

**Ready to deploy?** Follow the GitHub deployment steps above and your dashboard will be live on Streamlit Cloud!
