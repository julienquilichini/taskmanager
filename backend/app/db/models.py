from datetime import datetime, UTC
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.engine import Base


class OutboundCall(Base):
    __tablename__ = "outbound_calls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    call_sid: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True)

    instructions: Mapped[str] = mapped_column(Text)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    greeting: Mapped[str] = mapped_column(Text, default="Allo")

    status: Mapped[str] = mapped_column(String, default="created")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    