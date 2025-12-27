from fastapi import APIRouter, HTTPException
from .database import SessionLocal
from .models import Certificate, CertStatus
from datetime import datetime

api_router = APIRouter(prefix="/api", tags=["certificates"])

@api_router.get("/certificates")
def get_certificates():
    session = SessionLocal()
    certs = session.query(Certificate).all()
    result = [
        {
            "id": c.id,
            "issuer": c.issuer,
            "cn": c.cn,
            "valid_until": c.valid_until.isoformat(),
            "status": c.status.value,
            "certificate": c.certificate,
            "chain": c.chain,
            "csr": c.csr
        } for c in certs
    ]
    session.close()
    return result

@api_router.post("/job/sync")
def trigger_sync():
    from .scheduler import sync_certificates
    # Sync einmal auslösen (manuell)
    sync_certificates()
    return {"message": "Sync triggered"}

@api_router.post("/certificates/{cert_id}/deploy")
def deploy_certificate(cert_id: str):
    # Dummy-Action: Deployment loggen/triggern
    return {"message": f"Deployment triggered for {cert_id}"}

@api_router.post("/certificates/{cert_id}/csr")
def new_csr(cert_id: str):
    # Dummy-Action: neuen CSR generieren (hier nur Dummy)
    return {"message": f"New CSR generated for {cert_id}"}