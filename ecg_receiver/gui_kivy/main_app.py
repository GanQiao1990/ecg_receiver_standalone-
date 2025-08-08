import os
import time
from collections import deque

import numpy as np

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle

# Import core modules from the project
from ecg_receiver.core.serial_handler import SerialHandler
from ecg_receiver.core.data_recorder import DataRecorder


class ECGPlot(Widget):
    """Lightweight ECG plotting widget using Kivy canvas."""

    def __init__(self, max_points=2000, **kwargs):
        super().__init__(**kwargs)
        self.max_points = max_points
        self.data = deque(maxlen=max_points)
        self.line = None
        self.bg_rect = None
        self._min_y = -1.0
        self._max_y = 1.0

        with self.canvas.before:
            Color(1, 1, 1, 1)  # white background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        if self.bg_rect is not None:
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
        # Redraw when size changes
        self.redraw()

    def clear(self):
        self.data.clear()
        self.redraw()

    def append(self, value: float):
        self.data.append(value)

    def set_minmax(self, mn: float, mx: float):
        # Avoid zero range
        if mx <= mn:
            mx = mn + 1.0
        self._min_y, self._max_y = mn, mx

    def redraw(self):
        # Draw ECG polyline
        self.canvas.remove_group('ecg')
        if not self.data:
            with self.canvas:
                Color(0.8, 0.8, 0.8, 1, group='ecg')
                # Midline
                y = self.y + self.height / 2
                Line(points=[self.x, y, self.right, y], width=1.0, group='ecg')
            return

        points = list(self.data)
        n = len(points)
        if n < 2:
            return

        # Dynamic scaling with small margin
        data_arr = np.array(points, dtype=float)
        dmin, dmax = float(np.min(data_arr)), float(np.max(data_arr))
        padding = (dmax - dmin) * 0.1 if dmax > dmin else 1.0
        ymin = dmin - padding
        ymax = dmax + padding
        self.set_minmax(ymin, ymax)

        w = float(self.width)
        h = float(self.height)
        if w <= 2 or h <= 2:
            return

        x0 = float(self.x)
        y0 = float(self.y)
        dx = w / (n - 1)
        rng = (self._max_y - self._min_y)
        if rng <= 0:
            rng = 1.0

        # Build polyline points
        pts = []
        for i, v in enumerate(points):
            x = x0 + i * dx
            # Map value to widget Y space (flip so higher values at top)
            y = y0 + (v - self._min_y) / rng * h
            pts.extend((x, y))

        with self.canvas:
            Color(0.0, 0.3, 1.0, 1, group='ecg')  # blue line
            Line(points=pts, width=1.2, group='ecg')


class ECGReceiverUI(BoxLayout):
    """Main UI container for the Kivy ECG Receiver GUI."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Core components
        self.serial = SerialHandler(baudrate=57600)
        self.recorder = DataRecorder()

        # Buffers
        self.max_points = 2000
        self.ecg_buffer = deque(maxlen=self.max_points)
        self.packets_received = 0
        self.last_packet_time = None

        # Controls row
        controls = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), padding=(dp(8), dp(8)), spacing=dp(8))
        controls.add_widget(Label(text='Port:', size_hint_x=None, width=dp(60)))
        self.port_spinner = Spinner(text='Select Port', values=tuple(self.serial.list_ports()), size_hint_x=None, width=dp(200))
        controls.add_widget(self.port_spinner)

        self.refresh_btn = Button(text='Refresh Ports', size_hint_x=None, width=dp(140))
        self.refresh_btn.bind(on_release=lambda *_: self.refresh_ports())
        controls.add_widget(self.refresh_btn)

        self.connect_btn = Button(text='Connect', size_hint_x=None, width=dp(120))
        self.connect_btn.bind(on_release=lambda *_: self.toggle_connection())
        controls.add_widget(self.connect_btn)

        self.record_btn = ToggleButton(text='Start Recording', state='normal', size_hint_x=None, width=dp(160))
        self.record_btn.bind(on_release=lambda *_: self.toggle_recording())
        self.record_btn.disabled = True
        controls.add_widget(self.record_btn)

        self.add_widget(controls)

        # Status row
        status_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), padding=(dp(8), 0), spacing=dp(8))
        self.status_label = Label(text='Status: Disconnected', halign='left', valign='middle')
        self.packets_label = Label(text='Packets: 0', size_hint_x=None, width=dp(140))
        status_row.add_widget(self.status_label)
        status_row.add_widget(self.packets_label)
        self.add_widget(status_row)

        # Plot
        self.plot = ECGPlot(max_points=self.max_points)
        self.add_widget(self.plot)

        # Schedulers
        Clock.schedule_interval(self.update_plot, 1 / 30.0)  # ~30 FPS

        # Initial port scan
        self.refresh_ports()

    # ---------- UI handlers ----------
    def refresh_ports(self):
        ports = tuple(self.serial.list_ports())
        self.port_spinner.values = ports
        if ports and (self.port_spinner.text == 'Select Port' or self.port_spinner.text not in ports):
            self.port_spinner.text = ports[0]

    def toggle_connection(self):
        if not self.serial.is_connected:
            port = self.port_spinner.text.strip()
            if not port or port == 'Select Port':
                self.status_label.text = 'Status: No port selected'
                return
            self.status_label.text = f'Connecting to {port}...'
            connected = self.serial.connect(port)
            if connected:
                self.connect_btn.text = 'Disconnect'
                self.record_btn.disabled = False
                self.status_label.text = f'Status: Connected to {port}'
                self.packets_received = 0
                self.ecg_buffer.clear()
                self.plot.clear()
                # Start reading in background thread; handle data via callback
                self.serial.start_reading(self._serial_callback)
            else:
                self.status_label.text = 'Status: Connection failed'
        else:
            self.disconnect_serial()

    def disconnect_serial(self):
        if self.recorder.recording:
            self._stop_recording()
        self.serial.disconnect()
        self.connect_btn.text = 'Connect'
        self.record_btn.disabled = True
        self.status_label.text = 'Status: Disconnected'

    def toggle_recording(self):
        if not self.recorder.recording:
            if self.recorder.start_recording():
                self.record_btn.text = 'Stop Recording'
                self.status_label.text = f'Status: Recording to {os.path.basename(self.recorder.current_filename)}'
            else:
                self.status_label.text = 'Status: Could not start recording'
                self.record_btn.state = 'normal'
        else:
            self._stop_recording()

    def _stop_recording(self):
        self.recorder.stop_recording()
        self.record_btn.text = 'Start Recording'
        self.status_label.text = 'Status: Connected'

    # ---------- Serial data processing ----------
    def _serial_callback(self, line: str):
        """Called from serial background thread. Marshal to UI thread."""
        Clock.schedule_once(lambda dt: self._process_line_on_ui(line))

    def _process_line_on_ui(self, data: str):
        # Parse ECG value from various formats similar to PyQt implementation
        ecg_value = None
        try:
            if data.startswith('DATA,'):
                parts = data.split(',')
                if len(parts) >= 3:
                    ecg_value = float(parts[2])
            elif data.startswith('ERROR,') or data.startswith('INFO,'):
                # Log messages - show briefly in status
                self.status_label.text = f'Device: {data[:80]}'
                return
            else:
                # Try to parse as a single float or first token
                token = data.replace(',', ' ').split()[0]
                ecg_value = float(token)
        except Exception:
            # Ignore badly formatted lines
            return

        if ecg_value is None:
            return

        self.packets_received += 1
        self.packets_label.text = f'Packets: {self.packets_received}'
        self.last_packet_time = time.time()

        # Append to buffer
        self.ecg_buffer.append(ecg_value)

        # Write to CSV if recording
        if self.recorder.recording:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_packet_time))
            self.recorder.write_data(timestamp, ecg_value)

    # ---------- Plot updater ----------
    def update_plot(self, dt):
        if self.ecg_buffer:
            # Feed current buffer snapshot to plot
            self.plot.data = deque(self.ecg_buffer, maxlen=self.max_points)
            self.plot.redraw()
        else:
            # Occasionally display warning if no data for 5s while connected
            if self.serial.is_connected and self.last_packet_time:
                if time.time() - self.last_packet_time > 5:
                    self.status_label.text = 'Warning: No data received for 5 seconds'

    # ---------- Cleanup ----------
    def cleanup(self):
        try:
            if self.recorder.recording:
                self._stop_recording()
            if self.serial.is_connected:
                self.serial.disconnect()
        except Exception:
            pass


class ECGKivyApp(App):
    title = 'ECG Real-time Monitor (Kivy)'

    def build(self):
        self.ui = ECGReceiverUI()
        return self.ui

    def on_stop(self):
        if hasattr(self, 'ui') and self.ui:
            self.ui.cleanup()


def run_kivy_app():
    ECGKivyApp().run()
