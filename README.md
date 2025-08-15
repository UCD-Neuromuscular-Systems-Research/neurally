# Neurally - Clinical Speech Assessment Platform

A comprehensive desktop application for clinical speech analysis and assessment, built with Electron, React, and Python. Neurally provides automated speech assessment for inviduals with Huntington's disease (HD).

- **Multi-Test Support**: Neurally supports three different speech test types:

  - **Sustained Vowel (SV)**: Measures vocal endurance and quality
  - **Syllable Repetition (SR)**: Assesses speech motor control
  - **Paragraph Reading (PR)**: Evaluates connected speech production

## Architecture

### Frontend (React + Electron)

- **UI Framework**: React 19 with React Router
- **Styling**: Tailwind CSS for modern, responsive design
- **Desktop Integration**: Electron for cross-platform desktop deployment

### Backend (Node JS + Python)

- **Audio Processing**: Librosa, SciPy, NumPy, Praat-Parselmouth
- **Data Analysis**: Pandas, Matplotlib, Scikit-learn
- **Feature Extraction**: Custom HD (High Definition) processing modules based on the works of Ruth Filan ME, BioMedical Engineering, Vitória dos Santos Fahed PhD

## Installation

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd neurally
   ```

2. **Install Node.js dependencies**

   ```bash
   npm install
   ```

3. **Set up Python environment**

   ```bash
   cd src/scripts
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```

4. **Return to project root**
   ```bash
   cd ../..
   ```

## Usage

### Development Mode

1. **Start the development server**

   ```bash
   npm run dev
   ```

   This will start both the React development server and Electron application.

2. **Access the application**
   - The Electron window will open automatically
   - Navigate through the different test types on the home screen

### Production Build

1. **Build for your platform**

   ```bash
   For macOS (ARM64)
   npm run dist:mac

   For Windows (x64)
   npm run dist:win

   For Linux (x64)
   npm run dist:linux
   ```

2. **Find the built application**
   - Built applications will be in the `dist/` directory
   - Platform-specific installers will be generated

This can be distributed and used on other machines without any configuration

### Audio File Requirements

- **Format**: WAV files only

### Processing Settings

The application automatically handles:

- Audio file validation
- Quality checks
- Feature extraction optimization
- Result visualization

## 🛠️ Development

### Project Structure

```
neurally/
├── src/
│   ├── electron/          # Electron application
│   │   ├── main.js        # Main process
│   │   ├── preload.cjs    # Preload script
│   │   └── util.js        # Utilities
│   ├── scripts/           # Python backend
│   │   ├── main.py        # Main processing
│   │   ├── HD/            # Processing modules
│   │   └── requirements.txt
│   └── ui/                # React frontend
│       ├── components/    # UI components
│       ├── config/        # Configuration
│       └── utils/         # Utilities
├── package.json           # Node.js dependencies
├── electron-builder.json  # Build configuration
└── vite.config.js        # Vite configuration
```

### Key Scripts

- `npm run dev`: Start development environment
- `npm run build`: Build React application
- `npm run dist:*`: Build platform-specific distributions
- `npm run lint`: Run ESLint

### Adding New Features

1. **Frontend**: Add components in `src/ui/components/`
2. **Backend**: Extend processing in `src/scripts/HD/`
3. **Configuration**: Update feature definitions in `src/ui/config/`

## 🔍 Troubleshooting

### Common Issues

1. **Python Environment**

   - Ensure virtual environment is activated
   - Check Python version compatibility
   - Verify all requirements are installed

2. **Audio Processing**

   - Verify audio file format (WAV only)
   - Check file permissions
   - Ensure sufficient disk space

3. **Build Issues**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility
   - Verify platform-specific build tools

### Debug Mode

Enable debug logging by setting environment variables:

```bash
export NEURALLY_DEBUG=1
npm run dev
```

**Note**: This application is designed for clinical use and research purposes. Always ensure proper clinical protocols and ethical considerations when using for patient assessment.
