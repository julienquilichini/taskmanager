from sqlalchemy.orm import Session

from app.db.models import OutboundCall


class OutboundCallRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        call_sid: str,
        phone_number: str,
        instructions: str,
        context: str | None = None,
        greeting: str = "Allo",
    ) -> OutboundCall:
        call = OutboundCall(
            call_sid=call_sid,
            phone_number=phone_number,
            instructions=instructions,
            context=context,
            greeting=greeting,
            status="created",
        )

        self.db.add(call)
        self.db.commit()
        self.db.refresh(call)

        return call

    def get_by_call_sid(self, call_sid: str) -> OutboundCall | None:
        return (
            self.db.query(OutboundCall)
            .filter(OutboundCall.call_sid == call_sid)
            .first()
        )

    def update_status(self, call_sid: str, status: str) -> None:
        call = self.get_by_call_sid(call_sid)

        if call is None:
            return

        call.status = status
        self.db.commit()