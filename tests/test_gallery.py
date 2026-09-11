import numpy as np
from app.models.database import Base, Student, engine, SessionLocal
from app.services.gallery import append_gallery, gallery_index

def test_incremental_gallery_update():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    db=SessionLocal(); db.add(Student(roll_no="1", name="One")); db.commit()
    gallery_index.entries=[]; append_gallery(db,"1",np.array([1,0],dtype=np.float32),"x","manual_label"); db.commit()
    assert gallery_index.search(np.array([.9,.1],dtype=np.float32))[0] == "1"
    assert db.get(Student,"1").gallery_embedding_count == 1
    db.close()
