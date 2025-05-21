from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization"
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activities",
        back_populates="organizations",
    )


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    organization: Mapped["Organization"] = relationship(back_populates="phones")
