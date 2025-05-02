"""
AlertAI - Drowsiness and Distraction Detection System

This script uses a trained YOLOv8 model to detect signs of drowsiness and distraction
and provides audio alerts when these conditions are detected continuously.
"""

import cv2
import time
import argparse
from ultralytics import YOLO
from utils.alert_utils import AlertManager

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='AlertAI - Drowsiness Detection System')
    parser.add_argument('--model', type=str, default='best.pt', 
                        help='Path to the YOLOv8 model (default: best.pt)')
    parser.add_argument('--camera', type=int, default=0, 
                        help='Camera index (default: 0)')
    parser.add_argument('--conf', type=float, default=0.5, 
                        help='Detection confidence threshold (default: 0.5)')
    parser.add_argument('--detection-time', type=float, default=1.5, 
                        help='Required continuous detection time in seconds (default: 1.5)')
    parser.add_argument('--cooldown', type=int, default=5, 
                        help='Cooldown period between alerts of the same class (default: 5)')
    return parser.parse_args()

def print_model_info(model):
    """Print model class information"""
    print("\n=== AlertAI Model Information ===")
    print("Loaded classes:")
    for class_id, class_name in model.names.items():
        print(f"Class ID: {class_id}, Class Name: {class_name}")
    print("=================================\n")

def main():
    """Main function for AlertAI detection system"""
    # Parse arguments
    args = parse_arguments()
    
    # Initialize alert manager
    alert_manager = AlertManager(cooldown_period=args.cooldown)
    alert_manager.set_required_detection_time(args.detection_time)
    
    # Load the YOLO model
    try:
        model = YOLO(args.model)
    except Exception as e:
        print(f"Error loading model: {e}")
        print(f"Make sure '{args.model}' exists and is a valid YOLOv8 model file.")
        return
    
    # Print model information
    print_model_info(model)
    
    # Define the classes that should trigger alerts
    ALERT_CLASSES = ['drowsy', 'head drop', 'yawn', 'distracted']
    print(f"Monitoring for: {', '.join(ALERT_CLASSES)}")
    
    # Class-specific colors (BGR format)
    class_colors = {
        'drowsy': (0, 0, 255),      # Red
        'head drop': (0, 165, 255), # Orange
        'yawn': (0, 255, 255),      # Yellow
        'distracted': (255, 0, 0),  # Blue
    }
    
    # Start the webcam
    print(f"Opening camera {args.camera}...")
    cap = cv2.VideoCapture(args.camera)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {args.camera}")
        return
    
    # Get video properties for FPS calculation
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # Default to 30 FPS if unable to determine
    
    print(f"Camera opened successfully. Estimated FPS: {fps}")
    print("Press 'q' to quit")
    
    # Dictionary to track whether each class is detected in the current frame
    current_detections = {cls: False for cls in ALERT_CLASSES}
    
    # Main detection loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error reading from camera")
            break
        
        # Reset current detections for this frame
        for cls in ALERT_CLASSES:
            current_detections[cls] = False
        
        # Perform detection on the frame
        results = model(frame, conf=args.conf)
        
        # Process detection results
        for r in results:
            boxes = r.boxes  # Bounding boxes
            
            # Loop through detected objects
            for box in boxes:
                cls_id = int(box.cls[0])  # Get class ID
                cls_name = model.names[cls_id].lower()  # Get class name (lowercase)
                conf = float(box.conf[0])  # Detection confidence
                
                # Check if the detected class should trigger an alert
                if cls_name in ALERT_CLASSES:
                    # Mark this class as detected in the current frame
                    current_detections[cls_name] = True
                    
                    # Draw bounding box and label
                    xyxy = box.xyxy[0].cpu().numpy()  # Box coordinates
                    color = class_colors.get(cls_name, (255, 255, 255))  # Get color or default to white
                    label = f"{cls_name} {conf:.2f}"
                    
                    # Draw box
                    cv2.rectangle(
                        frame, 
                        (int(xyxy[0]), int(xyxy[1])), 
                        (int(xyxy[2]), int(xyxy[3])), 
                        color, 
                        2
                    )
                    
                    # Draw label background
                    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    cv2.rectangle(
                        frame,
                        (int(xyxy[0]), int(xyxy[1]) - text_size[1] - 10),
                        (int(xyxy[0]) + text_size[0], int(xyxy[1])),
                        color,
                        -1  # Fill rectangle
                    )
                    
                    # Draw text
                    cv2.putText(
                        frame, 
                        label, 
                        (int(xyxy[0]), int(xyxy[1]) - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, 
                        (255, 255, 255), 
                        2
                    )
        
        # Update detection states and trigger alerts if needed
        for cls_name in ALERT_CLASSES:
            if alert_manager.update_detection(cls_name, current_detections[cls_name]):
                alert_manager.sound_alert(f"Alert! {cls_name} detected")
        
        # Display status information on frame
        cv2.putText(
            frame,
            "AlertAI - Press 'q' to exit", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (255, 255, 255), 
            2
        )
        
        # Show the frame with detections
        cv2.imshow('AlertAI - Drowsiness Detection', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print("AlertAI terminated")

if __name__ == "__main__":
    main()
