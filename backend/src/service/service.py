import uuid

from src.core.db import session, Session
from src.model import User, Request, Data


class Service:

    @staticmethod
    def login_user(data):
        with session as s:
            user = s.query(User).filter(User.chat_id == data["id"]).first()
            if user is None:
                new_user = User(
                    chat_id=data["id"],
                    first_name=data["first_name"],
                    username=data["username"],
                    photo_url=data['photo_url'],
                )
                s.add(new_user)
                s.commit()
                return new_user

            return user

    @staticmethod
    def save_req(data):
        with Session() as session:
            try:
                new_req = Request(
                    id=uuid.uuid4(),
                    host=data.get("url"),
                    execution_time=str(data.get("execution_time")),
                    status=data.get("status"),
                    open_port=",".join(map(str, data.get("open_ports", []))),
                    vulnerabilities=data.get("vulnerabilities", []),
                    user_id=data.get("user_id"),
                )

                session.add(new_req)
                session.commit()

                return new_req

            except Exception as e:
                session.rollback()
                print(f"Error saving data: {e}")
                raise


    @staticmethod
    def history(chat_id):
        try:
            with Session() as s:
                data = s.query(Request).filter(Request.user_id == chat_id).all()
                result = [request.to_dict() for request in data]

                return result
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    @staticmethod
    def save_poc_or_ext(data, name):
        try:
            with Session() as s:
                for exploit in data.get('exploits', []):
                    # Check if the exploit already exists based on unique ID or URL
                    existing_exploit = (
                        s.query(Data)
                        .filter(Data.href == exploit.get('href'))
                        .first()
                    )

                    if existing_exploit:
                        print(f"⚠️ Exploit with href '{exploit.get('href')}' already exists. Skipping.")
                        continue

                    # Create a new record if it doesn't exist
                    new_req = Data(
                        id=uuid.uuid4(),
                        title=exploit.get('title'),
                        score=exploit.get('score'),
                        href=exploit.get('href'),
                        types=exploit.get('type'),
                        published=exploit.get('published'),
                        language=exploit.get('language'),
                        source=exploit.get('source') ,
                        name=name
                    )
                    s.add(new_req)

                s.commit()
                print("✅ Exploits successfully saved.")
        except Exception as e:
            print(f"❌ Error saving exploits: {e}")

    @staticmethod
    def all_data(name):
        try:
            with Session() as s:
                data = s.query(Data).filter(Data.name == name).all()
                result = [request.to_dict() for request in data]

                return result
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
