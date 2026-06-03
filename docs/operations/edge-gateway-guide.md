# Edge gateway deployment guide

This guide explains how to deploy, configure, validate, and service an Edge Gateway device used to support remote data ingestion and operational connectivity workflows.

The Edge Gateway acts as a bridge between local partner systems and cloud-based ingestion services. The device supports secure data transmission, local buffering, operational monitoring, and remote troubleshooting.

This guide is intended for:

- Field technicians
- Integration engineers
- Operations personnel
- Support teams


## System components

The Edge Gateway deployment consists of the following components:

| Component                  | Description                                |
| -------------------------- | ------------------------------------------ |
| Edge Gateway appliance     | Primary field-deployed compute device      |
| Power supply unit (PSU)    | Provides regulated system power            |
| Network interfaces         | Supports WAN and LAN connectivity          |
| Local storage              | Buffers ingestion data during outages      |
| Cloud integration platform | Receives and processes ingestion traffic   |
| Monitoring service         | Tracks device health and operational state |


## Deployment prerequisites

Before deployment, verify the following:

- Device serial number recorded
- Deployment location approved
- Network connectivity available
- Power source verified
- Required cables and mounting hardware available
- Latest firmware package installed


### Required tools

- Phillips screwdriver
- ESD strap
- Ethernet cable tester
- Laptop with administrative access
- Console cable, if required


## Safety considerations

> WARNING  
> Disconnect power before servicing internal hardware components.

> CAUTION  
> Do not operate the device outside supported environmental conditions.


### Environmental requirements

| Requirement           | Supported range          |
| --------------------- | ------------------------ |
| Operating temperature | `0°C to 40°C`            |
| Humidity              | `10%–85%` non-condensing |
| Input voltage         | `100–240V AC`            |


## Physical installation


### Mount the device

1. Verify the installation location meets environmental requirements.
2. Secure the mounting bracket to the installation surface.
3. Attach the Edge Gateway appliance to the mounting bracket.
4. Verify airflow clearance around ventilation areas.
5. Confirm all mounting hardware is tightened securely.


### Connect power

1. Connect the PSU to the device power input.
2. Connect the PSU to a grounded power source.
3. Verify the power LED illuminates.


### Connect network interfaces

| Port   | Purpose                           |
| ------ | --------------------------------- |
| `WAN`  | External or cloud connectivity    |
| `LAN`  | Local partner system connectivity |
| `MGMT` | Administrative access             |

1. Connect the WAN interface to the upstream network.
2. Connect the LAN interface to the local system.
3. Verify link activity LEDs.


## Initial configuration


### Access the management interface

1. Connect a laptop to the `MGMT` port.
2. Open a browser and navigate to:

```text
https://192.168.1.1
```

3. Log in using deployment credentials.
4. Change the default administrator password.


### Configure network settings

Configure the following:

- Hostname
- Static IP or DHCP configuration
- DNS servers
- NTP source
- Gateway address


### Configure cloud connectivity

1. Enter the ingestion endpoint URL.
2. Upload API credentials.
3. Verify TLS certificate validation.
4. Save the configuration.


## Deployment validation

After configuration completes, validate operational readiness.


### Validation checklist

| Validation item     | Expected result |
| ------------------- | --------------- |
| Power status        | Operational     |
| WAN connectivity    | Connected       |
| Cloud registration  | Successful      |
| Local buffering     | Enabled         |
| Telemetry reporting | Active          |
| Device time sync    | Synchronized    |


### Verify cloud connectivity

Run the following validation command:

```bash
curl -X GET https://<base-url>/health
```

Expected response:

```json
{
  "status": "healthy"
}
```


## Operational workflows


### Normal operational flow

```mermaid
flowchart LR
    LocalSystem --> Gateway
    Gateway --> CloudPlatform
    CloudPlatform --> Monitoring
```


### Offline buffering workflow

If WAN connectivity is interrupted:

1. The gateway stores ingestion data locally.
2. The device enters degraded operational mode.
3. Monitoring alerts are generated.
4. Buffered data retransmits after connectivity is restored.


## Status indicators


### Front panel LEDs

| Indicator | State          | Meaning                 |
| --------- | -------------- | ----------------------- |
| Power     | Solid green    | Device operational      |
| WAN       | Blinking green | Network activity        |
| WAN       | Red            | Connectivity failure    |
| Storage   | Amber          | Buffer nearing capacity |
| Alarm     | Red            | Critical system fault   |


## Troubleshooting


### Device not powering on

| Possible cause           | Resolution                   |
| ------------------------ | ---------------------------- |
| Power cable disconnected | Verify PSU connection        |
| Failed power supply      | Replace PSU                  |
| Circuit unavailable      | Verify external power source |


### WAN connectivity failure

| Possible cause                 | Resolution                    |
| ------------------------------ | ----------------------------- |
| Network outage                 | Verify upstream connectivity  |
| Invalid DNS configuration      | Validate DNS settings         |
| Firewall restriction           | Confirm outbound access rules |
| Certificate validation failure | Verify TLS certificate        |


### Device not transmitting data

| Possible cause               | Resolution               |
| ---------------------------- | ------------------------ |
| Invalid API credentials      | Re-upload credentials    |
| Cloud endpoint unavailable   | Verify service status    |
| Local buffer full            | Clear failed queue       |
| Time synchronization failure | Verify NTP configuration |


## Operational logs


### Log locations

| Log type          | Location                 |
| ----------------- | ------------------------ |
| System logs       | `/var/log/system.log`    |
| Connectivity logs | `/var/log/network.log`   |
| Ingestion logs    | `/var/log/ingestion.log` |
| Service logs      | `/var/log/service.log`   |


### Example connectivity error

```text
ERROR: TLS handshake failed for ingestion endpoint.
```


### Example ingestion failure

```text
ERROR: Failed to transmit buffered records.
```


## Field-replaceable unit (FRU) procedures


### Replace the power supply unit

> WARNING  
> Disconnect all power before servicing hardware components.

1. Power down the device.
2. Disconnect the power cable.
3. Remove PSU retaining screws.
4. Remove the failed PSU.
5. Install the replacement PSU.
6. Secure the retaining screws.
7. Reconnect power.
8. Verify operational LEDs.


### Replace the storage module

1. Shut down the device.
2. Remove the access panel.
3. Remove the storage retention bracket.
4. Replace the storage module.
5. Reinstall the bracket and access panel.
6. Boot the system.
7. Verify storage initialization.


## Recovery workflows


### Restore a failed device

1. Replace the failed hardware component.
2. Reinstall the approved firmware image.
3. Restore the saved configuration.
4. Validate cloud connectivity.
5. Confirm telemetry reporting.


### Reprocess buffered ingestion data

1. Verify WAN connectivity is restored.
2. Confirm the buffer service is active.
3. Monitor the retransmission queue.
4. Validate successful cloud ingestion.


## Operational monitoring

The monitoring platform tracks:

- Connectivity state
- Buffer utilization
- System uptime
- Ingestion throughput
- Error conditions
- Telemetry status


### Operational states

| State    | Description                  |
| -------- | ---------------------------- |
| Healthy  | Fully operational            |
| Degraded | Limited functionality        |
| Offline  | Connectivity unavailable     |
| Failed   | Critical operational failure |


## Related documentation

- [System architecture and operational flow](../architecture/index.md)
- [Integration guide](../architecture/integration-guide.md)