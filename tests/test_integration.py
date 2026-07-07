#!/usr/bin/env python3
"""Integration tests for cheshire light control using webcam color verification."""

import asyncio
import os
import re
import subprocess

import pytest
from bleak import BleakScanner

from cheshire.compiler.state import LightState
from cheshire.generic.command import BrightnessCommand, RGBCommand, SwitchCommand
from cheshire.hal.devices import device_profile_from_ble_device

WEBCAM_TOOL = os.path.expanduser(
    "~/projects/cheshire-homeassistant/agent_tools/webcam_avg_color.py"
)
WEBCAM_PYTHON = os.path.expanduser(
    "~/projects/cheshire-homeassistant/agent_tools/.venv/bin/python"
)
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", "0"))


def get_device_name():
    return os.environ.get("TARGET_DEVICE")


@pytest.fixture(scope="session")
def device_name():
    name = get_device_name()
    if not name:
        pytest.skip(
            "No target device specified. Set TARGET_DEVICE environment variable."
        )
    return name


@pytest.fixture
async def light_connection(device_name):
    """Scan for and connect to the target BLE device."""
    devices = await BleakScanner.discover(timeout=10.0)
    target = next((d for d in devices if d.name == device_name), None)
    if target is None:
        pytest.fail(f"Device '{device_name}' not found via BLE scan.")

    profile = device_profile_from_ble_device(target)
    connection = await profile.connect(target)
    yield connection
    # Cleanup: turn off and disconnect
    state = LightState()
    state.update(SwitchCommand(on=False))
    try:
        await connection.apply(state)
    except Exception:
        pass
    try:
        await connection.disconnect()
    except Exception:
        pass


async def set_light(connection, on=True, red=255, green=255, blue=255, brightness=255):
    """Set light to a specific state."""
    state = LightState()
    state.update(SwitchCommand(on=on))
    if on:
        state.update(RGBCommand(red=red, green=green, blue=blue))
        state.update(BrightnessCommand(brightness=brightness))
    await connection.apply(state)


def get_webcam_rgb(camera_index=CAMERA_INDEX):
    """Read average RGB from the webcam tool."""
    result = subprocess.run(
        [WEBCAM_PYTHON, WEBCAM_TOOL, str(camera_index)],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Webcam tool failed: {result.stderr}")

    match = re.search(r"R:(\d+)\s+G:(\d+)\s+B:(\d+)", result.stdout)
    if not match:
        raise RuntimeError(f"Could not parse webcam output: {result.stdout}")

    return int(match.group(1)), int(match.group(2)), int(match.group(3))


async def turn_off_and_wait(connection):
    """Turn lights off and wait for them to settle."""
    await set_light(connection, on=False)
    await asyncio.sleep(2)


# --------------- Tests ---------------


@pytest.mark.asyncio
async def test_lights_on(light_connection):
    """Turning lights on should produce visible brightness."""
    await turn_off_and_wait(light_connection)
    await set_light(light_connection, on=True, red=255, green=255, blue=255)
    await asyncio.sleep(2)

    r, g, b = get_webcam_rgb()
    assert max(r, g, b) > 100, f"Lights should be on, got R:{r} G:{g} B:{b}"


@pytest.mark.asyncio
async def test_lights_off(light_connection):
    """Turning lights off should produce near-zero values."""
    await set_light(light_connection, on=False)
    await asyncio.sleep(2)

    r, g, b = get_webcam_rgb()
    assert r < 50 and g < 50 and b < 50, (
        f"Lights should be off, got R:{r} G:{g} B:{b}"
    )


@pytest.mark.asyncio
async def test_full_red(light_connection):
    """Full red should show dominant red channel."""
    await turn_off_and_wait(light_connection)
    await set_light(light_connection, on=True, red=255, green=0, blue=0)
    await asyncio.sleep(2)

    r, g, b = get_webcam_rgb()
    assert r > 150, f"Red channel too low: R:{r} G:{g} B:{b}"
    assert g < 100, f"Green channel too high: R:{r} G:{g} B:{b}"
    assert b < 100, f"Blue channel too high: R:{r} G:{g} B:{b}"


@pytest.mark.asyncio
async def test_full_green(light_connection):
    """Full green should show dominant green channel."""
    await turn_off_and_wait(light_connection)
    await set_light(light_connection, on=True, red=0, green=255, blue=0)
    await asyncio.sleep(2)

    r, g, b = get_webcam_rgb()
    assert g > 150, f"Green channel too low: R:{r} G:{g} B:{b}"
    assert r < 100, f"Red channel too high: R:{r} G:{g} B:{b}"
    assert b < 100, f"Blue channel too high: R:{r} G:{g} B:{b}"


@pytest.mark.asyncio
async def test_full_blue(light_connection):
    """Full blue should show dominant blue channel."""
    await turn_off_and_wait(light_connection)
    await set_light(light_connection, on=True, red=0, green=0, blue=255)
    await asyncio.sleep(2)

    r, g, b = get_webcam_rgb()
    assert b > 150, f"Blue channel too low: R:{r} G:{g} B:{b}"
    assert r < 100, f"Red channel too high: R:{r} G:{g} B:{b}"
    assert g < 100, f"Green channel too high: R:{r} G:{g} B:{b}"
