from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

# Create SQLite DB
engine = create_engine('sqlite:///connectors.db', echo=True)  # echo=True for debug logging
Base = declarative_base()

# Define ORM model
class Agent(Base):
    __tablename__ = 'connectors'

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    port = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    teamserver_ip = Column(String, nullable=False)
    teamserver_port = Column(Integer, nullable=False)

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

def delete_agent(uuid_str):
    session = Session()
    try:
        agent = session.query(Agent).filter_by(uuid=uuid_str).first()
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

def add_or_update_agent(uuid_str, name, ip, port, status, teamserver_ip, teamserver_port):
    session = Session()
    try:
        agent = session.query(Agent).filter_by(uuid=uuid_str).first()

        if agent:
            # Update existing agent
            agent.name = name
            agent.ip = ip
            agent.port = port
            agent.status = status
            agent.teamserver_ip = teamserver_ip
            agent.teamserver_port = teamserver_port
        else:
            # Insert new agent
            agent = Agent(
                uuid=uuid_str,
                name=name,
                ip=ip,
                port=port,
                status=status,
                teamserver_ip=teamserver_ip,
                teamserver_port=teamserver_port
            )
            session.add(agent)

        session.commit()
        print(f"Agent {uuid_str} added or updated.")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()