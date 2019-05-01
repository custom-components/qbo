# Qbo Coffee Maker
## Installation
1. Place the component's files in `custom_components/qbo/`
2. Add the following to your `configuration.yaml`:
```yaml
qbo:
  url: "https://{{YOUR_QBO_HOST_NAME_OR_IP}}/"
  sensor:
    - enabled: true
```