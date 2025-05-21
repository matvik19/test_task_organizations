from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )

    parent: Mapped["Activity | None"] = relationship(
        back_populates="children", remote_side="Activity.id"
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activities",
        back_populates="activities",
    )


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), primary_key=True
    )
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"), primary_key=True
    )
