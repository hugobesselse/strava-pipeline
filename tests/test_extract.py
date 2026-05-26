import json
from src.extract import refresh_token_if_needed, extract_all_activities, save_activities

class MockHTTPClientRefresh:
    def post(self,url,data):
        return type("R",(), {
            "json": lambda self: {"access_token":"new_token"}
        })()
    
def test_refresh_token_calls_api():
    # Function should return a new token if the old token has expired. 
    config = {
        "access_token": "old_token",
        "refresh_token": "refresh_token",
        "client_id": "client_id",
        "client_secret": "client_secret",
        "expires_at": 0, 
    }

    result = refresh_token_if_needed(config,http_client=MockHTTPClientRefresh())

    assert result == "new_token"

class MockHTTPClientPaginated:
     
    def __init__(self, pages):
        self.pages = pages
    
    def get(self, url, headers, params):
        page = params["page"]
        data = self.pages.get(page, [])
        return type ("R", (), {"json": lambda self:data})()
    
def test_extract_stops():
    # Function loop should end if page is empty.
    mock_client = MockHTTPClientPaginated({
        1: [{"id": 1}, {"id": 2}],
        2: [{"id": 3}],
        3: [],
    })

    config = {"access_token": "fake", "expires_at": 9999999999}
    activities = extract_all_activities(config, http_client=mock_client)

    assert len(activities) == 3

def test_save_activities(tmp_path):
    activities = [{"id":1, "name": "Run"}, {"id":2, "name": "Ride"}]
    output_path = tmp_path / "activities_test.json"

    save_activities(activities, output_path=output_path)

    with open(output_path) as f:
        saved = json.load(f)   
    
    assert len(saved) == 2
    assert saved[0]["id"] == 1


    