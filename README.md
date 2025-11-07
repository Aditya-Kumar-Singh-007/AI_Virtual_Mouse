# AI Virtual Mouse 🖱️

Control your computer mouse using hand gestures with AI-powered computer vision.

## Demo 📸

![AI Virtual Mouse in Action](SS.png)
*Screenshot showing the AI Virtual Mouse application in action with hand gesture recognition*

![AI Virtual Mouse Demo](SS.png)

## Features 🎮

- **👆 Cursor Movement**: Point with index finger to move cursor
- **✌️ Left Click**: Bring index and middle fingers together
- **👍 Right Click**: Bring thumb and index finger together
- **✊ Volume Control**: Make fist and move up/down to adjust volume
- **🤙 Brightness Control**: Raise only pinky and move up/down
- **👍 Scroll**: Raise only thumb and move up/down to scroll
- **🖐️ No Action**: Open all fingers for safe mode

## Installation 📦

1. Clone the repository:
```bash
git clone https://github.com/your-username/AI_Virtual_Mouse.git
cd AI_Virtual_Mouse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🚀

Run the application:
```bash
python Aivirtual.py
```

Press 'Q' to quit the application.

## Requirements 📋

- Python 3.7+
- Webcam
- Windows OS (for volume/brightness control)

## Dependencies 🔧

- OpenCV
- MediaPipe
- AutoPy
- NumPy
- PyCaw (for volume control)

## How It Works 🔍

The application uses MediaPipe for hand tracking and gesture recognition. Different finger combinations trigger various mouse actions:

1. **Movement**: Index finger position maps to cursor movement
2. **Clicks**: Finger proximity detection triggers clicks
3. **System Controls**: Hand gestures control volume and brightness
4. **Scrolling**: Thumb position controls scroll direction

## Troubleshooting 🛠️

- Ensure good lighting for better hand detection
- Keep hand within the purple rectangle frame
- Adjust camera position for optimal tracking
- Make sure webcam permissions are enabled

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

This project is open source and available under the MIT License.