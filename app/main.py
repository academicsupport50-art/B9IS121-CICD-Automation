"""CloudOps Deployment API for B9IS121 CI/CD demonstration."""
import logging, os, uuid
from typing import Any
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

APP_NAME="CloudOps Deployment API"
APP_VERSION="1.0.0"
BUILD_SHA=os.getenv("BUILD_SHA","local")
APP_ENV=os.getenv("APP_ENV","development")
logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO").upper())
logger=logging.getLogger("cloudops_api")
app=FastAPI(title=APP_NAME,version=APP_VERSION,description="Stateless CI/CD demonstration API")
RESOURCES=[
 {"id":"github","name":"GitHub","role":"Source control"},
 {"id":"actions","name":"GitHub Actions","role":"Pipeline automation"},
 {"id":"docker","name":"Docker","role":"Containerisation"},
 {"id":"artifact-registry","name":"Artifact Registry","role":"Image registry"},
 {"id":"cloud-run","name":"Cloud Run","role":"Cloud hosting"},
]
class EchoRequest(BaseModel):
 message:str=Field(min_length=1,max_length=200)
 correlation_id:str|None=Field(default=None,max_length=64)
@app.middleware("http")
async def harden_response(request:Request,call_next):
 request_id=request.headers.get("x-request-id") or uuid.uuid4().hex
 response=await call_next(request)
 response.headers["X-Request-ID"]=request_id
 response.headers["X-Content-Type-Options"]="nosniff"
 response.headers["X-Frame-Options"]="DENY"
 response.headers["Referrer-Policy"]="no-referrer"
 response.headers["Cache-Control"]="no-store"
 logger.info("method=%s path=%s status=%s request_id=%s",request.method,request.url.path,response.status_code,request_id)
 return response
@app.get("/")
def root()->dict[str,Any]:
 return {"service":APP_NAME,"version":APP_VERSION,"status":"operational","links":{"health":"/healthz","info":"/api/v1/info","resources":"/api/v1/resources","documentation":"/docs"}}
@app.get("/healthz")
def health()->dict[str,str]: return {"status":"ok"}
@app.get("/api/v1/info")
def info()->dict[str,str]:
 return {"service":APP_NAME,"version":APP_VERSION,"environment":APP_ENV,"build_sha":BUILD_SHA,"platform":"cloud-run" if os.getenv("K_SERVICE") else "local-or-container"}
@app.get("/api/v1/resources")
def resources()->dict[str,Any]: return {"count":len(RESOURCES),"items":RESOURCES}
@app.get("/api/v1/resources/{resource_id}")
def resource(resource_id:str)->dict[str,str]:
 for item in RESOURCES:
  if item["id"]==resource_id:return item
 raise HTTPException(status_code=404,detail="Resource not found")
@app.post("/api/v1/echo")
def echo(payload:EchoRequest)->dict[str,Any]:
 return {"received":True,"message":payload.message,"correlation_id":payload.correlation_id}
