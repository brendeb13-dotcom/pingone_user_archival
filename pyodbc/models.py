from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlphaUser(BaseModel):
    id: str
    rev: Optional[str] = None
    custom_regcompanyname: Optional[str] = None
    frunindexedstring1: Optional[str] = None
    frunindexedstring2: Optional[str] = None
    frunindexedstring3: Optional[str] = None
    frunindexedstring4: Optional[str] = None
    frunindexedstring5: Optional[str] = None
    frindexedstring11: Optional[str] = None
    frindexedstring12: Optional[str] = None
    frindexedstring10: Optional[str] = None
    frindexedstring19: Optional[str] = None
    frindexedstring17: Optional[str] = None
    frindexedstring18: Optional[str] = None
    frindexedstring15: Optional[str] = None
    frindexedstring16: Optional[str] = None
    frindexedstring13: Optional[str] = None
    frindexedstring14: Optional[str] = None
    givenname: Optional[str] = None
    frindexedstring20: Optional[str] = None
    telephonenumber: Optional[str] = None
    city: Optional[str] = None
    displayname: Optional[str] = None
    accountstatus: Optional[str] = None
    sn: Optional[str] = None
    frunindexeddate1: Optional[datetime] = None
    frindexedstring9: Optional[str] = None
    frindexedstring8: Optional[str] = None
    frindexedstring7: Optional[str] = None
    frindexedstring6: Optional[str] = None
    passwordlastchangedtime: Optional[datetime] = None
    country: Optional[str] = None
    mail: Optional[str] = None
    frindexeddate5: Optional[datetime] = None
    frindexeddate4: Optional[datetime] = None
    frindexeddate3: Optional[datetime] = None
    frindexedstring5: Optional[str] = None
    frindexedstring4: Optional[str] = None
    frindexedstring3: Optional[str] = None
    frindexedstring2: Optional[str] = None
    frindexedstring1: Optional[str] = None
    frunindexedinteger3: Optional[int] = None
    frunindexedinteger2: Optional[int] = None
    frunindexedinteger1: Optional[int] = None
    description: Optional[str] = None
    frindexedinteger4: Optional[int] = None
    frindexedinteger3: Optional[int] = None
    frindexedinteger2: Optional[int] = None
    frindexedinteger1: Optional[int] = None
    frindexedinteger5: Optional[int] = None
    username: Optional[str] = None
    frindexeddate2: Optional[datetime] = None
    frindexeddate1: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobLog(BaseModel):
    job_id: int
    job_type: str
    run_timestamp: datetime
    status: str
    message: Optional[str] = None
    records_inserted: Optional[int] = 0
    records_updated: Optional[int] = 0
    records_archived: Optional[int] = 0
    source_file_name: Optional[str] = None
    class Config:
        from_attributes = True