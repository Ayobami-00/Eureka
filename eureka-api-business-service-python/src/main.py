import asyncio
import logging

import grpc

from src.protos import business_pb2_grpc
from src.protos import business_pb2
from src.gapi.business_service import BusinessService

from grpc_reflection.v1alpha import reflection

from src.core.container import Container

async def serve() -> None:
    server = grpc.aio.server()
    business_pb2_grpc.add_BusinessServiceServicer_to_server(BusinessService(), server)
    listen_addr = '0.0.0.0:50051'
    SERVICE_NAMES = (
        business_pb2.DESCRIPTOR.services_by_name['BusinessService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()
    
    
if __name__ == '__main__':
    container = Container()
    db = container.db()
    db.create_database()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

    