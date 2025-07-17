# Investment Banking Platform

A comprehensive investment banking platform with income/expense tracking, savings advisor, and advanced reporting capabilities.

## 🚀 Features

- **Income/Expense Tracking**: Monitor your financial inflows and outflows
- **Savings Advisor**: AI-powered recommendations for optimal savings strategies
- **Report Engine**: Generate detailed financial reports and analytics
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **RESTful API**: Fast, scalable backend built with FastAPI

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy with PostgreSQL
- **Authentication**: JWT tokens
- **Validation**: Pydantic models

### Frontend

- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios

## 📦 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite for development)

### Backend Setup

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🏗️ Project Structure

```
InvestmentBanking/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── database/        # Database models
│   │   └── utils/           # Utility functions
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/           # React components
│   │   └── services/        # API services
│   └── tailwind.config.js
└── docs/
    ├── api-specs.md         # API documentation
    ├── architecture.md      # System architecture
    └── feature-docs/        # Feature specifications
```

## 🔧 Development

### API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./investment_banking.db
SECRET_KEY=your-secret-key-here
```

## 📊 Features Overview

### Income/Expense Tracking

- Add, edit, and categorize transactions
- Track recurring vs one-time expenses
- Generate spending reports

### Savings Advisor

- AI-powered savings recommendations
- Goal-based savings planning
- Investment suggestions

### Report Engine

- Financial health metrics
- Trend analysis
- Custom report generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
