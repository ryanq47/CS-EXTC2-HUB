from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid
import logging
from datetime import datetime
# Create SQLite DB
engine = create_engine('sqlite:///controllers.db', echo=False)  # echo=True for debug logging
Base = declarative_base()

# Define ORM model
class RunningControllers(Base):
    __tablename__ = 'running_controllers'

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pid = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow)  # Automatically set on insert

# Create the table
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def delete_controller(uuid_str):
    session = Session()
    try:
        controller = session.query(RunningControllers).filter_by(uuid=uuid_str).first()
        if controller:
            session.delete(controller)
            session.commit()
            logging.info(f"Controller {uuid_str} removed from DB.")
        else:
            logging.info(f"No controller found with UUID {uuid_str}")
    except Exception as e:
        session.rollback()
        logging.info("Error:", e)
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
        logging.info(f"controller {uuid_str} added.")
    except Exception as e:
        session.rollback()
        logging.info("Error:", e)
    finally:
        session.close()

def get_all_running_controllers():
    session = Session()
    try:
        controllers = session.query(RunningControllers).all()
        return [
            {
                "uuid": controller.uuid,
                "pid": controller.pid,
                "started_at": controller.started_at.isoformat()
            }
            for controller in controllers
        ]
    except Exception as e:
        logging.info("Error fetching controllers:", e)
        return []
    finally:
        session.close()

def get_controller_by_uuid(uuid_str):
    session = Session()
    try:
        controller = session.query(RunningControllers).filter_by(uuid=uuid_str).first()
        if controller:
            return {
                    "uuid": controller.uuid,
                    "pid": controller.pid,
                    "started_at": controller.started_at.isoformat()
                }
        else:
            logging.info(f"No controller found with UUID {uuid_str}")
            return None
    except Exception as e:
        logging.info("Error during DB lookup:", e)
        return None
    finally:
        session.close()
