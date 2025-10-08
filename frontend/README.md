# VoiceAI Frontend

A React application that connects to the VoiceAI backend API for authentication and user management.

## Features

- **Authentication System**: Login and registration with JWT token management
- **Protected Routes**: Automatic redirection based on authentication status
- **Responsive Design**: Mobile-friendly interface with modern styling
- **API Integration**: Seamless connection to backend at `http://127.0.0.1:5000/`
- **Error Handling**: Comprehensive error handling for API calls and user interactions

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn package manager
- VoiceAI backend running on `http://127.0.0.1:5000/`

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm start
   ```

2. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── Navbar.js
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Dashboard.js
│   ├── contexts/
│   │   └── AuthContext.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## API Configuration

The application is configured to connect to the backend at `http://127.0.0.1:5000/`. This can be modified in `src/services/api.js` if needed.

## Available Scripts

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects from Create React App (one-way operation)

## Authentication Flow

1. **Registration**: Users can create new accounts with username, email, and password
2. **Login**: Existing users can log in with username and password
3. **Token Management**: JWT tokens are automatically stored and managed
4. **Protected Routes**: Dashboard is only accessible to authenticated users
5. **Auto-logout**: Users are automatically logged out when tokens expire

## Styling

The application uses custom CSS with a clean, modern design. Key styling features:
- Responsive grid layouts
- Card-based component design
- Consistent color scheme
- Mobile-first approach

## Browser Support

The application supports all modern browsers including:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- The app uses React Router for navigation
- Axios is used for HTTP requests
- Context API manages authentication state
- All API calls include proper error handling
- Loading states are implemented for better UX
