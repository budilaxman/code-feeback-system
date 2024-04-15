from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from feedback import gen_feedback
from analysis import result

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow these HTTP methods
    allow_headers=["Content-Type", "Authorization"],  # Allow these headers
)

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

@app.post("/feedback")
def send_feedback(analysis: str):
    return { "msg" : gen_feedback(analysis) }

@app.post("/analysis")
def main(code: str):
    # a try catch block
    try:
        res = result(code)
        # catch any error
    except Exception as e:
        return {"msg": "Error: {}".format(e)}
    # if no error, return the result
    else:
        return { "msg": res }
