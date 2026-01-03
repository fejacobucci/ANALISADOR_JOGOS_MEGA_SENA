#!/usr/bin/env python3
"""Script para importar dados da Mega Sena"""

import sys
sys.path.insert(0, '/Volumes/Micro64Gb/PROJETOS/MEGA_SENA/backend')

import asyncio
from app.models.database import SessionLocal
from app.services.import_service import importar_xlsx

async def main():
    db = SessionLocal()
    try:
        file_path = '/Volumes/Micro64Gb/PROJETOS/MEGA_SENA/resultados_MegaSena.xlsx'

        print("=" * 60)
        print("  Importação de Dados da Mega Sena")
        print("=" * 60)
        print()

        async for progress in importar_xlsx(file_path, db):
            status = progress.get('status')
            message = progress.get('message', '')
            percentual = progress.get('percentual', 0)

            if status == 'processando':
                print(f"\r[{percentual:5.1f}%] {message}", end='', flush=True)
            elif status == 'concluido':
                print(f"\n\n✓ {message}")
                print(f"  Total: {progress.get('total')}")
                print(f"  Processados: {progress.get('processados')}")
                print(f"  Erros: {progress.get('erros', 0)}")
            elif status == 'erro':
                print(f"\n\n✗ ERRO: {message}")
            else:
                print(f"{message}")

        print()
        print("=" * 60)

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
