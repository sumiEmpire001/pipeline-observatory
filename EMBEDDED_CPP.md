# Embedded C++ companion

Fixed-memory CI/telemetry run health counters; strict nonoverlapping timestamps, invalid-state latching and overflow rejection. Unlike Python, accepts already parsed integer millisecond timestamps; does not parse JSON or timezone-aware strings.

## Host verification

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
python -m unittest discover -s tests -v
```

The C++11 header is allocation-free and uses no Arduino-specific APIs. Integrators may include `cpp/include/EmbeddedCore.h` in Arduino Uno or ESP32 sketches, but **firmware builds and physical-board tests are not yet verified**. Use advisory LEDs only; never directly switch mains, motors or safety-critical actuators. Handle sensor disconnection, time rollover, watchdog resets, retained configuration and electrical isolation separately. CI verifies host C++ and existing Python tests, not device behavior.
