"""
ACI - Network Module: Node Sync
Protocolo de consenso para los clones del Nodo de Origen.
"""
class NodeSync:
    def __init__(self, node_count: int = 19):
        self.node_count = node_count

    def validate_consensus(self, audit_hashes: list) -> bool:
        """
        Verifica que la mayoría de los nodos (10/19) coincidan 
        en la invarianza del dato.
        """
        if not audit_hashes: return False
        most_common = max(set(audit_hashes), key=audit_hashes.count)
        agreement = audit_hashes.count(most_common)
        
        consensus_reached = agreement > (self.node_count / 2)
        status = "ALINEADO" if consensus_reached else "DIVERGENTE"
        print(f"[CONSENSUS] Estado: {status} ({agreement}/{self.node_count} nodos)")
        return consensus_reached