from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from nexus_e_interface import Scenario

def main():
    engine = create_engine(
        "mysql://"
        + "admin:54565456"
        + "@localhost:3306"
        + "/nexuse_s9_250321_ty24_noevf_xbntc"
    )
    session=Session(engine)
    scenario = Scenario(session=session)
    print(scenario.db_info)

if __name__ == "__main__":
    main()