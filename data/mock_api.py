ELECTION_DATA = {
    "USA": {
        "name": "United States of America",
        "system": "Electoral College & First-Past-the-Post",
        "timeline": [
            {"phase": "Registration", "date": "15-30 days before election", "description": "Final day to sign up to vote in most states."},
            {"phase": "Early Voting", "date": "2-4 weeks before", "description": "Vote early in person or by mail in many states."},
            {"phase": "Election Day", "date": "First Tuesday in November", "description": "The main day for in-person voting."},
            {"phase": "Electoral College Vote", "date": "Mid-December", "description": "Electors officially cast their votes for President."},
            {"phase": "Inauguration", "date": "January 20", "description": "The new President is sworn into office."}
        ],
        "simulator_steps": [
            {"id": "check_in", "title": "Check In", "description": "Show your ID (if required by state) and verify your name on the voter roll."},
            {"id": "get_ballot", "title": "Receive Ballot", "description": "Get your paper or electronic ballot from the poll worker."},
            {"id": "vote", "title": "Cast Vote", "description": "Select candidates for President, Senate, House, and local offices. Choose your preferred presidential candidate below:", "type": "choice", "options": ["Candidate A (Party X)", "Candidate B (Party Y)", "Candidate C (Independent)"]},
            {"id": "submit", "title": "Submit Ballot", "description": "Feed your paper ballot into the scanner or submit on the machine. Get your 'I Voted' sticker!"}
        ]
    },
    "India": {
        "name": "India",
        "system": "Parliamentary Democracy & First-Past-the-Post",
        "timeline": [
            {"phase": "Election Announcement", "date": "Varies (Weeks before phase 1)", "description": "Election Commission announces the multi-phase schedule."},
            {"phase": "Nomination Filing", "date": "Specific to each phase", "description": "Candidates file their nomination papers."},
            {"phase": "Campaigning Ends", "date": "48 hours before voting", "description": "Silence period begins; no active campaigning allowed."},
            {"phase": "Polling Days", "date": "Multiple phases over weeks", "description": "Voting occurs across different states on different days using EVMs (Electronic Voting Machines)."},
            {"phase": "Counting Day", "date": "Single day after all phases end", "description": "Votes from all phases are counted and results declared."}
        ],
        "simulator_steps": [
            {"id": "queue", "title": "Join the Queue", "description": "Wait in line at your designated polling booth."},
            {"id": "verify", "title": "Verification", "description": "Polling officer checks your name on the electoral roll and your Voter ID (EPIC)."},
            {"id": "ink", "title": "Indelible Ink", "description": "Officer marks your left index finger with indelible ink and you sign the register."},
            {"id": "evm_vote", "title": "Vote on EVM", "description": "Go to the voting compartment. Press the blue button next to your chosen candidate's symbol on the Electronic Voting Machine (EVM).", "type": "choice", "options": ["Candidate 1 (Lotus)", "Candidate 2 (Hand)", "Candidate 3 (Broom)", "NOTA (None of the Above)"]},
            {"id": "vvpat", "title": "Check VVPAT", "description": "Look at the VVPAT machine window to verify a slip with your candidate's symbol printed on it before it drops into the sealed box."}
        ]
    },
    "UK": {
        "name": "United Kingdom",
        "system": "Parliamentary System & First-Past-the-Post",
        "timeline": [
            {"phase": "Dissolution of Parliament", "date": "25 working days before election", "description": "Parliament is dissolved and the campaign officially begins."},
            {"phase": "Registration Deadline", "date": "12 working days before", "description": "Last day to register to vote."},
            {"phase": "Postal Vote Application", "date": "11 working days before", "description": "Deadline to apply for a postal vote."},
            {"phase": "Polling Day", "date": "A Thursday (usually)", "description": "Polling stations open from 7 AM to 10 PM."},
            {"phase": "Results Night", "date": "Overnight into Friday", "description": "Counting begins immediately after polls close. Results declared locally."}
        ],
        "simulator_steps": [
            {"id": "poll_card", "title": "Receive Poll Card", "description": "You receive a poll card in the mail telling you where your polling station is."},
            {"id": "arrive", "title": "Arrive at Station", "description": "Give your name and address to the staff. Show accepted photo ID."},
            {"id": "ballot_paper", "title": "Get Ballot Paper", "description": "You are given a stamped ballot paper with a list of local candidates."},
            {"id": "booth", "title": "Voting Booth", "description": "Go to a booth. Mark a single 'X' next to the candidate you wish to vote for to represent your constituency.", "type": "choice", "options": ["Candidate Red", "Candidate Blue", "Candidate Yellow", "Candidate Green"]},
            {"id": "box", "title": "Ballot Box", "description": "Fold your ballot paper in half and drop it into the sealed ballot box."}
        ]
    }
}

def get_country_data(country_name: str) -> dict:
    """Returns mock data for a given country."""
    return ELECTION_DATA.get(country_name, {})

def get_supported_countries() -> list:
    """Returns a list of supported countries."""
    return list(ELECTION_DATA.keys())
