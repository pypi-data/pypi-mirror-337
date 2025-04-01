import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Execute a API FastAPI")
    parser.add_argument("--host", default="127.0.0.1", help="Host para executar o servidor")
    parser.add_argument("--port", type=int, default=8000, help="Porta para executar o servidor")
    args = parser.parse_args()

    uvicorn.run("minha_fastapi_lib:get_app()",
                host=args.host,
                port=args.port,
                reload=True)


if __name__ == "__main__":
    main()