import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import Home from './components/Home.jsx';
import Dashboard from './components/Dashboard.jsx';
import Results from './components/Results.jsx';
import { createMemoryRouter, RouterProvider } from 'react-router';

const router = createMemoryRouter([
  {
    path: '/',
    Component: Home,
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

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
