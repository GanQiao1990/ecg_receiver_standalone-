#!/usr/bin/env python3
"""
Test script for ECG heart diagnosis functionality.
This script demonstrates how to use the diagnosis API without the full GUI.
"""

import os
import sys
import numpy as np
import time
from dotenv import load_dotenv

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecg_diagnosis import GeminiECGDiagnosisClient, create_diagnosis_client

def generate_sample_ecg_data(duration_seconds=10, sampling_rate=250, heart_rate=75):
    """
    Generate realistic sample ECG data for testing.
    
    Args:
        duration_seconds: Duration of ECG data to generate
        sampling_rate: Sampling rate in Hz
        heart_rate: Heart rate in BPM
        
    Returns:
        List of ECG values
    """
    num_samples = duration_seconds * sampling_rate
    t = np.linspace(0, duration_seconds, num_samples)
    
    # Generate basic ECG waveform (simplified)
    ecg_signal = np.zeros(num_samples)
    
    # Add QRS complexes
    beat_interval = 60.0 / heart_rate  # seconds between beats
    beat_samples = int(beat_interval * sampling_rate)
    
    for i in range(0, num_samples, beat_samples):
        if i + 50 < num_samples:  # QRS complex width
            # Simple QRS complex simulation
            ecg_signal[i:i+10] += np.linspace(0, 200, 10)  # Q wave
            ecg_signal[i+10:i+25] += np.linspace(200, -400, 15)  # R wave  
            ecg_signal[i+25:i+35] += np.linspace(-400, 100, 10)  # S wave
            ecg_signal[i+35:i+50] += np.linspace(100, 0, 15)  # Return to baseline
    
    # Add some noise and baseline variation
    noise = np.random.normal(0, 10, num_samples)
    baseline_drift = 20 * np.sin(2 * np.pi * 0.1 * t)  # Slow baseline drift
    
    ecg_signal += noise + baseline_drift
    
    return ecg_signal.tolist()

def test_normal_ecg():
    """Test with normal ECG pattern."""
    print("Generating normal ECG pattern...")
    return generate_sample_ecg_data(duration_seconds=10, heart_rate=75)

def test_tachycardia_ecg():
    """Test with tachycardia (fast heart rate)."""
    print("Generating tachycardia ECG pattern...")
    return generate_sample_ecg_data(duration_seconds=10, heart_rate=120)

def test_bradycardia_ecg():
    """Test with bradycardia (slow heart rate)."""
    print("Generating bradycardia ECG pattern...")
    return generate_sample_ecg_data(duration_seconds=10, heart_rate=45)

def test_arrhythmia_ecg():
    """Test with irregular rhythm."""
    print("Generating arrhythmia ECG pattern...")
    base_ecg = generate_sample_ecg_data(duration_seconds=10, heart_rate=75)
    
    # Add some irregular beats
    for i in range(500, len(base_ecg), 800):
        if i + 100 < len(base_ecg):
            # Add premature ventricular contraction (PVC)
            base_ecg[i:i+50] = [val * 1.5 for val in base_ecg[i:i+50]]
    
    return base_ecg

def run_diagnosis_test(client, ecg_data, test_name, patient_info=None):
    """
    Run a diagnosis test with the given ECG data.
    
    Args:
        client: GeminiECGDiagnosisClient instance
        ecg_data: List of ECG values
        test_name: Name of the test for display
        patient_info: Optional patient information
    """
    print(f"\n{'='*60}")
    print(f"RUNNING TEST: {test_name}")
    print(f"{'='*60}")
    
    # Preprocess the data
    print("Preprocessing ECG data...")
    processed_data = client.preprocess_ecg_data(ecg_data)
    
    print(f"ECG Statistics:")
    stats = processed_data.get('statistics', {})
    print(f"  • Duration: {stats.get('duration_seconds', 0):.1f} seconds")
    print(f"  • Samples: {stats.get('sample_count', 0)}")
    print(f"  • Heart Rate: {processed_data.get('heart_rate_bpm', 'N/A')} BPM")
    print(f"  • Mean Voltage: {stats.get('mean', 0):.2f} μV")
    print(f"  • Voltage Range: {stats.get('peak_to_peak', 0):.2f} μV")
    
    # Get diagnosis
    print("\nRequesting diagnosis from Gemini model...")
    start_time = time.time()
    
    try:
        diagnosis = client.diagnose_heart_condition(processed_data, patient_info)
        end_time = time.time()
        
        print(f"Diagnosis completed in {end_time - start_time:.2f} seconds")
        
        # Display results
        print(f"\n📋 DIAGNOSIS RESULTS:")
        print(f"Primary Diagnosis: {diagnosis.get('primary_diagnosis', 'Unknown')}")
        print(f"Severity: {diagnosis.get('severity', 'unknown').upper()}")
        print(f"Confidence: {diagnosis.get('confidence', 0):.1%}")
        
        # Secondary conditions
        secondary = diagnosis.get('secondary_conditions', [])
        if secondary:
            print(f"Secondary Conditions: {', '.join(secondary)}")
        
        # Key findings
        findings = diagnosis.get('key_findings', [])
        if findings:
            print(f"Key Findings:")
            for finding in findings:
                print(f"  • {finding}")
        
        # Recommendations
        recommendations = diagnosis.get('recommendations', {})
        if recommendations:
            immediate = recommendations.get('immediate_actions', [])
            if immediate:
                print(f"Immediate Actions:")
                for action in immediate:
                    print(f"  • {action}")
        
        return diagnosis
        
    except Exception as e:
        print(f"❌ Diagnosis failed: {str(e)}")
        return None

def main():
    """Main test function."""
    print("ECG Heart Diagnosis Test Suite")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key or set the environment variable.")
        print("Example: GEMINI_API_KEY=your_api_key_here")
        return 1
    
    # Create diagnosis client
    try:
        print(f"Initializing Gemini diagnosis client...")
        client = create_diagnosis_client(api_key)
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {str(e)}")
        return 1
    
    # Test scenarios
    test_scenarios = [
        ("Normal Heart Rhythm", test_normal_ecg(), {"age": 35, "gender": "male"}),
        ("Tachycardia", test_tachycardia_ecg(), {"age": 60, "gender": "female", "symptoms": "palpitations"}),
        ("Bradycardia", test_bradycardia_ecg(), {"age": 70, "gender": "male", "symptoms": "fatigue, dizziness"}),
        ("Arrhythmia", test_arrhythmia_ecg(), {"age": 45, "gender": "female", "symptoms": "irregular heartbeat"}),
    ]
    
    results = []
    
    for test_name, ecg_data, patient_info in test_scenarios:
        result = run_diagnosis_test(client, ecg_data, test_name, patient_info)
        results.append((test_name, result))
        
        # Add delay between tests to be respectful to the API
        print("\nWaiting 3 seconds before next test...")
        time.sleep(3)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    for test_name, result in results:
        if result:
            primary = result.get('primary_diagnosis', 'Unknown')
            severity = result.get('severity', 'unknown')
            confidence = result.get('confidence', 0)
            print(f"✅ {test_name}: {primary} (Severity: {severity}, Confidence: {confidence:.1%})")
        else:
            print(f"❌ {test_name}: Test failed")
    
    print(f"\nAll tests completed! The ECG diagnosis system is ready to use.")
    print(f"You can now run the full GUI application with: python -m ecg_receiver.main")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())