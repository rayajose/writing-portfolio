from fastapi import HTTPException

from webhooks.events import SUPPORTED_WEBHOOK_EVENTS


def validate_webhook_events(events: list[str]) -> None:
    invalid_events = [
        event for event in events if event not in SUPPORTED_WEBHOOK_EVENTS
    ]

    if invalid_events:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Unsupported webhook event type.",
                "invalid_events": invalid_events,
                "supported_events": sorted(SUPPORTED_WEBHOOK_EVENTS),
            },
        )
