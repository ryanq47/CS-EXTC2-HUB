from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid
import structlog
from datetime import datetime

logger = structlog.get_logger(__name__)

# Create SQLite DB
engine = create_engine('sqlite:///controllers.db', echo=False)  # echo=True for debug logger
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
            logger.info(f"Controller {uuid_str} removed from DB.")
        else:
            logger.info(f"No controller found with UUID {uuid_str}")
    except Exception as e:
        session.rollback()
        logger.info("Error:", e)
    finally:
        session.close()

def add_running_controller(uuid_str, pid):
    session = Session()
    try:
        controller = session.query(RunningControllers).filter_by(uuid=uuid_str).first()

        if controller:
            # Update existing entry
            controller.pid = pid
            controller.started_at = datetime.utcnow()  # Optionally reset timestamp
            logger.info(f"Controller {uuid_str} updated.")
        else:
            # Insert new entry
            controller = RunningControllers(
                uuid=uuid_str,
                pid=pid
            )
            session.add(controller)
            logger.info(f"Controller {uuid_str} added.")

        session.commit()
    except Exception as e:
        session.rollback()
        logger.info("Error:", e)
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
        logger.info("Error fetching controllers:", e)
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
            logger.info(f"No controller found with UUID {uuid_str}")
            return None
    except Exception as e:
        logger.info("Error during DB lookup:", e)
        return None
    finally:
        session.close()
