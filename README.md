# V1 Branch Updates

This branch contains significant improvements to the project infrastructure and documentation:

## 1. CI/CD Pipeline
- Automated testing with pytest and coverage reporting
- Code quality checks (flake8, black, isort)
- Security scanning (bandit, safety)
- Performance testing integration
- Automated deployment for main branch

## 2. Performance Testing
- Comprehensive test scenarios for all major API endpoints
- Authentication flow testing
- Job management operations
- Profile operations
- Geographic data endpoints
- 2FA setup testing
- Configurable load testing parameters

## 3. Frontend JWT Integration Guide
- Complete authentication flow implementation
- Token management utilities
- Protected route handling
- 2FA integration
- Error handling
- Security best practices
- Example implementations
- Troubleshooting guide

## Getting Started

1. CI/CD Pipeline:
   - Automatically runs on push to main branch and pull requests
   - View results in GitHub Actions tab

2. Performance Testing:
   ```bash
   locust -f backend/python/tests/performance/locustfile.py --host http://localhost:10000
   ```
   Access Locust web interface at http://localhost:8089

3. Frontend Integration:
   - Follow the guide in `claudeDev_docs/userInstructions/frontend_jwt_integration.md`
   - Implements secure authentication patterns
   - Includes complete code examples

## Documentation
- CI/CD: `.github/workflows/main.yml`
- Performance Tests: `backend/python/tests/performance/locustfile.py`
- JWT Integration: `claudeDev_docs/userInstructions/frontend_jwt_integration.md`
