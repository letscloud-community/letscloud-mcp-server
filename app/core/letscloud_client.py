"""
LetsCloud API Client
~~~~~~~~~~~~~~~~~~~

Cliente para interação com a API da LetsCloud.
"""

import requests
from typing import Dict, List, Optional, Any
from .config import settings

class LetsCloudClient:
    """
    Cliente para interação com a API da LetsCloud.
    """

    def __init__(self, api_token: str):
        """
        Inicializa o cliente com o token de API.

        Args:
            api_token: Token de API da LetsCloud
        """
        self.api_token = api_token
        self.base_url = "https://api.letscloud.io/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Faz uma requisição para a API da LetsCloud.

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            **kwargs: Argumentos adicionais para a requisição

        Returns:
            Resposta da API em formato de dicionário
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def list_servers(self) -> List[Dict[str, Any]]:
        """
        Lista todos os servidores.

        Returns:
            Lista de servidores
        """
        return self._make_request("GET", "servers")

    def get_server(self, server_id: int) -> Dict[str, Any]:
        """
        Obtém detalhes de um servidor específico.

        Args:
            server_id: ID do servidor

        Returns:
            Detalhes do servidor
        """
        return self._make_request("GET", f"servers/{server_id}")

    def create_server(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo servidor.

        Args:
            data: Dados do servidor

        Returns:
            Detalhes do servidor criado
        """
        return self._make_request("POST", "servers", json=data)

    def delete_server(self, server_id: int) -> None:
        """
        Deleta um servidor.

        Args:
            server_id: ID do servidor
        """
        self._make_request("DELETE", f"servers/{server_id}")

    def list_ssh_keys(self) -> List[Dict[str, Any]]:
        """
        Lista todas as chaves SSH.

        Returns:
            Lista de chaves SSH
        """
        return self._make_request("GET", "ssh-keys")

    def create_ssh_key(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova chave SSH.

        Args:
            data: Dados da chave SSH

        Returns:
            Detalhes da chave SSH criada
        """
        return self._make_request("POST", "ssh-keys", json=data)

    def delete_ssh_key(self, key_id: int) -> None:
        """
        Deleta uma chave SSH.

        Args:
            key_id: ID da chave SSH
        """
        self._make_request("DELETE", f"ssh-keys/{key_id}")

    def create_snapshot(self, server_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um snapshot de um servidor.

        Args:
            server_id: ID do servidor
            data: Dados do snapshot

        Returns:
            Detalhes do snapshot criado
        """
        return self._make_request("POST", f"servers/{server_id}/snapshots", json=data)

    def list_snapshots(self, server_id: int) -> List[Dict[str, Any]]:
        """
        Lista todos os snapshots de um servidor.

        Args:
            server_id: ID do servidor

        Returns:
            Lista de snapshots
        """
        return self._make_request("GET", f"servers/{server_id}/snapshots")

    def delete_snapshot(self, server_id: int, snapshot_id: int) -> None:
        """
        Deleta um snapshot.

        Args:
            server_id: ID do servidor
            snapshot_id: ID do snapshot
        """
        self._make_request("DELETE", f"servers/{server_id}/snapshots/{snapshot_id}")

    def restore_snapshot(self, server_id: int, snapshot_id: int) -> Dict[str, Any]:
        """
        Restaura um servidor a partir de um snapshot.

        Args:
            server_id: ID do servidor
            snapshot_id: ID do snapshot

        Returns:
            Detalhes da operação de restauração
        """
        return self._make_request("POST", f"servers/{server_id}/snapshots/{snapshot_id}/restore") 