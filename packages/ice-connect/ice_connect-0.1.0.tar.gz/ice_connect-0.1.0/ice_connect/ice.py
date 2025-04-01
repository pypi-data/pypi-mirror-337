import asyncio
import pystun3
import socket

class IceAgent:
    def __init__(self, stun_server, stun_port=3478):
        self.stun_server = stun_server
        self.stun_port = stun_port
        self.local_candidates = []
        self.remote_candidates = []

    async def gather_local_candidates(self):
        """Gather local ICE candidates using the specified STUN server."""
        nat_type, external_ip, external_port = pystun3.get_ip_info(stun_host=self.stun_server, stun_port=self.stun_port)
        if external_ip:
            self.local_candidates.append((external_ip, external_port))
            print(f"Local Candidate: {external_ip}:{external_port}")
        return self.local_candidates

    def add_remote_candidate(self, ip, port):
        """Add a remote candidate."""
        self.remote_candidates.append((ip, port))
        print(f"Remote Candidate added: {ip}:{port}")

    async def establish_connection(self):
        """Simulate connectivity checks and ICE establishment."""
        for candidate in self.remote_candidates:
            ip, port = candidate
            print(f"Checking connectivity to {ip}:{port}")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.settimeout(2)
                    sock.sendto(b"HELLO", (ip, port))
                    data, _ = sock.recvfrom(1024)
                    if data == b"HELLO":
                        print("ICE connection successfully established!")
                        return True
            except socket.timeout:
                print(f"Failed to connect to {ip}:{port}")
        print("ICE connection failed.")
        return False
