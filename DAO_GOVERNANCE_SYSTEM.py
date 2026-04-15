import time
from enum import Enum
from typing import Dict, List

class VoteChoice(Enum):
    APPROVE = "approve"
    REJECT = "reject"

class DAOGovernance:
    def __init__(self, voting_delay: int = 86400, voting_period: int = 604800):
        self.proposals: Dict[int, Dict] = {}
        self.votes: Dict[int, Dict[str, str]] = {}
        self.proposal_id = 1
        self.voting_delay = voting_delay
        self.voting_period = voting_period

    def create_proposal(self, proposer: str, title: str, description: str) -> int:
        pid = self.proposal_id
        self.proposal_id += 1
        self.proposals[pid] = {
            "id": pid,
            "proposer": proposer,
            "title": title,
            "description": description,
            "start_time": time.time() + self.voting_delay,
            "end_time": time.time() + self.voting_delay + self.voting_period,
            "status": "pending"
        }
        self.votes[pid] = {}
        return pid

    def cast_vote(self, voter: str, proposal_id: int, choice: VoteChoice) -> bool:
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        now = time.time()
        
        if now < proposal["start_time"] or now > proposal["end_time"]:
            return False
        
        self.votes[proposal_id][voter] = choice.value
        return True

    def tally_votes(self, proposal_id: int) -> Dict[str, int]:
        votes = self.votes.get(proposal_id, {})
        approve = sum(1 for c in votes.values() if c == VoteChoice.APPROVE.value)
        reject = sum(1 for c in votes.values() if c == VoteChoice.REJECT.value)
        return {"approve": approve, "reject": reject}
