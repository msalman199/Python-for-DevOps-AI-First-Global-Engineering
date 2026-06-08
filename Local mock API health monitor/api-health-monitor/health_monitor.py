#!/usr/bin/env python3
"""
API Health Monitor
Periodically checks API endpoints and logs their status
"""

import requests
import time
import json
from datetime import datetime
import sys

class APIHealthMonitor:
    def __init__(self, base_url, check_interval=10):
        """
        Initialize the health monitor
        
        Args:
            base_url: Base URL of the API to monitor
            check_interval: Seconds between health checks
        """
        self.base_url = base_url
        self.check_interval = check_interval
        self.log_file = 'logs/health_monitor.log'
        self.status_file = 'logs/current_status.json'
        
    def log_message(self, message, level='INFO'):
        """
        Write a log message to file and console
        
        Args:
            message: The message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Print to console
        print(log_entry)
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def check_endpoint(self, endpoint, timeout=5):
        """
        Check a single endpoint and return its status
        
        Args:
            endpoint: The endpoint path to check (e.g., '/health')
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary with status information
        """
        url = f"{self.base_url}{endpoint}"
        result = {
            'endpoint': endpoint,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'response_time': None,
            'status_code': None,
            'error': None
        }
        
        try:
            # TODO: Make HTTP GET request to the endpoint
            # Measure the time it takes to get a response
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            end_time = time.time()
            
            # TODO: Calculate response time in milliseconds
            result['response_time'] = round((end_time - start_time) * 1000, 2)
            result['status_code'] = response.status_code
            
            # TODO: Determine if endpoint is healthy
            # Consider 200-299 status codes as healthy
            if 200 <= response.status_code < 300:
                result['status'] = 'healthy'
            else:
                result['status'] = 'unhealthy'
                
        except requests.exceptions.Timeout:
            # TODO: Handle timeout errors
            result['status'] = 'timeout'
            result['error'] = 'Request timed out'
            
        except requests.exceptions.ConnectionError:
            # TODO: Handle connection errors
            result['status'] = 'unreachable'
            result['error'] = 'Could not connect to service'
            
        except Exception as e:
            # TODO: Handle any other errors
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def check_all_endpoints(self, endpoints):
        """
        Check all configured endpoints
        
        Args:
            endpoints: List of endpoint paths to check
            
        Returns:
            List of results for all endpoints
        """
        results = []
        
        for endpoint in endpoints:
            # TODO: Check each endpoint
            result = self.check_endpoint(endpoint)
            results.append(result)
            
            # TODO: Log the result with appropriate level
            if result['status'] == 'healthy':
                self.log_message(
                    f"{endpoint} is healthy (Response time: {result['response_time']}ms)",
                    'INFO'
                )
            else:
                self.log_message(
                    f"{endpoint} is {result['status']} - {result.get('error', 'Status code: ' + str(result['status_code']))}",
                    'ERROR'
                )
        
        return results
    
    def save_status(self, results):
        """
        Save current status to JSON file
        
        Args:
            results: List of endpoint check results
        """
        status_data = {
            'last_check': datetime.now().isoformat(),
            'endpoints': results,
            'summary': {
                'total': len(results),
                'healthy': sum(1 for r in results if r['status'] == 'healthy'),
                'unhealthy': sum(1 for r in results if r['status'] != 'healthy')
            }
        }
        
        # TODO: Write status to JSON file
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def run(self, endpoints, duration=None):
        """
        Run the health monitor continuously
        
        Args:
            endpoints: List of endpoints to monitor
            duration: How long to run (seconds), None for infinite
        """
        self.log_message(f"Starting health monitor for {self.base_url}")
        self.log_message(f"Monitoring endpoints: {', '.join(endpoints)}")
        self.log_message(f"Check interval: {self.check_interval} seconds")
        
        start_time = time.time()
        check_count = 0
        
        try:
            while True:
                check_count += 1
                self.log_message(f"--- Health Check #{check_count} ---")
                
                # TODO: Check all endpoints
                results = self.check_all_endpoints(endpoints)
                
                # TODO: Save current status
                self.save_status(results)
                
                # Check if we should stop
                if duration and (time.time() - start_time) >= duration:
                    self.log_message("Monitoring duration completed")
                    break
                
                # TODO: Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log_message("Monitoring stopped by user", 'INFO')
        except Exception as e:
            self.log_message(f"Monitor error: {str(e)}", 'ERROR')

# Main execution
if __name__ == '__main__':
    # Configuration
    BASE_URL = 'http://localhost:5000'
    CHECK_INTERVAL = 10  # seconds
    
    # Endpoints to monitor
    ENDPOINTS = [
        '/health',
        '/api/users',
        '/api/data'
    ]
    
    # Create and run monitor
    monitor = APIHealthMonitor(BASE_URL, CHECK_INTERVAL)
    
    # Run for 2 minutes (120 seconds) for testing
    # Change to None for continuous monitoring
    monitor.run(ENDPOINTS, duration=120)
