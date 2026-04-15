from typing import Dict, List
import time

class DPoSConsensus:
    def __init__(self, max_witnesses: int = 21):
        self.max_witnesses = max_witnesses
        self.candidates: Dict[str, int] = {}
        self.voters: Dict[str, str] = {}
        self.witnesses: List[str] = []

    def register_candidate(self, candidate: str) -> bool:
        if candidate in self.candidates:
            return False
        self.candidates[candidate] = 0
        return True

    def vote(self, voter: str, candidate: str) -> bool:
        if candidate not in self.candidates:
            return False
        
        old_vote = self.voters.get(voter)
        if old_vote:
            self.candidates[old_vote] -= 1
        
        self.candidates[candidate] += 1
        self.voters[voter] = candidate
        return True

    def unvote(self, voter: str) -> bool:
        if voter not in self.voters:
            return False
        
        candidate = self.voters[voter]
        self.candidates[candidate] -= 1
        del self.voters[voter]
        return True

    def update_witnesses(self) -> List[str]:
        sorted_candidates = sorted(self.candidates.items(), key=lambda x: x[1], reverse=True)
        self.witnesses = [c[0] for c in sorted_candidates[:self.max_witnesses]]
        return self.witnesses

    def get_witnesses(self) -> List[str]:
        return self.witnesses.copy()
