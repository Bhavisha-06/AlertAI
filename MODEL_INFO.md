# Model Information

## Overview

The `best.pt` model included in this repository is a YOLOv8 model trained to detect signs of drowsiness and distraction. The model can identify the following classes:

- **drowsy**: Detects when a person appears to be drowsy (eyes partially closed)
- **head drop**: Identifies when a person's head drops down (nodding off)
- **yawn**: Recognizes yawning, which can be a sign of fatigue
- **distracted**: Detects when a person is not focusing on the road/task

## Model Details

- Architecture: YOLOv8
- Format: PyTorch (.pt)
- Training Platform: Roboflow
- Input Resolution: 640x640 pixels

## Using the Model

The model file (`best.pt`) should be kept in the root directory of the project. The main script (`alert_ai.py`) will automatically load this model file when run.

If you want to use a different model file, you can specify it with the `--model` argument:

```bash
python alert_ai.py --model path/to/your/model.pt
```

## Detection Sensitivity

You can adjust the detection sensitivity by changing these command-line parameters:

- `--conf`: Detection confidence threshold (default: 0.5)
- `--detection-time`: Required continuous detection time in seconds (default: 1.5)
- `--cooldown`: Cooldown period between alerts (default: 5)

Example:
```bash
python alert_ai.py --conf 0.6 --detection-time 1.0 --cooldown 3
```

## Fine-tuning

If you wish to fine-tune the model for your specific environment:

1. Collect additional data in your target environment
2. Use YOLOv8's fine-tuning capabilities to update the model
3. Replace the `best.pt` file with your newly trained model

## Model Performance

The model performs best in well-lit environments with a clear view of the subject's face. Performance may degrade in low-light conditions or when the face is partially obscured.
