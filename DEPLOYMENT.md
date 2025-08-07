# ECM_LLM - ECG Monitor with Large Language Model Integration

## 🎯 Project Overview

**Repository Name**: `ecm_llm`  
**Full Name**: ECG Monitor with AI-powered heart diagnosis using Large Language Models  
**Technology Stack**: Python + PyQt5 + Gemini 2.5 Flash AI Model  
**API Endpoint**: https://api.gptnb.ai/  

## 🚀 GitHub Repository Setup

### Repository Information
- **GitHub URL**: https://github.com/GanQiao1990/ecm_llm
- **Visibility**: Public
- **Description**: ECG Monitor with AI-powered heart diagnosis using Large Language Models (Gemini 2.5 Flash). Real-time ECG analysis with intelligent cardiac condition detection and clinical recommendations.

### Repository Topics (Add on GitHub)
```
ecg-monitoring
ai-diagnosis
heart-health
gemini-ai
large-language-models
medical-ai
real-time-analysis
cardiology
health-tech
python-gui
esp32
ads1292r
```

## 📊 Project Statistics

### Codebase Stats
- **Total Files**: 15+ Python files + documentation
- **Lines of Code**: 2,600+ lines added in v2.0
- **Languages**: Python (primary), Markdown (documentation)
- **Dependencies**: 6 main packages (PyQt5, numpy, requests, etc.)

### Key Features Implemented
✅ Real-time ECG data visualization  
✅ AI-powered heart diagnosis using Gemini 2.5 Flash  
✅ Patient information integration  
✅ Automatic ECG analysis and statistics  
✅ Auto-diagnosis mode (configurable intervals)  
✅ Diagnosis history tracking  
✅ Severity assessment with color coding  
✅ Clinical recommendations generation  
✅ Comprehensive test suite  
✅ Cross-platform GUI application  

## 🔧 Technical Architecture

### Core Components
1. **ECG Data Acquisition** (`ecg_receiver/core/`)
   - Serial communication with ESP32+ADS1292R
   - Real-time data processing and buffering
   - CSV data recording capabilities

2. **AI Diagnosis Engine** (`ecg_diagnosis.py`)
   - Gemini 2.5 Flash LLM integration
   - ECG preprocessing and feature extraction
   - Heart condition analysis and recommendations
   - Confidence scoring and risk assessment

3. **User Interface** (`ecg_receiver/gui/`)
   - Dual-panel layout (ECG plot + diagnosis panel)
   - Real-time waveform visualization
   - Interactive diagnosis controls
   - Tabbed results display (diagnosis, history, statistics)

4. **Testing & Validation** (`test_diagnosis.py`, `demo.py`)
   - Simulated ECG pattern generation
   - API connectivity testing
   - System validation and feature demonstration

## 🔍 AI Diagnosis Capabilities

### Supported Conditions
- Arrhythmias (irregular heart rhythms)
- Tachycardia (fast heart rate > 100 BPM)
- Bradycardia (slow heart rate < 60 BPM)
- Heart rate variability abnormalities
- QRS complex morphology issues
- Conduction abnormalities

### Clinical Output
- Primary diagnosis with confidence score
- Secondary condition possibilities
- Severity assessment (Low, Moderate, High, Critical)
- Key ECG findings explanation
- Immediate action recommendations
- Follow-up care suggestions
- Lifestyle modification advice

## 📈 Version Information

### Version 2.0 Enhancements
- **AI Integration**: Gemini 2.5 Flash model integration
- **Enhanced GUI**: Modern interface with diagnosis panel
- **Real-time Analysis**: Background processing with threading
- **Patient Context**: Demographics and symptoms integration
- **History Tracking**: Persistent diagnosis records
- **Auto-diagnosis**: Configurable periodic analysis
- **Error Handling**: Robust API and connection management
- **Documentation**: Comprehensive README and guides

## 🛠️ Deployment Instructions

### 1. Prerequisites
```bash
# Python 3.8+ required
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration
```bash
# Copy configuration template
cp .env.example .env

# Edit .env file and add:
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_URL=https://api.gptnb.ai/
```

### 3. Hardware Setup
- ESP32 microcontroller
- ADS1292R ECG shield
- ECG electrodes
- USB connection cable

### 4. Application Launch
```bash
# Method 1: Direct execution
python -m ecg_receiver.main

# Method 2: Package installation
pip install -e .
ecg-receiver
```

### 5. Testing Without Hardware
```bash
# Test AI diagnosis with simulated data
python test_diagnosis.py

# Run system validation
python demo.py
```

## 🔐 Security & Privacy

### API Security
- API keys stored in environment variables
- No hardcoded credentials in source code
- Secure HTTPS communication with AI service
- Request timeout and error handling

### Patient Data
- Patient information used only for diagnosis context
- No persistent storage of patient data
- Real-time processing without cloud storage
- Local ECG data recording (optional)

## 📋 Usage Scenarios

### Clinical Settings
- Real-time ECG monitoring in clinics
- Quick heart condition screening
- Educational demonstrations
- Research data collection

### Home Healthcare
- Personal heart health monitoring
- Elderly care assistance
- Fitness and wellness tracking
- Telemedicine support

### Educational Use
- Medical student training
- Cardiology education
- AI/ML demonstration
- Biomedical engineering projects

## 🎉 Project Success Metrics

### Technical Achievements
- ✅ Successful AI model integration
- ✅ Real-time processing capabilities
- ✅ Cross-platform compatibility
- ✅ Comprehensive error handling
- ✅ Modular and extensible architecture

### User Experience
- ✅ Intuitive graphical interface
- ✅ Clear diagnostic output
- ✅ Helpful clinical recommendations
- ✅ Configurable analysis settings
- ✅ Comprehensive documentation

## 📞 Support & Contact

**Developer**: qiao@126.com  
**Repository**: https://github.com/GanQiao1990/ecm_llm  
**License**: MIT License  
**AI Model**: Gemini 2.5 Flash Preview  
**API Provider**: https://api.gptnb.ai/  

---

*🤖 Enhanced with Claude Code - Intelligent software development assistant*

**Last Updated**: 2025-01-06  
**Version**: 2.0  
**Status**: Production Ready ✅