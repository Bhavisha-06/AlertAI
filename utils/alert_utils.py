"""
Alert utilities for AlertAI
"""
import os
import platform
import time
from gtts import gTTS

class AlertManager:
    def __init__(self, cooldown_period=5):
        """
        Initialize the AlertManager.
        
        Args:
            cooldown_period (int): Minimum time (seconds) between alerts for the same class
        """
        self.last_alerts = {}  # Dictionary to track when each class was last alerted
        self.cooldown_period = cooldown_period
        self.alert_file = "alert.mp3"
        
        # Detection state tracking
        self.detection_state = {}  # Dictionary to track detection state for each class
        self.detection_start_time = {}  # When continuous detection started
        
        # Default required detection time (seconds)
        self.required_detection_time = 1.5
        
    def set_required_detection_time(self, seconds):
        """Set the required continuous detection time to trigger an alert"""
        self.required_detection_time = seconds
        
    def update_detection(self, class_name, is_detected):
        """
        Update the detection state for a class.
        
        Args:
            class_name (str): The class being detected
            is_detected (bool): Whether the class is currently detected
            
        Returns:
            bool: True if an alert should be triggered, False otherwise
        """
        current_time = time.time()
        
        # Initialize tracking for this class if not already done
        if class_name not in self.detection_state:
            self.detection_state[class_name] = False
            self.detection_start_time[class_name] = 0
            self.last_alerts[class_name] = 0
            
        # If detection state changes to True, record the start time
        if is_detected and not self.detection_state[class_name]:
            self.detection_state[class_name] = True
            self.detection_start_time[class_name] = current_time
            
        # If detection state changes to False, reset
        elif not is_detected and self.detection_state[class_name]:
            self.detection_state[class_name] = False
            
        # Check if we should trigger an alert
        should_alert = False
        if (self.detection_state[class_name] and 
                current_time - self.detection_start_time[class_name] >= self.required_detection_time and
                current_time - self.last_alerts[class_name] >= self.cooldown_period):
            self.last_alerts[class_name] = current_time
            should_alert = True
            
        return should_alert
            
    def sound_alert(self, message):
        """
        Generate and play a text-to-speech alert.
        
        Args:
            message (str): The message to be spoken
        """
        try:
            # Generate speech file
            tts = gTTS(message)
            tts.save(self.alert_file)
            
            # Play the audio based on operating system
            system = platform.system()
            if system == "Windows":
                os.system(f"start {self.alert_file}")
            elif system == "Darwin":  # macOS
                os.system(f"afplay {self.alert_file}")
            else:  # Linux
                os.system(f"mpg123 {self.alert_file}")
                
            print(f"Alert triggered: {message}")
                
        except Exception as e:
            print(f"Error generating alert: {e}")
