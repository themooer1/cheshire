# Integration Tests

These tests verify light control by reading the actual light output with a webcam.

## Hardware Requirements

- **BLE smart light** (Keepsmile/LuckyStyle/Leeleberd compatible)
- **USB webcam** (or any camera supported by OpenCV)
- **Bluetooth adapter** (BLE-capable)
- **Opaque box** to isolate the camera and light from ambient light

## Setup

1. **Prepare the test box**: Place the camera and light inside an opaque box
   (e.g., a cardboard box) so the camera only sees the light output.
   Ambient light will cause false readings.

2. **Connect the camera**: Plug in the USB webcam and note its device index.
   Common indices are `0`, `1`, or `2`. You can test with:
   ```bash
   ~/projects/cheshire-homeassistant/agent_tools/.venv/bin/python \
     ~/projects/cheshire-homeassistant/agent_tools/webcam_avg_color.py 0
   ```
   Try incrementing the index if you get an error.

3. **Find your device name**: Run the BLE scanner:
   ```bash
   python -m cheshire.tools.ble_scan
   # or
   python smile.py
   ```
   Look for your light's name (e.g., `KS03~B59CBE`).

4. **Set camera index** (if not `0`):
   ```bash
   export CAMERA_INDEX=1
   ```

## Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run with device name
python -m pytest tests/test_integration.py --target-device KS03~B59CBE -v

# Or use environment variable
TARGET_DEVICE=KS03~B59CBE python -m pytest tests/test_integration.py -v
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Device not found` | Ensure the light is powered on and in range. Run `ble_scan` to verify. |
| `Could not open camera` | Check camera index with `ls /dev/video*`. Try indices 0, 1, 2. |
| `Webcam tool failed` | Ensure the webcam venv exists: `cd ~/projects/cheshire-homeassistant/agent_tools && uv sync` |
| Colors look wrong | Make sure the box is fully closed. Ambient light contaminates readings. |
| Tests flaky | Increase sleep times in the test or ensure the light has fully settled before reading. |
| `ModuleNotFoundError: cheshire` | Run `pip install -e .` from the cheshire project root. |
