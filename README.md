# Sopor.nu Home Assistant Integration

A custom Home Assistant integration that provides recycling station data from [Sopor.nu](https://www.sopor.nu) (Sweden's national waste portal by Avfall Sverige).

Each recycling station becomes a device in Home Assistant with sensors for every service type — showing when each waste type was last emptied and when the next emptying is scheduled.

## Sensors

For each station, sensors are created for the available service types:

| Service | Icon | Description |
|---------|------|-------------|
| Paper packaging | 📦 | Pappersförpackningar |
| Plastic packaging | 🧴 | Plastförpackningar |
| Metal packaging | 🥫 | Metallförpackningar |
| Clear glass | 🍾 | Ofärgade glasförpackningar |
| Colored glass | 🍷 | Färgade glasförpackningar |
| Newspapers | 📰 | Tidningar och andra trycksaker |
| Batteries | 🔋 | Batterier |
| Textiles | 👕 | Textilier |
| Cleaning | 🧹 | Städning |
| Snow removal | ❄️ | Snöröjning |

Each sensor's **state** is the next scheduled action date (device class `timestamp`), making it easy to use in automations.

**Attributes** on each sensor include:

- `last_action` — when the service was last performed
- `next_action` — when the next service is scheduled
- `last_action_alt_text` / `next_action_alt_text` — free-text schedule info
- `extra_info` — additional details
- `responsible` — the company responsible for the service
- `service_name_sv` — Swedish name of the service type
- `number_of_containers` — how many containers exist for this type

## Installation

### HACS (recommended)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** > **Custom repositories** (three-dot menu in the top right).
3. Add this repository URL: `https://github.com/ollelindeman/probable-lamp`
4. Select category **Integration** and click **Add**.
5. Search for **Sopor.nu** in HACS and click **Download**.
6. Restart Home Assistant.

### Manual

1. Copy the `custom_components/sopor_nu` folder into your Home Assistant `custom_components` directory:

   ```
   <ha-config>/
   └── custom_components/
       └── sopor_nu/
           ├── __init__.py
           ├── api.py
           ├── config_flow.py
           ├── const.py
           ├── coordinator.py
           ├── manifest.json
           ├── sensor.py
           ├── strings.json
           └── translations/
               └── en.json
   ```

2. Restart Home Assistant.

## Setup

1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for **Sopor.nu**.
3. Select your **municipality** (kommun) from the dropdown list.
4. Select the **recycling station** you want to monitor.
5. The station appears as a device with one sensor per service type.

You can add multiple stations by repeating the process.

## Data updates

The integration polls the Avfallshubben API every **6 hours**. Recycling station schedules don't change frequently, so this keeps API load minimal while keeping data reasonably fresh.

## API

This integration uses the public (unauthenticated) Avfallshubben API operated by Avfall Sverige:

- `GetAllAVS` — list of all recycling stations in Sweden
- `GetAVS` — detailed service/schedule data for a specific station

No API key is required.
