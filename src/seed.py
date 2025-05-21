import asyncio
from src.common.database import async_session_maker
from src.building.models import Building
from src.activity.models import Activity, OrganizationActivity
from src.organization.models import Organization, OrganizationPhone


async def seed():
    async with async_session_maker() as session:
        # Здания
        building1 = Building(
            address="г. Москва, ул. Ленина, 1", latitude=55.7558, longitude=37.6173
        )
        building2 = Building(
            address="г. Санкт-Петербург, Невский проспект, 10",
            latitude=59.9386,
            longitude=30.3141,
        )
        building3 = Building(
            address="г. Новосибирск, Красный проспект, 50",
            latitude=55.0302,
            longitude=82.9204,
        )
        session.add_all([building1, building2, building3])
        await session.flush()

        # Деятельности
        food = Activity(name="Еда")
        meat = Activity(name="Мясная продукция", parent=food)
        milk = Activity(name="Молочная продукция", parent=food)
        auto = Activity(name="Автомобили")
        trucks = Activity(name="Грузовые", parent=auto)
        cars = Activity(name="Легковые", parent=auto)
        parts = Activity(name="Запчасти", parent=cars)
        accessories = Activity(name="Аксессуары", parent=cars)
        session.add_all([food, meat, milk, auto, trucks, cars, parts, accessories])
        await session.flush()

        # Организации
        org1 = Organization(name="ООО Молочные продукты", building=building1)
        org2 = Organization(name="ЗАО Мясной Дом", building=building2)
        org3 = Organization(name="ИП АвтоМир", building=building3)
        session.add_all([org1, org2, org3])
        await session.flush()

        # Телефоны
        session.add_all(
            [
                OrganizationPhone(phone="8-800-555-35-35", organization=org1),
                OrganizationPhone(phone="8-800-111-22-33", organization=org2),
                OrganizationPhone(phone="8-913-123-45-67", organization=org3),
                OrganizationPhone(phone="2-222-222", organization=org1),
            ]
        )
        await session.flush()

        # Связи организация-деятельность
        session.add_all(
            [
                OrganizationActivity(organization_id=org1.id, activity_id=milk.id),
                OrganizationActivity(organization_id=org2.id, activity_id=meat.id),
                OrganizationActivity(organization_id=org3.id, activity_id=parts.id),
                OrganizationActivity(
                    organization_id=org3.id, activity_id=accessories.id
                ),
            ]
        )
        await session.commit()
        print("Тестовые данные успешно добавлены")


if __name__ == "__main__":
    asyncio.run(seed())
