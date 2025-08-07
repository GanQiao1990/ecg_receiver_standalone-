"""
ECG Heart Problem Diagnosis using Gemini 2.5 Flash Model
"""
import json
import requests
import numpy as np
from typing import List, Dict, Any, Optional
import logging
import time
from datetime import datetime

class GeminiECGDiagnosisClient:
    """Client for ECG heart problem diagnosis using Gemini 2.5 Flash model."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.gptnb.ai/"):
        """
        Initialize the Gemini diagnosis client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = "gemini-2.5-flash-preview-04-17"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def preprocess_ecg_data(self, ecg_values: List[float], sampling_rate: int = 250) -> Dict[str, Any]:
        """
        Preprocess ECG data for analysis.
        
        Args:
            ecg_values: List of ECG values
            sampling_rate: Sampling rate in Hz
            
        Returns:
            Dictionary containing processed ECG features
        """
        if not ecg_values:
            return {}
            
        ecg_array = np.array(ecg_values)
        
        # Basic statistics
        stats = {
            'mean': float(np.mean(ecg_array)),
            'std': float(np.std(ecg_array)),
            'min': float(np.min(ecg_array)),
            'max': float(np.max(ecg_array)),
            'peak_to_peak': float(np.max(ecg_array) - np.min(ecg_array)),
            'rms': float(np.sqrt(np.mean(ecg_array**2))),
            'sample_count': len(ecg_values),
            'duration_seconds': len(ecg_values) / sampling_rate
        }
        
        # Find peaks (simple peak detection)
        peaks = self._find_peaks(ecg_array)
        
        # Calculate heart rate if peaks found
        heart_rate = None
        if len(peaks) > 1:
            peak_intervals = np.diff(peaks) / sampling_rate  # intervals in seconds
            if len(peak_intervals) > 0:
                avg_interval = np.mean(peak_intervals)
                heart_rate = 60.0 / avg_interval if avg_interval > 0 else None
        
        # Heart rate variability
        hrv = None
        if len(peaks) > 2:
            rr_intervals = np.diff(peaks) * (1000.0 / sampling_rate)  # RR intervals in ms
            hrv = {
                'mean_rr': float(np.mean(rr_intervals)),
                'std_rr': float(np.std(rr_intervals)),
                'rmssd': float(np.sqrt(np.mean(np.diff(rr_intervals)**2)))
            }
        
        return {
            'statistics': stats,
            'heart_rate_bpm': heart_rate,
            'peak_count': len(peaks),
            'heart_rate_variability': hrv,
            'raw_data_sample': ecg_values[:min(100, len(ecg_values))]  # First 100 samples for context
        }
    
    def _find_peaks(self, data: np.ndarray, min_distance: int = 50) -> List[int]:
        """Simple peak detection algorithm."""
        if len(data) < 3:
            return []
            
        peaks = []
        for i in range(1, len(data) - 1):
            if (data[i] > data[i-1] and data[i] > data[i+1] and 
                data[i] > np.mean(data) + 0.5 * np.std(data)):
                if not peaks or i - peaks[-1] >= min_distance:
                    peaks.append(i)
        
        return peaks
    
    def diagnose_heart_condition(self, ecg_data: Dict[str, Any], patient_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Diagnose heart condition using Gemini model.
        
        Args:
            ecg_data: Preprocessed ECG data
            patient_info: Optional patient information (age, gender, symptoms, etc.)
            
        Returns:
            Diagnosis result with conditions, severity, and recommendations
        """
        try:
            # Prepare the prompt for the LLM
            prompt = self._create_diagnosis_prompt(ecg_data, patient_info)
            
            # Make API request
            response = self._make_api_request(prompt)
            
            # Parse and validate response
            diagnosis = self._parse_diagnosis_response(response)
            
            # Add metadata
            diagnosis['timestamp'] = datetime.now().isoformat()
            diagnosis['model_used'] = self.model
            diagnosis['api_response_raw'] = response
            
            return diagnosis
            
        except Exception as e:
            self.logger.error(f"Error in heart condition diagnosis: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'diagnosis': 'Unable to analyze due to error',
                'severity': 'unknown',
                'confidence': 0.0
            }
    
    def _create_diagnosis_prompt(self, ecg_data: Dict[str, Any], patient_info: Optional[Dict[str, Any]]) -> str:
        """Create a detailed prompt for ECG diagnosis."""
        
        prompt = """You are an expert cardiologist analyzing ECG data. Please provide a comprehensive heart condition diagnosis based on the following ECG analysis:

ECG DATA ANALYSIS:
"""
        
        if 'statistics' in ecg_data:
            stats = ecg_data['statistics']
            prompt += f"""
Statistical Analysis:
- Mean voltage: {stats.get('mean', 'N/A')} μV
- Standard deviation: {stats.get('std', 'N/A')} μV
- Voltage range: {stats.get('min', 'N/A')} to {stats.get('max', 'N/A')} μV
- Peak-to-peak amplitude: {stats.get('peak_to_peak', 'N/A')} μV
- RMS value: {stats.get('rms', 'N/A')} μV
- Recording duration: {stats.get('duration_seconds', 'N/A')} seconds
- Sample count: {stats.get('sample_count', 'N/A')}
"""
        
        if ecg_data.get('heart_rate_bpm'):
            prompt += f"\nHeart Rate: {ecg_data['heart_rate_bpm']:.1f} BPM"
        
        if ecg_data.get('peak_count'):
            prompt += f"\nDetected QRS complexes: {ecg_data['peak_count']}"
        
        if ecg_data.get('heart_rate_variability'):
            hrv = ecg_data['heart_rate_variability']
            prompt += f"""
Heart Rate Variability:
- Mean RR interval: {hrv.get('mean_rr', 'N/A')} ms
- RR interval std dev: {hrv.get('std_rr', 'N/A')} ms
- RMSSD: {hrv.get('rmssd', 'N/A')} ms
"""
        
        if patient_info:
            prompt += f"\nPATIENT INFORMATION:\n"
            for key, value in patient_info.items():
                prompt += f"- {key}: {value}\n"
        
        prompt += """
Please provide your diagnosis in the following JSON format:
{
    "primary_diagnosis": "Primary heart condition identified",
    "secondary_conditions": ["List", "of", "other", "possible", "conditions"],
    "severity": "low|moderate|high|critical",
    "confidence": 0.85,
    "key_findings": ["Key", "ECG", "findings", "that", "support", "diagnosis"],
    "recommendations": {
        "immediate_actions": ["Urgent", "actions", "if", "needed"],
        "follow_up": ["Follow-up", "recommendations"],
        "lifestyle": ["Lifestyle", "modifications"]
    },
    "normal_ranges_comparison": {
        "heart_rate": "comparison with normal 60-100 BPM",
        "rhythm": "assessment of rhythm regularity",
        "morphology": "assessment of wave morphology"
    },
    "risk_factors": ["Identified", "risk", "factors"],
    "prognosis": "Short description of expected outcome"
}

ONLY return the JSON response, no additional text."""
        
        return prompt
    
    def _make_api_request(self, prompt: str) -> str:
        """Make API request to Gemini model."""
        url = f"{self.base_url}/v1/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # Low temperature for more consistent medical analysis
            "max_tokens": 2000
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception("No response content from API")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
    
    def _parse_diagnosis_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the diagnosis response from the LLM."""
        try:
            # Try to extract JSON from response
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean[7:-3].strip()
            elif response_clean.startswith('```'):
                response_clean = response_clean[3:-3].strip()
            
            diagnosis = json.loads(response_clean)
            
            # Validate required fields
            required_fields = ['primary_diagnosis', 'severity', 'confidence']
            for field in required_fields:
                if field not in diagnosis:
                    diagnosis[field] = 'unknown'
            
            # Ensure confidence is a float between 0 and 1
            try:
                confidence = float(diagnosis.get('confidence', 0))
                diagnosis['confidence'] = max(0.0, min(1.0, confidence))
            except (ValueError, TypeError):
                diagnosis['confidence'] = 0.5
            
            return diagnosis
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            # Return a basic diagnosis structure
            return {
                'primary_diagnosis': 'Analysis completed - see raw response',
                'severity': 'unknown',
                'confidence': 0.5,
                'raw_response': response,
                'parse_error': str(e)
            }
    
    def analyze_ecg_stream(self, ecg_values: List[float], window_size: int = 2500, 
                          overlap: float = 0.5, patient_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Analyze ECG data in chunks for real-time diagnosis.
        
        Args:
            ecg_values: List of ECG values
            window_size: Size of analysis window (default 2500 = 10 seconds at 250Hz)
            overlap: Overlap between windows (0.0 to 1.0)
            patient_info: Optional patient information
            
        Returns:
            List of diagnosis results for each window
        """
        if len(ecg_values) < window_size:
            # Not enough data, analyze what we have
            ecg_data = self.preprocess_ecg_data(ecg_values)
            return [self.diagnose_heart_condition(ecg_data, patient_info)]
        
        results = []
        step_size = int(window_size * (1 - overlap))
        
        for i in range(0, len(ecg_values) - window_size + 1, step_size):
            window_data = ecg_values[i:i + window_size]
            ecg_data = self.preprocess_ecg_data(window_data)
            
            # Add window metadata
            ecg_data['window_start'] = i
            ecg_data['window_end'] = i + window_size
            
            diagnosis = self.diagnose_heart_condition(ecg_data, patient_info)
            diagnosis['window_info'] = {
                'start_sample': i,
                'end_sample': i + window_size,
                'window_number': len(results) + 1
            }
            
            results.append(diagnosis)
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        
        return results


def create_diagnosis_client(api_key: str) -> GeminiECGDiagnosisClient:
    """
    Factory function to create a diagnosis client.
    
    Args:
        api_key: API key for Gemini model
        
    Returns:
        Configured GeminiECGDiagnosisClient instance
    """
    return GeminiECGDiagnosisClient(api_key, "https://api.gptnb.ai/")


# Example usage and testing
if __name__ == "__main__":
    # Example usage (for testing)
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        client = create_diagnosis_client(api_key)
        
        # Test with sample ECG data
        sample_ecg = [100, 102, 98, 95, 120, 150, 180, 160, 140, 110, 105, 100] * 200  # Simulated data
        
        # Preprocess the data
        ecg_data = client.preprocess_ecg_data(sample_ecg)
        print("ECG Data Analysis:", json.dumps(ecg_data, indent=2))
        
        # Get diagnosis
        patient_info = {
            'age': 45,
            'gender': 'male',
            'symptoms': 'chest pain, shortness of breath'
        }
        
        diagnosis = client.diagnose_heart_condition(ecg_data, patient_info)
        print("Diagnosis:", json.dumps(diagnosis, indent=2))
    else:
        print("Please set GEMINI_API_KEY environment variable for testing")