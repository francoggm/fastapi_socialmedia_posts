from fastapi import FastAPI
from dotenv import load_dotenv

from . import models
from .database import engine
from .routers import post, user

load_dotenv()
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

# tries = 0
# while tries < 3:
#     try:
#         conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user=os.getenv('USER'), 
#         password=os.getenv('PASSWORD'), cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('DB Connected')
#         break
#     except Exception as e:
#         print('Error connecting DB ->', e, '\nTrying again!')
#         sleep(2)
#         tries += 1
#         if tries == 3:
#             print('Exceded tries, error connecting DB')




    

