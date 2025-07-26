import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
<<<<<<< HEAD
import App from './App.jsx';
=======
import Home from './components/Home.jsx';
import Dashboard from './components/Dashboard.jsx';
import App from './App.jsx';
import Results from './components/Results.jsx';

const router = createMemoryRouter([
  {
    path: '/',
    Component: App,
  },
  {
    path: 'tests/:testType',
    Component: Dashboard,
  },
  {
    path: '/results',
    Component: Results,
  },
]);
>>>>>>> d67f0f8 (style: add UI with dummy data for ref)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
