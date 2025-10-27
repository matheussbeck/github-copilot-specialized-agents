#!/usr/bin/env python3
"""
Instalador de GitHub Copilot Agents
Baixa e instala sistema de agents do GitHub em projetos locais
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import urllib.request
import zipfile
import tempfile


class Colors:
    """Cores para output no terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{msg}{Colors.RESET}")


def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")


def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


class CopilotAgentInstaller:
    """Gerencia instalação do sistema de agents"""
    
    def __init__(self, target_dir: str, github_url: str, force: bool = False, backup: bool = True):
        self.target_dir = Path(target_dir).resolve()
        self.github_url = github_url
        self.force = force
        self.backup = backup
        self.temp_dir = None
        self.backup_dir = None
        
    def validate_target(self):
        """Valida diretório de destino"""
        if not self.target_dir.exists():
            print_error(f"Diretório não existe: {self.target_dir}")
            return False
        
        if not self.target_dir.is_dir():
            print_error(f"Caminho não é um diretório: {self.target_dir}")
            return False
        
        print_success(f"Diretório válido: {self.target_dir}")
        return True
    
    def check_existing_installation(self):
        """Verifica se já existe instalação"""
        copilot_file = self.target_dir / ".github" / "copilot-instructions.md"
        copilot_dir = self.target_dir / ".copilot"
        
        exists = copilot_file.exists() or copilot_dir.exists()
        
        if exists:
            if self.force:
                print_warning("Instalação existente será sobrescrita (--force)")
                return True
            else:
                print_error("Instalação já existe!")
                print_info("Use --force para sobrescrever ou --backup=false para não fazer backup")
                return False
        
        return True
    
    def create_backup(self):
        """Cria backup da instalação existente"""
        if not self.backup:
            return True
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f".copilot_backup_{timestamp}"
        
        try:
            self.backup_dir.mkdir(exist_ok=True)
            
            # Backup .github/copilot-instructions.md
            copilot_file = self.target_dir / ".github" / "copilot-instructions.md"
            if copilot_file.exists():
                shutil.copy2(copilot_file, self.backup_dir / "copilot-instructions.md")
                print_success(f"Backup: copilot-instructions.md")
            
            # Backup .copilot/ directory
            copilot_dir = self.target_dir / ".copilot"
            if copilot_dir.exists():
                shutil.copytree(copilot_dir, self.backup_dir / ".copilot")
                print_success(f"Backup: .copilot/ directory")
            
            print_success(f"Backup criado em: {self.backup_dir.name}")
            return True
            
        except Exception as e:
            print_error(f"Erro ao criar backup: {e}")
            return False
    
    def download_from_github(self):
        """Baixa arquivos do GitHub"""
        print_info(f"Baixando de: {self.github_url}")
        
        try:
            # Cria diretório temporário
            self.temp_dir = Path(tempfile.mkdtemp())
            zip_path = self.temp_dir / "repo.zip"
            
            # Converte URL do repo para URL de download ZIP
            if "github.com" in self.github_url:
                # Transforma https://github.com/user/repo em download ZIP
                parts = self.github_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    user = parts[-2]
                    repo = parts[-1]
                    download_url = f"https://github.com/{user}/{repo}/archive/refs/heads/main.zip"
                else:
                    print_error("URL do GitHub inválida")
                    return False
            else:
                download_url = self.github_url
            
            # Baixa arquivo ZIP
            print_info("Fazendo download...")
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extrai ZIP
            print_info("Extraindo arquivos...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            print_success("Download concluído")
            return True
            
        except Exception as e:
            print_error(f"Erro ao baixar: {e}")
            print_info("Verifique se a URL está correta e se o repositório é público")
            return False
    
    def install_files(self):
        """Instala arquivos no diretório de destino"""
        try:
            # Encontra diretório extraído (normalmente repo-main/)
            extracted_dirs = [d for d in self.temp_dir.iterdir() if d.is_dir()]
            if not extracted_dirs:
                print_error("Nenhum diretório encontrado no arquivo baixado")
                return False
            
            source_dir = extracted_dirs[0]
            
            # Instala copilot-instructions.md
            source_file = source_dir / "copilot-instructions.md"
            if source_file.exists():
                github_dir = self.target_dir / ".github"
                github_dir.mkdir(exist_ok=True)
                
                dest_file = github_dir / "copilot-instructions.md"
                shutil.copy2(source_file, dest_file)
                print_success("Instalado: .github/copilot-instructions.md")
            else:
                print_warning("Arquivo copilot-instructions.md não encontrado no repo")
            
            # Instala diretório .copilot/
            source_copilot = source_dir / ".copilot"
            if source_copilot.exists():
                dest_copilot = self.target_dir / ".copilot"
                
                # Remove destino se existir
                if dest_copilot.exists():
                    shutil.rmtree(dest_copilot)
                
                shutil.copytree(source_copilot, dest_copilot)
                
                # Conta arquivos instalados
                agent_files = list((dest_copilot / "agents").glob("*.md")) if (dest_copilot / "agents").exists() else []
                print_success(f"Instalado: .copilot/ ({len(agent_files)} agents)")
            else:
                print_warning("Diretório .copilot/ não encontrado no repo")
            
            # Copia README se existir
            source_readme = source_dir / "README.md"
            if source_readme.exists():
                dest_readme = self.target_dir / ".copilot" / "README.md"
                dest_readme.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(source_readme, dest_readme)
                print_success("Instalado: .copilot/README.md")
            
            return True
            
        except Exception as e:
            print_error(f"Erro ao instalar arquivos: {e}")
            return False
    
    def cleanup(self):
        """Remove arquivos temporários"""
        if self.temp_dir and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
                print_info("Arquivos temporários removidos")
            except Exception as e:
                print_warning(f"Não foi possível remover temporários: {e}")
    
    def rollback(self):
        """Restaura backup em caso de erro"""
        if not self.backup_dir or not self.backup_dir.exists():
            return
        
        print_warning("Restaurando backup...")
        
        try:
            # Restaura copilot-instructions.md
            backup_file = self.backup_dir / "copilot-instructions.md"
            if backup_file.exists():
                dest = self.target_dir / ".github" / "copilot-instructions.md"
                shutil.copy2(backup_file, dest)
            
            # Restaura .copilot/
            backup_copilot = self.backup_dir / ".copilot"
            if backup_copilot.exists():
                dest_copilot = self.target_dir / ".copilot"
                if dest_copilot.exists():
                    shutil.rmtree(dest_copilot)
                shutil.copytree(backup_copilot, dest_copilot)
            
            print_success("Backup restaurado")
            
        except Exception as e:
            print_error(f"Erro ao restaurar backup: {e}")
    
    def print_post_install(self):
        """Imprime instruções pós-instalação"""
        print_header("✨ INSTALAÇÃO CONCLUÍDA!")
        
        print("\n📋 Próximos passos:")
        print(f"   1. Abra {Colors.BOLD}.github/copilot-instructions.md{Colors.RESET}")
        print("   2. Customize com contexto do seu projeto")
        print("   3. Reinicie o VS Code")
        print("   4. Teste com comentário: # @standards: este código está bom?")
        
        print(f"\n📚 Documentação completa: {Colors.BOLD}.copilot/README.md{Colors.RESET}")
        
        if self.backup_dir:
            print(f"\n💾 Backup salvo em: {Colors.YELLOW}{self.backup_dir.name}{Colors.RESET}")
            print("   (Pode deletar após validar instalação)")
    
    def install(self):
        """Executa instalação completa"""
        print_header("🚀 INSTALADOR DE COPILOT AGENTS")
        
        # Validações
        if not self.validate_target():
            return False
        
        if not self.check_existing_installation():
            return False
        
        # Backup
        if not self.create_backup():
            print_error("Falha ao criar backup. Abortando.")
            return False
        
        # Download
        if not self.download_from_github():
            self.cleanup()
            return False
        
        # Instalação
        if not self.install_files():
            print_error("Falha na instalação. Restaurando backup...")
            self.rollback()
            self.cleanup()
            return False
        
        # Limpeza
        self.cleanup()
        
        # Sucesso
        self.print_post_install()
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Instala sistema de GitHub Copilot Agents em projeto local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Instalar no diretório atual
  python install_copilot_agents.py --url https://github.com/user/copilot-agents
  
  # Instalar em projeto específico
  python install_copilot_agents.py --target /path/to/project --url https://github.com/user/copilot-agents
  
  # Forçar reinstalação sem backup
  python install_copilot_agents.py --url ... --force --no-backup
        """
    )
    
    parser.add_argument(
        '--target',
        default='.',
        help='Diretório do projeto (default: diretório atual)'
    )
    
    parser.add_argument(
        '--url',
        required=True,
        help='URL do repositório GitHub (ex: https://github.com/user/repo)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Sobrescrever instalação existente'
    )
    
    parser.add_argument(
        '--no-backup',
        dest='backup',
        action='store_false',
        help='Não criar backup de arquivos existentes'
    )
    
    args = parser.parse_args()
    
    # Executa instalação
    installer = CopilotAgentInstaller(
        target_dir=args.target,
        github_url=args.url,
        force=args.force,
        backup=args.backup
    )
    
    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()