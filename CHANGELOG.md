## v1.1.2 (2024-05-04)

### Refactor

- **example_stub_data**: catch additional potential exceptions

## v1.1.1 (2024-05-03)

### Refactor

- **demo_service**: change how pickle found is located depending on operating system

## v1.1.0 (2024-05-03)

### Feat

- **demo_service**: introduce using `pickle` to mimic database storage
- **events**: updated `/v1/events/insert` to validate and return results
- **event_models**: return a list of validation errors on bad requests

### Refactor

- **insert_event_logs**: use correct `event_id` format for system events
- **demo_service**: check lenght of event logs being inserted
- **events**: requested `size` must be greater than 0

## v1.0.0 (2024-05-02)

### BREAKING CHANGE

- `/demo/*` endpoints and all references has been removed from the application
- `/verison/*` endpoints has been removed from the application

### Feat

- **demo**: delete demo endpoints
- **events**: add new endpoints for retrieval of event logs
- **event_models**: initial event logging models

### Refactor

- **event_models**: provide examples for models and add new ones
- **versions**: delete versions endpoints
