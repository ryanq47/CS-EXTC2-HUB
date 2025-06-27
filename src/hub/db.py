from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

# Create SQLite DB
engine = create_engine('sqlite:///controllers.db', echo=True)  # echo=True for debug logging
Base = declarative_base()

# Define ORM model
class RunningControllers(Base):
    __tablename__ = 'running_controllers'

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pid = Column(Integer)


# Create the table
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


#use: 
# add_or_update_agent(
#     uuid_str="123e4567-e89b-12d3-a456-426614174000",
#     name="Agent007",
#     ip="192.168.1.100",
#     port=8080,
#     status="active",
#     teamserver_ip="10.0.0.2",
#     teamserver_port=4444
# )
#delete_agent(uuid)

def delete_controller(uuid_str):
    session = Session()
    try:
        agent = session.query(RunningControllers).filter_by(uuid=uuid_str).first()
        if agent:
            session.delete(agent)
            session.commit()
            print(f"Agent {uuid_str} deleted.")
        else:
            print(f"No agent found with UUID {uuid_str}")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()

def add_running_controller(uuid_str, pid):
    session = Session()
    try:
        controller = session.query(RunningControllers).filter_by(uuid=uuid_str).first()

        # Insert new agent
        controller = RunningControllers(
            uuid=uuid_str,
            pid=pid
            
        )
        session.add(controller)

        session.commit()
        print(f"controller {uuid_str} added.")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()

def get_all_running_controllers():
    session = Session()
    try:
        controllers = session.query(RunningControllers).all()
        return [controller.uuid for controller in controllers]
    except Exception as e:
        print("Error fetching controllers:", e)
        return []
    finally:
        session.close()

def get_controller_by_uuid(uuid_str):
    session = Session()
    try:
        controller = session.query(RunningControllers).filter_by(uuid=uuid_str).first()
        if controller:
            return controller
        else:
            print(f"No controller found with UUID {uuid_str}")
            return None
    except Exception as e:
        print("Error during DB lookup:", e)
        return None
    finally:
        session.close()
