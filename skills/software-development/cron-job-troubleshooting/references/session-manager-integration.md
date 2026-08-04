# Session Manager + Weather Integration Pattern

## Overview
The `time_location_weather.zip` package adds two capabilities to Hermes:
1. **Weather data** (Rust) — fetches current weather from Open-Meteo and injects it into the `[CTX]` block alongside time/location/solar position.
2. **Daily session management** (Python) — detects first interaction of the day, creates a session JSON file, fetches a weather snapshot, and tracks turn count and last activity.

## Files Installed
| File | Destination | Purpose |
|---|---|---|
| `session_manager.py` | `~/.hermes/tools/session_manager.py` | Daily session tracking + weather snapshot |
| `sessions.toml` | `~/.hermes/config/sessions.toml` | Configuration (timezone, lat/lon, weather toggle) |
| `weather.rs` | `~/weather.rs` (pending) | Rust module for agent-unified integration |
| `agent.toml.additions` | `~/.hermes/config/agent.toml.additions` | `[weather]` and `[session]` config sections |

## Session Manager Usage
```bash
python ~/.hermes/tools/session_manager.py
# Output: JSON with date, created_at, last_active, timezone, turn_count, weather_at_creation, freshly_created
```

- `freshly_created: true` — first interaction of the day
- `freshly_created: false` — continuation of existing session
- `turn_count` increments on each call within the same day
- Weather snapshot captured only at session creation (not on every turn)

## Weather Data (Open-Meteo)
- Free, no API key required
- Endpoint: `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true`
- Returns: temperature, windspeed, winddirection, is_day, weathercode
- Weather codes mapped to Arabic descriptions (0=clear, 1-3=partly cloudy, etc.)

## Integration with agent-unified (Rust)
1. Copy `weather.rs` to `agent-unified/src/weather.rs`
2. Add `mod weather;` in `main.rs` or `lib.rs`
3. Add dependencies to `Cargo.toml`: `reqwest`, `serde`, `tokio`, `anyhow`
4. In the `[CTX]` block builder, call `WeatherCache::get(lat, lon).await` and `format_for_ctx(&w)`
5. Add `[weather]` and `[session]` sections to `agent.toml`

## Storage
Each day = one JSON file at `~/.hermes/sessions/YYYY-MM-DD.json`. No SQLite needed. Files are independent and never touch previous days.