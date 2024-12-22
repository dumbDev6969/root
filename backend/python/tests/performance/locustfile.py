from locust import HttpUser, task, between
import json

class JobSearchUser(HttpUser):
    wait_time = between(1, 3)  # Random wait between tasks
    
    def on_start(self):
        """Setup before starting tests - login and get token"""
        # Login credentials
        credentials = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        # Login request
        response = self.client.post("/login", json=credentials)
        if response.status_code == 200:
            self.token = response.json().get("token", "")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = ""
            self.headers = {}

    @task(3)
    def view_jobs(self):
        """Test job listing endpoint"""
        self.client.get("/api/jobs", headers=self.headers)

    @task(2)
    def search_jobs(self):
        """Test job search functionality"""
        params = {
            "keyword": "developer",
            "location": "San Francisco"
        }
        self.client.get("/api/jobs/search", params=params, headers=self.headers)

    @task(1)
    def view_job_details(self):
        """Test single job view"""
        # Assuming job ID 1 exists
        self.client.get("/api/jobs/1", headers=self.headers)

    @task(1)
    def apply_for_job(self):
        """Test job application submission"""
        application_data = {
            "job_id": "1",
            "cover_letter": "I am interested in this position",
            "resume_url": "https://example.com/resume.pdf"
        }
        self.client.post(
            "/api/jobs/apply",
            json=application_data,
            headers=self.headers
        )

    @task(2)
    def view_profile(self):
        """Test profile viewing"""
        self.client.get("/api/profile/current", headers=self.headers)

    @task(1)
    def update_profile(self):
        """Test profile update"""
        profile_data = {
            "phone_number": "1234567890",
            "state": "California",
            "city_or_province": "San Francisco"
        }
        self.client.put(
            "/api/profile/update",
            json=profile_data,
            headers=self.headers
        )

    @task(1)
    def geographic_data(self):
        """Test geographic data endpoints"""
        self.client.get("/api/geo/regions")
        self.client.get("/api/geo/provinces")
        self.client.get("/api/geo/municipalities")

    @task(1)
    def two_factor_setup(self):
        """Test 2FA setup flow"""
        # Initialize 2FA setup
        response = self.client.post(
            "/api/2fa/setup",
            headers=self.headers
        )
        if response.status_code == 200:
            # Verify 2FA setup with test token
            verify_data = {
                "token": "123456"  # Test token
            }
            self.client.post(
                "/api/2fa/verify",
                json=verify_data,
                headers=self.headers
            )

    def on_stop(self):
        """Cleanup after tests - logout"""
        if self.token:
            self.client.post("/logout", headers=self.headers)